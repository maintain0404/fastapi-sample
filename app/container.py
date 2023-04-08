from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import (
    Callable,
    Configuration,
    Factory,
    Resource,
    Singleton,
)
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from core.db.orm import build_sa_uri, get_session
from core.var.config import config, Config
from domain.user.repo.user_repo import UserRepo
from domain.user.service.auth_service import AuthService
from domain.user.service.user_self_service import UserSelfService


class MainContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["handler.rest.endpoints.user"])
    config: Config = Configuration(
        pydantic_settings=[config], strict=True
    )  # Duck-typing
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
    user_repo = Factory(UserRepo, session=sa_session)
    auth_service = Factory(
        AuthService,
        access_token_expire=config.jwt.access_token_expire,
        refresh_token_expire=config.jwt.refresh_token_expire,
        jwt_secret=config.jwt.secret,
        jwt_algorithm=config.jwt.algorithm,
    )
    user_self_service = Factory(UserSelfService, repo=user_repo, auth=auth_service)
