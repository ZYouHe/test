"""Data models for the application."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional



@dataclass
class User:
    """User model."""
    id: int
    username: str
    email: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)


    def deactivate(self) -> None:
        """Deactivate this user."""
        self.is_active = False


    def activate(self) -> None:
        """Activate this user."""
        self.is_active = True


@dataclass
class Product:
    """Product model."""
    sku: str
    name: str
    price: float
    stock: int = 0


    @property
    def is_in_stock(self) -> bool:
        return self.stock > 0

    def can_fulfill(self, quantity: int) -> bool:
        """Check if enough stock for the order."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        return self.stock >= quantity

