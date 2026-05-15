from browser.session import BrowserSession

with BrowserSession() as session:
    input("Log in to Worksmith, then press Enter to save your session...")
    session.save()
    print("Done! Your session has been saved. Future runs will skip login.")
