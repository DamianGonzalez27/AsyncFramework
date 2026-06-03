"""Handlers para eventos del dominio de pagos."""

from typing import Any, Dict

from logger_tracker import logg_info, logg_error

from src.modules.payments.services.payment_service import PaymentService


class PaymentHandler:
    """Procesa eventos relacionados con pagos."""

    @staticmethod
    async def handle_processed(payload: Dict[str, Any], **kwargs) -> None:
        logg_info(f"PaymentHandler: processing payment.processed - {payload.get('id', 'unknown')}")
        service = PaymentService()
        try:
            result = service.process_payment(payload)
            logg_info(f"PaymentHandler: payment processed - id={result.get('id')}")
        except Exception as e:
            logg_error(f"PaymentHandler: error processing payment - {e}")
            raise

    @staticmethod
    async def handle_refunded(payload: Dict[str, Any], **kwargs) -> None:
        logg_info(f"PaymentHandler: processing payment.refunded - {payload.get('id', 'unknown')}")
