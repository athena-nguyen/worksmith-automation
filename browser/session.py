from pathlib import Path

from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from config import SESSION_PATH, WORKSMITH_URL


class BrowserSession:
    def __init__(self):
        self._playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None
        self.session_loaded: bool = False

    def __enter__(self) -> "BrowserSession":
        self._playwright = sync_playwright().start()
        self.browser = self._playwright.firefox.launch(headless=False)

        kwargs = {}
        if SESSION_PATH.exists():
            self.session_loaded = True
            kwargs["storage_state"] = str(SESSION_PATH)

        self.context = self.browser.new_context(**kwargs)
        self.page = self.context.new_page()
        self.page.goto(WORKSMITH_URL)
        return self

    def save(self) -> None:
        SESSION_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.context.storage_state(path=str(SESSION_PATH))
        print("Session saved.")

    def __exit__(self, *_) -> None:
        pass
        # if self.context:
        #     self.context.close()
        # if self.browser:
        #     self.browser.close()
        # if self._playwright:
        #     self._playwright.stop()
