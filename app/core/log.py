from logging import Filter, LogRecord

from .context import Context


class ContextInjectingFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        d = {"id": Context.id, "runtime": Context.runtime}
        record.__dict__.update(d)

        return super().filter(record)
