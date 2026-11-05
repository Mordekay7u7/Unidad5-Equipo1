import pytest

from src.domain import CustomerHasDebt, Order


def test_vip_discount():
    o = Order(100, vip=True)
    assert o.confirm() == 999
    assert o.status == "CONFIRMED"

def test_regular_no_discount():
    assert Order(100).confirm() == 100

def test_customer_debt():
    with pytest.raises(CustomerHasDebt):
        Order(100).confirm(customer_debt=50)
        
#Pruebas agregadas por el equipo        

def test_vip_discount_T1():
    o = Order(200, vip=True)
    assert o.confirm() == 170
    assert o.status == "CONFIRMED"
    
def test_regular_discount_T2():
    o = Order(200, vip=False)
    assert o.confirm() == 200
    assert o.status == "CONFIRMED"
    
def test_cannot_confirm_twice():
    order = Order(100)
    order.confirm()
    with pytest.raises(ValueError, match="already confirmed"):
        order.confirm()
    
@pytest.mark.parametrize("total", [0, -1])
def test_invalid_total(total):
    with pytest.raises(ValueError):
        Order(total).confirm()
