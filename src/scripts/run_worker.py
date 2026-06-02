"""
Script de entrada para ejecutar el worker asíncrono.

Usage:
    poetry run worker
    python -m src.scripts.run_worker
"""

import asyncio
import signal
import sys
from typing import Any, Dict

from logger_tracker import logg_info, logg_error

from src.config import DEBUG
from src.worker.worker_container import WorkerContainer


container: WorkerContainer = None


async def handle_message(body: Dict[str, Any], headers: Dict[str, str]) -> None:
    event_id = headers.get("event_id", "unknown")
    correlation_id = headers.get("correlation_id", "")

    if correlation_id:
        await container.idempotency.try_acquire(
            f"rabbit:{event_id}",
            ttl=container.idempotency.ttl,
        )

    event_type = body.get("event_type", "unknown")
    aggregate_type = body.get("aggregate_type", "unknown")
    aggregate_id = body.get("aggregate_id", "unknown")

    logg_info(
        f"Processing event: {event_type} "
        f"[aggregate={aggregate_type}:{aggregate_id}, "
        f"correlation_id={correlation_id}]"
    )

    await container.kafka_publisher.publish_event(
        event_type=event_type,
        aggregate_type=aggregate_type,
        aggregate_id=aggregate_id,
        correlation_id=correlation_id,
        payload=body.get("data", body),
        event_id=event_id,
    )

    await container.idempotency.mark_processed(
        f"rabbit:{event_id}",
    )


async def amain() -> None:
    global container

    logg_info("Starting Kerverus Async Worker...")

    container = WorkerContainer()
    await container.connect_all()

    health = await container.health_checker.check_all()
    logg_info(f"Initial health: {health.status}")
    for name, check in health.checks.items():
        logg_info(f"  {name}: {'✓' if check['healthy'] else '✗'} {check['message']}")

    if health.status != "healthy" and not DEBUG:
        logg_error("Initial health check failed, aborting")
        await container.disconnect_all()
        sys.exit(1)

    outbox_processor = await container.create_outbox_processor()
    rabbit_consumer = await container.create_rabbit_consumer(
        message_handler=handle_message,
    )

    async def shutdown(sig: signal.Signals) -> None:
        logg_info(f"Received signal {sig.name}, shutting down...")
        await outbox_processor.stop()
        await rabbit_consumer.stop()
        await container.disconnect_all()
        logg_info("Worker shutdown complete")

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda s=sig: asyncio.create_task(shutdown(s)),
        )

    await asyncio.gather(
        outbox_processor.start(),
        rabbit_consumer.start(),
    )


def run_worker() -> None:
    try:
        asyncio.run(amain())
    except KeyboardInterrupt:
        logg_info("Worker interrupted by user")
    except Exception as e:
        logg_error(f"Worker failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    run_worker()
