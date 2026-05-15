from models.ticket import Ticket


def print_tickets(tickets: list[Ticket]) -> None:
    print(f"\n{'='*50}")
    print(f"  Loaded {len(tickets)} ticket(s)")
    print(f"{'='*50}")
    for ticket in tickets:
        print(f"\nTicket ID : {ticket.ticket_id}  |  Company: {ticket.company}")
        print(f"  {'Item':<20} {'Work Type':<15} {'Qty':>4} {'Unit Price':>10} {'Line Total':>10}  Notes")
        print(f"  {'-'*80}")
        for a in ticket.articles:
            print(
                f"  {a.item:<20} {a.service_type:<15} {a.quantity:>4} "
                f"${a.price_per_unit:>9.2f} ${a.line_total():>9.2f}  {a.notes}"
            )
        print(f"  {'-'*80}")
        print(f"  {'TOTAL':>52} ${ticket.total():>9.2f}")
    print()


def wait_for_login() -> None:
    input("Please log in to Worksmith in the browser, then press Enter to continue...")


def wait_for_start() -> None:
    input("Press Enter when you are ready to start the automation...")


def wait_for_close() -> None:
    input("Automation complete. Press Enter to close the browser...")
