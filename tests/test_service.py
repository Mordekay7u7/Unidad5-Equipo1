from unittest.mock import Mock

import pytest

from src.application import OrderService
from src.domain import Order


def test_gateway_approved():
    gateway = Mock()
    gateway.charge.return_value = True
    assert OrderService(gateway).checkout(Order(100)) == 100
    gateway.charge.assert_called_once_with(100)

def test_gateway_rejected():
    gateway = Mock()
    gateway.charge.return_value = False
    with pytest.raises(RuntimeError):
        OrderService(gateway).checkout(Order(100))

def test_vip_payment_rejected():
    # Arrange: Pedido VIP de $200 (descuento del 15% da $170 a cobrar)
    order = Order(200, vip=True)
    gateway = Mock()
    gateway.charge.return_value = False  # Simular pago rechazado

    # Act & Assert: Verificar que el intento de cobro fue por $170 y se lanza RuntimeError
    with pytest.raises(RuntimeError):
        OrderService(gateway).checkout(order)
    
    gateway.charge.assert_called_once_with(170)