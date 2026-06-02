"""Servicio de ejemplo para el módulo de pagos."""

from typing import Dict, Any, Optional


class PaymentService:
    def __init__(self, repository: Optional[Any] = None):
        self.repository = repository

    def process_payment(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        payment = {
            "id": payload.get("id", "payment-0001"),
            "status": "processed",
            "amount": payload.get("amount", 0),
        }
        if self.repository is not None:
            self.repository.save(payment)
        return payment
