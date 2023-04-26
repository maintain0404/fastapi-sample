# copied from dependency_injector.wiring
# for using FastAPI Depends with Annotated
# https://github.com/tiangolo/fastapi/releases/tag/0.95.0

import inspect
from types import GenericAlias
from typing import Annotated, Any, Callable, cast, get_args, get_origin

from dependency_injector.wiring import (
    _get_patched,
    _is_fastapi_depends,
    _Marker,
    Closing,
    F,
)


def _fetch_reference_injections(  # noqa: C901
    fn: Callable[..., Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    # Hotfix, see:
    # - https://github.com/ets-labs/python-dependency-injector/issues/362
    # - https://github.com/ets-labs/python-dependency-injector/issues/398
    if any((fn is GenericAlias, getattr(fn, "__func__", None) is GenericAlias)):
        fn = fn.__init__  # type: ignore[misc]

    try:
        signature = inspect.signature(fn)
    except ValueError as exception:
        if "no signature found" in str(exception):
            return {}, {}
        elif "not supported by signature" in str(exception):
            return {}, {}
        else:
            raise exception

    injections = {}
    closing = {}
    for parameter_name, parameter in signature.parameters.items():
        if get_origin(parameter.annotation) is Annotated:
            marker = get_args(parameter.annotation)[1]
        else:
            marker = parameter.default

        if not isinstance(marker, _Marker) and not _is_fastapi_depends(marker):
            continue

        if _is_fastapi_depends(marker):
            marker = marker.dependency

            if not isinstance(marker, _Marker):
                continue

        if isinstance(marker, Closing):
            marker = marker.provider
            closing[parameter_name] = marker

        injections[parameter_name] = marker
    return injections, closing


def inject(fn: F) -> F:
    reference_injections, reference_closing = _fetch_reference_injections(fn)
    patched = _get_patched(fn, reference_injections, reference_closing)
    return cast(F, patched)
