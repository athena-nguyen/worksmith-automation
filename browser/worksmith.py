from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from models.ticket import Ticket


class WorksmithBot:
    def __init__(self, page: Page):
        self.page = page

    def edit_ticket(self, ticket: Ticket) -> None:
        print(f"Searching for ticket {ticket.ticket_id}...")
        self.search_ticket(ticket.ticket_id)
        print("Clicking edit button...")
        try:
            self.click_edit_button()
        except PlaywrightTimeoutError:
            print(f"  Ticket {ticket.ticket_id} not found in system, skipping.")
            return

        rows = self.page.locator('tr[data-ng-repeat="item in vm.ticket.items"]')
        rows.first.wait_for(state="visible")

        for i, article in enumerate(ticket.articles):
            if i >= rows.count():
                self.click_add_article_button()
                rows.nth(i).wait_for(state="visible")
            print(f"  Filling row {i}: {article.item} / {article.service_type}...")
            self.fill_article_section(rows.nth(i), article)

        print("  All rows filled. Review the ticket, then save or close it to continue.")
        self.wait_for_modal_close()
        print(f"Ticket {ticket.ticket_id} done.")

    def search_ticket(self, ticket_id: str) -> None:
        search_bar = self.page.locator('[data-ng-model="pagination.filter.ticketNumber"]')
        search_bar.fill(ticket_id)
        search_bar.press("Enter")

    def click_edit_button(self) -> None:
        self.page.locator('[data-ng-click="openTicketModal(ticket)"]').click(timeout=5000)

    def fill_article_section(self, row, article) -> None:
        # Change article of clothing to "Other" to enable editing the rest of the fields
        row.locator('[data-ng-model="item.standardPricingId"]').select_option("")

        # Fill description to the article of clothing, which is required to save the ticket.
        row.locator('[data-ng-model="item.title"]').fill(str(article.item))

        # Fill service type dropdown, which is required to save the ticket.
        row.locator('[data-ng-model="item.lineItemType"]').select_option(label=article.service_type)

        row.locator('[data-ng-model="item.quantity"]').fill(str(article.quantity))
        row.locator('[ng-model="item.unitWholesalePrice"]').fill(str(article.price_per_unit))
        row.locator('[data-ng-model="item.description"]').fill(article.notes)

    def click_add_article_button(self) -> None:
        self.page.locator('[data-ng-click="vm.addItem()"]').click()

    def wait_for_modal_close(self) -> None:
        # timeout=0 waits indefinitely — the user decides when to save or close
        self.page.wait_for_selector('[data-ng-click="vm.close()"]', state="hidden", timeout=0)
