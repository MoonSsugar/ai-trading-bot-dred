import asyncio
import logging
import sys

import click


@click.group()
def cli():
    pass


@cli.command()
def run():
    from app.bot import main
    from app.services.scheduler.run_worker import run_worker
    from app.utils.redis import redis_factory

    async def _main():
        logging.basicConfig(
            level=logging.INFO,
        )

        await asyncio.gather(main(), run_worker(redis_factory()))

    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        sys.exit()
