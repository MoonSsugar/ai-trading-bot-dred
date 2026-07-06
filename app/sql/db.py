from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


def create_pool(
    dsn: str, enable_logging: bool = False
) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(dsn, echo=enable_logging)
    return async_sessionmaker(engine, expire_on_commit=False)
