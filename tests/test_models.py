from decimal import Decimal

import pytest

from models.clothing_article import ClothingArticle
from models.ticket import Ticket


def make_article(item="pants", service_type="alteration", quantity=1, price_per_unit="22.00", notes=""):
    return ClothingArticle(
        item=item,
        service_type=service_type,
        quantity=quantity,
        price_per_unit=Decimal(price_per_unit),
        notes=notes,
    )


class TestClothingArticle:
    def test_line_total_is_quantity_times_price(self):
        # Arrange
        article = make_article(quantity=3, price_per_unit="15.00")

        # Act
        result = article.line_total()

        # Assert
        assert result == Decimal("45.00")

    def test_line_total_single_unit(self):
        article = make_article(quantity=1, price_per_unit="22.00")
        assert article.line_total() == Decimal("22.00")

    def test_line_total_uses_exact_decimal_arithmetic(self):
        # Floats would give imprecise results here — Decimal should not
        article = make_article(quantity=3, price_per_unit="0.10")
        assert article.line_total() == Decimal("0.30")


class TestTicket:
    def test_total_sums_all_line_totals(self):
        # Arrange
        ticket = Ticket(
            ticket_id="WS-001",
            company="Acme",
            articles=[
                make_article(quantity=1, price_per_unit="22.00"),  # 22.00
                make_article(quantity=2, price_per_unit="15.00"),  # 30.00
            ],
        )

        # Act
        result = ticket.total()

        # Assert
        assert result == Decimal("52.00")

    def test_total_with_single_article(self):
        ticket = Ticket(
            ticket_id="WS-001",
            company="Acme",
            articles=[make_article(quantity=1, price_per_unit="30.00")],
        )
        assert ticket.total() == Decimal("30.00")

    def test_total_with_no_articles_is_zero(self):
        ticket = Ticket(ticket_id="WS-001", company="Acme", articles=[])
        assert ticket.total() == Decimal("0")
