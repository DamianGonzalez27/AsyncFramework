"""Registro central de handlers de eventos.

Cada módulo de dominio puede registrar sus propios handlers
para procesar eventos específicos. El worker utiliza este
registro para despachar los mensajes entrantes.
"""

from typing import Any, Awaitable, Callable, Dict

from src.modules.clients.handlers.client_handler import ClientHandler
from src.modules.users.handlers.account_handler import AccountHandler
from src.modules.users.handlers.client_handler import ClientHandler as UserClientHandler
from src.modules.users.handlers.application_handler import ApplicationHandler
from src.modules.users.handlers.repo_handler import RepoHandler
from src.modules.payments.handlers.payment_handler import PaymentHandler
from src.modules.products.handlers.product_handler import ProductHandler


EVENT_HANDLERS: Dict[str, Callable[..., Awaitable[None]]] = {
    # Clients
    "client.created": ClientHandler.handle_created,
    "client.updated": ClientHandler.handle_updated,
    # Users - Accounts
    "account.created": AccountHandler.handle_created,
    "account.updated": AccountHandler.handle_updated,
    "account.deleted": AccountHandler.handle_deleted,
    # Users - Clients
    "user.client.created": UserClientHandler.handle_created,
    # Users - Repos
    "repo.created": RepoHandler.handle_created,
    # Users - Applications
    "application.created": ApplicationHandler.handle_created,
    "application.deleted": ApplicationHandler.handle_deleted,
    # Payments
    "payment.processed": PaymentHandler.handle_processed,
    "payment.refunded": PaymentHandler.handle_refunded,
    # Products
    "product.created": ProductHandler.handle_created,
    "product.updated": ProductHandler.handle_updated,
}


async def dispatch(event_type: str, payload: dict, **kwargs) -> None:
    handler = EVENT_HANDLERS.get(event_type)
    if handler is None:
        return
    await handler(payload, **kwargs)
