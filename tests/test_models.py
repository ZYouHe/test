"""Tests for app.models."""

import pytest
from app.models import User, Product


class TestUser:
    """Unit tests for User model."""

    def test_create_user_with_defaults(self):
        user = User(id=1, username="alice", email="alice@test.com")
        assert user.id == 1
        assert user.username == "alice"
        assert user.email == "alice@test.com"
        assert user.is_active is True

    def test_deactivate_user(self):
        user = User(id=1, username="alice", email="alice@test.com")
        user.deactivate()
        assert user.is_active is False

    def test_activate_user(self):
        user = User(id=1, username="alice", email="alice@test.com")
        user.deactivate()
        user.activate()
        assert user.is_active is True

    def test_created_at_is_set(self):
        user = User(id=1, username="alice", email="alice@test.com")
        assert user.created_at is not None


class TestProduct:
    """Unit tests for Product model."""

    @pytest.fixture
    def product(self):
        return Product(sku="SKU-001", name="Widget", price=9.99, stock=50)

    def test_product_creation(self, product):
        assert product.sku == "SKU-001"
        assert product.price == 9.99

    def test_is_in_stock_true(self, product):
        assert product.is_in_stock is True

    def test_is_in_stock_false(self):
        product = Product(sku="SKU-002", name="Gadget", price=19.99, stock=0)
        assert product.is_in_stock is False

    def test_can_fulfill_sufficient_stock(self, product):
        assert product.can_fulfill(30) is True

    def test_can_fulfill_insufficient_stock(self, product):
        assert product.can_fulfill(100) is False

    def test_can_fulfill_exact_stock(self, product):
        assert product.can_fulfill(50) is True

    def test_can_fulfill_zero_raises(self, product):
        with pytest.raises(ValueError, match="positive"):
            product.can_fulfill(0)

    def test_can_fulfill_negative_raises(self, product):
        with pytest.raises(ValueError, match="positive"):
            product.can_fulfill(-5)