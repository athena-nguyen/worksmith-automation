# Worksmith Automation

Automatically fills your Worksmith tickets from a spreadsheet.

---

## Before You Start (One-Time)

You need **Python 3** installed on your computer.

**Mac** — open Terminal and type:
```
python3 --version
```

**Windows** — open Command Prompt and type:
```
python --version
```

If you see `Python 3.x.x` you are ready. If you get an error, download Python 3 from [python.org/downloads](https://www.python.org/downloads/), install it, then come back here.

---

## First-Time Setup (Run Once)

Open Terminal (Mac) or Command Prompt (Windows).

**1. Go to the project folder:**

Mac:
```
cd ~/Documents/worksmith-automation
```

Windows (adjust the path to where you saved the folder):
```
cd C:\Users\YourName\Documents\worksmith-automation
```

**2. Run the setup script:**

Mac:
```
python3 install.py
```

Windows:
```
python install.py
```

This will take a few minutes — it downloads the Firefox browser used by the automation. Wait until you see **"Setup complete!"** before moving on.

**That's it for setup.** The first time you run the automation it will ask you to log in to Worksmith — see below.

---

## Every Day: Running the Automation

### Step 1 — Update your spreadsheet

Open the file at:
```
worksmith-automation / data / worksmith.csv
```

Edit it with your tickets for today. **Save and close the file before running the automation.**

The columns are:

| Column | What to enter |
|---|---|
| `company` | Client company name (e.g. `Loro Piana`) |
| `ticket_id` | Worksmith ticket number (e.g. `WS560018`) |
| `item` | Article of clothing (e.g. `Shirt`, `Pant`, `Jacket`) |
| `service_type` | Type of work (e.g. `Alteration`, `Dry Clean`, `Laundered`) |
| `quantity` | Number of items (e.g. `1`) |
| `price_per_unit` | Price for one item — numbers only, no $ sign (e.g. `40`) |
| `notes` | Extra notes, or leave blank |

Multiple rows with the same `ticket_id` are grouped into one ticket automatically.

### Step 2 — Run the automation

Mac:
```
python3 run.py
```

Windows:
```
python run.py
```

Firefox will open and fill in your tickets. For each ticket, the automation will pause so you can review the changes and save the ticket yourself before it moves on.

**First run only:** Firefox will open and you will be logged out of Worksmith. Log in normally, then come back to the terminal and press **Enter**. Your session will be saved so you won't need to log in again.

---

## If Something Goes Wrong

| What you see | What to do |
|---|---|
| "Spreadsheet file not found" | Make sure `data/worksmith.csv` exists and is in the right folder |
| "Setup has not been run yet" | Run `python3 install.py` (Mac) or `python install.py` (Windows) first |
| Firefox opens but you're not logged in | Log in normally and press Enter in the terminal |
| "not found in system, skipping" | That ticket ID doesn't exist in Worksmith — check the number |
| The script stops unexpectedly | Close Firefox, check your CSV is saved and closed, then run again |
| Packages seem broken | Re-run `python3 install.py` / `python install.py` |

---

## File Locations

```
worksmith-automation/
├── data/
│   └── worksmith.csv    <-- YOUR SPREADSHEET (edit this daily)
├── install.py           — Run once during first-time setup
├── run.py               — Run this every day
└── session/             — Your saved login (do not touch)
```
