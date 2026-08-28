"""Tests for app.services."""

import pytest
from app.models import Product
from app.services import UserService, OrderService


class TestUserService:
    """Unit tests for UserService."""

    @pytest.fixture
    def service(self):
        return UserService()

    def test_create_user(self, service):
        user = service.create_user("alice", "alice@test.com")
        assert user.username == "alice"
        assert user.email == "alice@test.com"
        assert user.id == 1

    def test_create_multiple_users_ids_increment(self, service):
        u1 = service.create_user("alice", "alice@test.com")
        u2 = service.create_user("bob", "bob@test.com")
        assert u1.id == 1
        assert u2.id == 2

    def test_create_user_empty_username(self, service):
        with pytest.raises(ValueError, match="empty"):
            service.create_user("", "test@test.com")

    def test_create_user_whitespace_username(self, service):
        with pytest.raises(ValueError, match="empty"):
            service.create_user("   ", "test@test.com")

    def test_create_user_invalid_email(self, service):
        with pytest.raises(ValueError, match="email"):
            service.create_user("alice", "not-an-email")

    def test_get_user_found(self, service):
        created = service.create_user("alice", "alice@test.com")
        found = service.get_user(created.id)
        assert found is not None
        assert found.username == "alice"

    def test_get_user_not_found(self, service):
        found = service.get_user(999)
        assert found is None

    def test_get_all_active_users(self, service):
        service.create_user("alice", "alice@test.com")
        service.create_user("bob", "bob@test.com")
        service.create_user("charlie", "charlie@test.com")
        active = service.get_all_active_users()
        assert len(active) == 3

    def test_deactivate_removes_from_active(self, service):
        service.create_user("alice", "alice@test.com")
        service.create_user("bob", "bob@test.com")
        service.deactivate_user(1)
        active = service.get_all_active_users()
        assert len(active) == 1
        assert active[0].username == "bob"

    def test_deactivate_nonexistent_user(self, service):
        result = service.deactivate_user(999)
        assert result is False

    def test_deactivate_existing_user(self, service):
        service.create_user("alice", "alice@test.com")
        result = service.deactivate_user(1)
        assert result is True


class TestOrderService:
    """Unit tests for OrderService."""

    @pytest.fixture
    def products(self):
        return {
            "A": Product(sku="A", name="Item A", price=10.0, stock=100),
            "B": Product(sku="B", name="Item B", price=25.0, stock=50),
            "C": Product(sku="C", name="Item C", price=5.0, stock=0),
        }

    @pytest.fixture
    def service(self, products):
        return OrderService(products)

    def test_calculate_total_single_item(self, service):
        total = service.calculate_total([("A", 3)])
        assert total == 30.0

    def test_calculate_total_multiple_items(self, service):
        total = service.calculate_total([("A", 2), ("B", 1)])
        assert total == 45.0  # 10*2 + 25*1

    def test_calculate_total_empty_order(self, service):
        total = service.calculate_total([])
        assert total == 0.0

    def test_calculate_total_product_not_found(self, service):
        with pytest.raises(ValueError, match="not found"):
            service.calculate_total([("Z", 1)])

    def test_calculate_total_insufficient_stock(self, service):
        with pytest.raises(ValueError, match="Insufficient"):
            service.calculate_total([("C", 1)])

    def test_calculate_total_exact_stock(self, service):
        total = service.calculate_total([("A", 100)])
        assert total == 1000.0