from dataclasses import dataclass, field
from decimal import Decimal

from models.clothing_article import ClothingArticle


@dataclass
class Ticket:
    ticket_id: str
    company: str
    articles: list[ClothingArticle] = field(default_factory=list)

    def total(self) -> Decimal:
        return sum((a.line_total() for a in self.articles), Decimal("0"))
