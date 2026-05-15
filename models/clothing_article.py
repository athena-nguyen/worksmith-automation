from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ClothingArticle:
    item: str
    service_type: str
    quantity: int
    price_per_unit: Decimal
    notes: str

    def line_total(self) -> Decimal:
        return self.quantity * self.price_per_unit
