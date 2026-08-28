"""Business logic services."""

from typing import Optional
from .models import User, Product


class UserService:
    """Service for user-related operations."""

    def __init__(self):
        self._users: dict[int, User] = {}
        self._next_id = 1

    def create_user(self, username: str, email: str) -> User:
        """Create a new user."""
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        if "@" not in email:
            raise ValueError("Invalid email format")

        user = User(id=self._next_id, username=username, email=email)
        self._users[self._next_id] = user
        self._next_id += 1
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self._users.get(user_id)

    def get_all_active_users(self) -> list[User]:
        """Get all active (non-deactivated) users."""
        return [u for u in self._users.values() if u.is_active]

    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user. Returns False if user not found."""
        user = self._users.get(user_id)
        if user is None:
            return False
        user.deactivate()
        return True



class OrderService:
    """Service for order-related operations."""

    def __init__(self, products: dict[str, Product]):
        self._products = products

    def calculate_total(self, items: list[tuple[str, int]]) -> float:
        """Calculate order total for list of (sku, quantity) pairs.

        Raises:
            ValueError: If a product is not found or stock is insufficient.
        """
        total = 0.0
        for sku, quantity in items:
            product = self._products.get(sku)
            if product is None:
                raise ValueError(f"Product not found: {sku}")
            if not product.can_fulfill(quantity):
                raise ValueError(f"Insufficient stock for {sku}: need {quantity}, have {product.stock}")
            total += product.price * quantity
        return round(total, 2)

