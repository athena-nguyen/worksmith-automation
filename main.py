from config import CSV_PATH
from parsing.csv_reader import read_csv
from parsing.ticket_parser import parse_tickets
from ui.terminal import print_tickets, wait_for_login, wait_for_start, wait_for_close
from browser.session import BrowserSession
from browser.worksmith import WorksmithBot


def main():
    rows = read_csv(CSV_PATH)
    tickets = parse_tickets(rows)

    print_tickets(tickets)

    with BrowserSession() as session:
        if not session.session_loaded:
            wait_for_login()
            session.save()

        wait_for_start()

        bot = WorksmithBot(session.page)
        for ticket in tickets:
            bot.edit_ticket(ticket)
        session.save()
        wait_for_close()


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        print()
        print("=" * 50)
        print("  ERROR: Spreadsheet file not found.")
        print()
        print("  Expected: data/worksmith.csv")
        print()
        print("  Add your CSV file there and try again.")
        print("=" * 50)
        print()
        raise SystemExit(1)
    except KeyboardInterrupt:
        print()
        print("Stopped by user.")
        raise SystemExit(0)
    except Exception as e:
        print()
        print("=" * 50)
        print("  ERROR: Something unexpected went wrong.")
        print()
        print(f"  Details: {e}")
        print()
        print("  Try:")
        print("   - Close Firefox and run again")
        print("   - Log in again if your session expired")
        print("   - Re-run install.py if packages seem broken")
        print("=" * 50)
        print()
        raise SystemExit(1)
