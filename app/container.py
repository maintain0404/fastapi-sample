from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import (
    Callable,
    Configuration,
    Factory,
    Resource,
    Singleton,
)
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.db.orm import build_sa_uri, get_session
from core.var.config import config, Config
from domain.account.repo.account import AccountRepo
from domain.account.service.account_self import AccountSelfService
from domain.account.service.auth import AuthService


class MainContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["handler.rest.endpoints.account"])
    # duck-typing
    config: Config = Configuration(
        pydantic_settings=[config], strict=True
    )  # type: ignore[assignment]
    sa_uri = Callable(
        build_sa_uri,
        name=config.db.name,
        api=config.db.api,
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,
        port=config.db.port,
        path=config.db.path,
    )
    sa_engine = Callable(create_async_engine, sa_uri)
    sa_sessionmaker = Singleton(async_sessionmaker, sa_engine)
    sa_session = Resource(
        get_session,
        sessionmaker=sa_sessionmaker,
    )
    account_repo = Factory(AccountRepo, session=sa_session)
    auth_service = Factory(
        AuthService,
        access_token_expire=config.jwt.access_token_expire,
        refresh_token_expire=config.jwt.refresh_token_expire,
        jwt_secret=config.jwt.secret,
        jwt_algorithm=config.jwt.algorithm,
    )
    account_self_service = Factory(
        AccountSelfService, repo=account_repo, auth=auth_service
    )
