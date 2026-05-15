# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the full automation
python3 main.py

# First-time login only (saves session cookies)
python3 login.py

# Run all tests
python3 -m pytest

# Run a single test file
python3 -m pytest tests/test_models.py

# Run a single test by name
python3 -m pytest tests/test_ticket_parser.py::TestParseTickets::test_rows_with_same_ticket_id_are_grouped_into_one_ticket

# Quick CSV parse check (no browser)
python3 csv_reader_test.py
```

## Architecture

This is a terminal-driven Python Playwright automation that reads invoice CSVs and edits tickets on `https://vendors.worksmith.com`.

**Data flow:**
```
data/worksmith.csv → parsing/ → list[Ticket] → terminal preview → browser automation
```

**Key design decisions:**
- The `parsing/` package is named that (not `io/`) to avoid shadowing Python's stdlib `io` module.
- `BrowserSession` is a context manager that opens Firefox (non-headless). The `__exit__` cleanup is currently commented out during development so the browser stays open after the script ends.
- Session cookies are persisted to `session/storage_state.json`. On first run this file doesn't exist and the user logs in manually; subsequent runs load it and skip login. This file is gitignored.
- `Decimal` is used for all money fields to avoid float precision errors.

**The Worksmith ticket form uses Angular `ngRepeat`:**
Each article row is `<tr data-ng-repeat="item in vm.ticket.items">`. All fields within a row share the same `data-ng-model` names (`item.quantity`, `item.standardPricingId`, etc.), so locators must be scoped to a specific row using `.nth(i)` before calling `.locator()`. Never call `self.page.locator(field_selector)` directly for form fields — always go through a row locator first.

**WorksmithBot edit flow:**
1. `search_ticket(ticket_id)` — fills the search bar and presses Enter
2. `click_edit_button()` — waits up to 5 seconds for the Edit button; raises `PlaywrightTimeoutError` if the ticket doesn't exist
3. Loop over `ticket.articles` with `enumerate` → `fill_article_section(rows.nth(i), article)`
4. `wait_for_modal_close()` — blocks indefinitely until the user saves or closes the modal, then moves to the next ticket

**Error handling in `edit_ticket`:**
If `click_edit_button()` times out (ticket ID not found in Worksmith), the exception is caught, a skip message is printed, and the bot continues to the next ticket. `PlaywrightTimeoutError` is imported from `playwright.sync_api`.

**`fill_article_section` field selectors (confirmed from live HTML):**

| Field | Selector | Notes |
|---|---|---|
| Article dropdown | `[data-ng-model="item.standardPricingId"]` | Select `""` for "Other" |
| Quantity | `[data-ng-model="item.quantity"]` | |
| Unit price | `[ng-model="item.unitWholesalePrice"]` | May be disabled until "Other" is selected |
| Notes | `[data-ng-model="item.description"]` | textarea |
| Service type | `[data-ng-model="item.lineItemType"]` | Only present when `item.standardPricingId` is unset (i.e. "Other" selected); values are objects, select by matching `.id` |

The conditional item-name text input that appears after selecting "Other" is not yet implemented — its selector is still pending HTML inspection.

**Row count mismatch edge case (implemented):**
The CSV is the source of truth. The Worksmith ticket form is pre-filled by the company and may have fewer rows than the CSV specifies. Before filling each row, `edit_ticket` checks `if i >= rows.count()` and calls `click_add_article_button()` to create the missing row, then waits for it to appear. Playwright locators are live, so `rows.count()` re-evaluates automatically after each add.

The "Add Article of Clothing" button selector: `[data-ng-click="vm.addItem()"]`

## Distribution Scripts

Two cross-platform Python scripts are included for handing the tool off to a non-technical user (Mac or Windows):

- **`install.py`** — one-time setup. Creates `.venv/`, installs `requirements.txt`, and runs `playwright install firefox`. The user runs this once with their system Python (`python3 install.py` on Mac, `python install.py` on Windows).
- **`run.py`** — daily driver. Guards for missing `.venv/` and missing `data/worksmith.csv`, then delegates to the venv Python to run `main.py`. The user runs this every day.

`main.py` wraps the `main()` call in a try/except that catches `FileNotFoundError`, `KeyboardInterrupt`, and unexpected exceptions, printing plain-English messages instead of raw tracebacks. This is a safety net for when the user runs `main.py` directly — `run.py` also has its own shell-level guards.

`README.md` documents the full setup and daily-use workflow for a non-technical user.

## CSV Format

`data/worksmith.csv` — one row per clothing article, rows sharing a `ticket_id` are grouped into one `Ticket`:

```
company,ticket_id,item,service_type,quantity,price_per_unit,notes
```
