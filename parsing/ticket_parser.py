from decimal import Decimal

from models.clothing_article import ClothingArticle
from models.ticket import Ticket


def parse_tickets(rows: list[dict]) -> list[Ticket]:
    tickets: dict[str, Ticket] = {}

    for row in rows:
        ticket_id = row["ticket_id"].strip()
        article = ClothingArticle(
            item=row["item"].strip(),
            service_type=row["service_type"].strip(),
            quantity=int(row["quantity"].strip()),
            price_per_unit=Decimal(row["price_per_unit"].strip()),
            notes=row["notes"].strip(),
        )
        if ticket_id not in tickets:
            tickets[ticket_id] = Ticket(ticket_id=ticket_id, company=row["company"].strip())
        tickets[ticket_id].articles.append(article)

    return list(tickets.values())
