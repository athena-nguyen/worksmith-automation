from decimal import Decimal

import pytest

from parsing.ticket_parser import parse_tickets


def make_row(ticket_id="WS-001", company="Acme", item="pants", service_type="alteration",
             quantity="1", price_per_unit="22.00", notes=""):
    return {
        "ticket_id": ticket_id,
        "company": company,
        "item": item,
        "service_type": service_type,
        "quantity": quantity,
        "price_per_unit": price_per_unit,
        "notes": notes,
    }


class TestParseTickets:
    def test_single_row_produces_one_ticket_with_one_article(self):
        rows = [make_row()]
        tickets = parse_tickets(rows)

        assert len(tickets) == 1
        assert tickets[0].ticket_id == "WS-001"
        assert len(tickets[0].articles) == 1

    def test_rows_with_same_ticket_id_are_grouped_into_one_ticket(self):
        rows = [
            make_row(ticket_id="WS-001", item="pants"),
            make_row(ticket_id="WS-001", item="jacket"),
        ]
        tickets = parse_tickets(rows)

        assert len(tickets) == 1
        assert len(tickets[0].articles) == 2

    def test_rows_with_different_ticket_ids_produce_separate_tickets(self):
        rows = [
            make_row(ticket_id="WS-001"),
            make_row(ticket_id="WS-002"),
        ]
        tickets = parse_tickets(rows)

        assert len(tickets) == 2
        assert tickets[0].ticket_id == "WS-001"
        assert tickets[1].ticket_id == "WS-002"

    def test_article_fields_are_parsed_correctly(self):
        rows = [make_row(item="dress", service_type="dry_clean", quantity="3", price_per_unit="15.50", notes="handle carefully")]
        article = parse_tickets(rows)[0].articles[0]

        assert article.item == "dress"
        assert article.service_type == "dry_clean"
        assert article.quantity == 3
        assert article.price_per_unit == Decimal("15.50")
        assert article.notes == "handle carefully"

    def test_company_is_set_on_ticket(self):
        rows = [make_row(company="Globex Inc")]
        ticket = parse_tickets(rows)[0]

        assert ticket.company == "Globex Inc"

    def test_empty_notes_parsed_as_empty_string(self):
        rows = [make_row(notes="")]
        article = parse_tickets(rows)[0].articles[0]

        assert article.notes == ""

    def test_whitespace_in_fields_is_stripped(self):
        rows = [make_row(ticket_id="  WS-001  ", item="  pants  ", notes="  hem  ")]
        ticket = parse_tickets(rows)[0]

        assert ticket.ticket_id == "WS-001"
        assert ticket.articles[0].item == "pants"
        assert ticket.articles[0].notes == "hem"

    def test_empty_input_returns_empty_list(self):
        assert parse_tickets([]) == []
