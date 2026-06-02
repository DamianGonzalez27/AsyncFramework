import asyncio
import json
from typing import Any, Callable, Dict, Optional
from logger_tracker import logg_info, logg_error, logg_debug


class AsyncRabbitMQAdapter:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 5672,
        username: str = "guest",
        password: str = "guest",
        vhost: str = "/",
        prefetch_count: int = 20,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.vhost = vhost
        self.prefetch_count = prefetch_count
        self.connection = None
        self.channel = None

    async def connect(self) -> None:
        try:
            import aio_pika

            self.connection = await aio_pika.connect_robust(
                host=self.host,
                port=self.port,
                login=self.username,
                password=self.password,
                virtualhost=self.vhost,
            )
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=self.prefetch_count)
            logg_info(f"✓ Async RabbitMQ connected: {self.host}:{self.port}")
        except Exception as e:
            logg_error(f"✗ Failed to connect to Async RabbitMQ: {e}")
            raise

    async def declare_queue(
        self,
        queue_name: str,
        durable: bool = True,
        dead_letter_exchange: Optional[str] = None,
        dead_letter_routing_key: Optional[str] = None,
        message_ttl: Optional[int] = None,
    ) -> Any:
        try:
            if not self.channel:
                raise RuntimeError("Not connected to RabbitMQ")
            arguments = {}
            if dead_letter_exchange:
                arguments["x-dead-letter-exchange"] = dead_letter_exchange
            if dead_letter_routing_key:
                arguments["x-dead-letter-routing-key"] = dead_letter_routing_key
            if message_ttl:
                arguments["x-message-ttl"] = message_ttl

            queue = await self.channel.declare_queue(
                queue_name,
                durable=durable,
                arguments=arguments,
            )
            logg_debug(f"Queue declared: {queue_name}")
            return queue
        except Exception as e:
            logg_error(f"Failed to declare queue {queue_name}: {e}")
            raise

    async def declare_exchange(
        self,
        exchange_name: str,
        exchange_type: str = "direct",
        durable: bool = True,
    ) -> Any:
        try:
            if not self.channel:
                raise RuntimeError("Not connected to RabbitMQ")
            exchange = await self.channel.declare_exchange(
                exchange_name,
                type=exchange_type,
                durable=durable,
            )
            logg_debug(f"Exchange declared: {exchange_name}")
            return exchange
        except Exception as e:
            logg_error(f"Failed to declare exchange {exchange_name}: {e}")
            raise

    async def bind_queue(
        self,
        queue_name: str,
        exchange_name: str,
        routing_key: str,
    ) -> None:
        try:
            if not self.channel:
                raise RuntimeError("Not connected to RabbitMQ")
            queue = await self.channel.get_queue(queue_name)
            exchange = await self.channel.get_exchange(exchange_name)
            await queue.bind(exchange, routing_key=routing_key)
            logg_debug(f"Queue {queue_name} bound to {exchange_name} via {routing_key}")
        except Exception as e:
            logg_error(f"Failed to bind queue: {e}")
            raise

    async def publish(
        self,
        queue_name: str,
        payload: Dict[str, Any],
        correlation_id: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        try:
            if not self.channel:
                raise RuntimeError("Not connected to RabbitMQ")
            import aio_pika

            message_body = json.dumps(payload)
            message = aio_pika.Message(
                body=message_body.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                correlation_id=correlation_id or "",
                headers=headers or {},
            )
            await self.channel.default_exchange.publish(
                message,
                routing_key=queue_name,
            )
            logg_debug(f"Message published to {queue_name}")
        except Exception as e:
            logg_error(f"Failed to publish message: {e}")
            raise

    async def publish_to_exchange(
        self,
        exchange_name: str,
        routing_key: str,
        payload: Dict[str, Any],
        correlation_id: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        try:
            if not self.channel:
                raise RuntimeError("Not connected to RabbitMQ")
            import aio_pika

            exchange = await self.channel.get_exchange(exchange_name)
            message_body = json.dumps(payload)
            message = aio_pika.Message(
                body=message_body.encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                correlation_id=correlation_id or "",
                headers=headers or {},
            )
            await exchange.publish(message, routing_key=routing_key)
            logg_debug(f"Message published to exchange {exchange_name}/{routing_key}")
        except Exception as e:
            logg_error(f"Failed to publish to exchange: {e}")
            raise

    async def consume(
        self,
        queue_name: str,
        callback: Callable,
    ) -> None:
        try:
            if not self.channel:
                raise RuntimeError("Not connected to RabbitMQ")
            queue = await self.channel.get_queue(queue_name)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    try:
                        await callback(message)
                    except Exception as e:
                        logg_error(f"Callback error processing message: {e}")
                        await message.nack(requeue=False)
        except Exception as e:
            logg_error(f"Failed to consume from queue {queue_name}: {e}")
            raise

    async def ack(self, message: Any) -> None:
        try:
            await message.ack()
        except Exception as e:
            logg_error(f"Failed to ack message: {e}")

    async def nack(self, message: Any, requeue: bool = False) -> None:
        try:
            await message.nack(requeue=requeue)
        except Exception as e:
            logg_error(f"Failed to nack message: {e}")

    async def close(self) -> None:
        try:
            if self.connection and not self.connection.is_closed:
                await self.connection.close()
                logg_info("✓ Async RabbitMQ connection closed")
        except Exception as e:
            logg_error(f"Error closing Async RabbitMQ connection: {e}")
