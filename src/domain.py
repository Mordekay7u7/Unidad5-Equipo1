# from dataclasses import dataclass

# class CustomerHasDebt(Exception):
#     pass

# @dataclass
# class Order:
#     total: float
#     vip: bool = False
#     status: str = "NEW"
#     discount: float = 0.0

#     def confirm(self, customer_debt=0):
#         if self.status == "CONFIRMED":
#             raise ValueError("already confirmed")

#         if self.total <= 0:
#             raise ValueError("total must be positive")
#         if customer_debt > 0:
#             raise CustomerHasDebt("outstanding debt")
#         self.discount = round(self.total * 0.15, 2) if self.vip else 0.0
#         self.status = "CONFIRMED"
#         return self.total - self.discount
    
#Rafactor

from dataclasses import dataclass


class CustomerHasDebt(Exception):
    """Excepción lanzada cuando el cliente tiene una deuda pendiente."""

@dataclass
class Order:
    total: float
    vip: bool = False
    status: str = "NEW"
    discount: float = 0.0

    def confirm(self, customer_debt: float = 0) -> float:
        """Confirma el pedido, aplica descuentos y retorna el importe final a pagar."""
        self._validate_confirmation_eligibility(customer_debt)
        
        self.discount = self._calculate_discount()
        self.status = "CONFIRMED"
        return self.total - self.discount

    def _validate_confirmation_eligibility(self, customer_debt: float) -> None:
        """Valida que el pedido y el cliente cumplan las reglas para confirmación."""
        if self.status == "CONFIRMED":
            raise ValueError("already confirmed")

        if self.total <= 0:
            raise ValueError("total must be positive")

        if customer_debt > 0:
            raise CustomerHasDebt("outstanding debt")

    def _calculate_discount(self) -> float:
        """Calcula el descuento aplicable según el tipo de cliente."""
        return round(self.total * 0.15, 2) if self.vip else 0.0
