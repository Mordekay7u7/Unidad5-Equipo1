from datetime import UTC, datetime, timedelta

from src.security import can_cancel


def test_owner_within_24h():
    now = datetime.now(UTC)
    assert can_cancel("NEW", 1, 1, False, now - timedelta(hours=1), now)

def test_stranger_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 2, False, now, now)

def test_shipped_denied_even_admin():
    now = datetime.now(UTC)
    assert not can_cancel("SHIPPED", 1, 1, True, now, now)

def test_expired_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 1, False, now - timedelta(hours=25), now)



def test_admin_can_cancel_other_user_order():
    now = datetime.now(UTC)
    # Administrador (is_admin=True) cancela pedido "NEW" del usuario owner_id=1 siendo user_id=2
    assert can_cancel("NEW", owner_id=1, user_id=2, is_admin=True, created_at=now, now=now)

def test_owner_at_exactly_24h_denied():
    now = datetime.now(UTC)
    # Propietario intenta cancelar exactamente a las 24 horas transcurridas
    assert not can_cancel("NEW", owner_id=1, user_id=1, is_admin=False, created_at=now - timedelta(hours=24), now=now)