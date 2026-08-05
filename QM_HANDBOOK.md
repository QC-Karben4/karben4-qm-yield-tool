# Karben4 QM Yield Tool — Quality Manager's Handbook

**Install · Daily use · Updates · Troubleshooting**

Version 2.0 · 2026-08-05 · Prepared by Keshav Shah
Questions: Keshav Shah — Quality / Process Engineering

> **To print:** open in Obsidian → **⋮ (top-right) → Export to PDF** → print that.
> Sections are ordered so you can print just Part 1 for install day, or just Part 5 for the wall.

---

## Contents

1. **What this tool is** — page 1
2. **How to run it** — the web link (and the optional local install)
3. **Part 1 — One-time install** (Windows, ~10 min — *optional*)
4. **Part 2 — Daily use** (starting, the tabs, entering a batch)
5. **Part 3 — Your data** (where it lives, backups, exports)
6. **Part 4 — Updating to a newer version**
7. **Part 5 — Troubleshooting**
8. **Part 6 — Quick reference card** (print this one separately)

---

## 1. What this tool is

The **Karben4 QM Yield Tool** computes brewhouse and lauter yield numbers for a batch —
efficiency, lauter loading, mash thickness, volume cascade — from the two existing
spreadsheets plus anything you type in by hand.

**What it's for:**
- Getting computed yield numbers for a batch without hand-calculating them.
- Seeing trends across batches for recipe formulation.
- Spotting how efficiency moves with lauter loading and mash thickness.
- Producing a **transcription card** — the computed values formatted to copy into paper
  brewlogs and Ekos.

**What it is *not*:**
- **Brewers do not use this.** It's a single-user analysis tool for the QM. Results are read
  here, then transcribed by hand into the brewlogs and Ekos.
- It does not write to Ekos, and it does not change any brewery system.
- It is not the system of record. The spreadsheets and Ekos remain the record.

**Nothing you do in this tool can affect a brew in progress.** It only reads and computes.

---

## 2. How to run it

### The web link — this is what you want

**https://karben4-qm-yield-tool.streamlit.app/**

- Sign in with your **Karben4 Microsoft 365 account** (same login as your email).
- Both spreadsheets load automatically from SharePoint — nothing to upload.
- **Your typed-in batches save permanently** to Karben4's SharePoint, in the same
  `Production Ops/R&D` folder as the source spreadsheets. They're there tomorrow, next month, and
  from any computer you sign in on.
- Nothing to install. Works from any machine, including one that isn't yours.

That's it — you can stop reading here and start using the tool. Parts 3 and 4 below are only for
people who want it installed locally.

> ⏳ **If it looks stuck on first open, wait.** When nobody has used the link for a while, the app
> goes to sleep and takes **up to 2 minutes** to wake up — you'll see a spinner or a pie-slice icon.
> If it's still spinning after that, reload the page once. This is normal and only happens on the
> first open of the day.

### Installing it on your computer — optional

Part 3 walks through it. Worth doing only if you want to work **offline**, need the tool when the
network or SharePoint is down, or are testing changes.

The trade-off: a local install keeps your batches in a file **on that one computer** instead of in
SharePoint. That means it's yours alone, it isn't backed up by Karben4, and batches you enter there
won't appear on the web link. **If you use both, they keep separate histories.** Pick one as your
main and stick with it.

---

<div style="page-break-after: always;"></div>

## Part 1 — One-time install (Windows) — *optional*

> Only if you need offline access (see section 2). For everyday use, the web link needs none of this.

Do this once. About 10 minutes, most of it waiting on downloads.

### Step 1 — Install Python

1. Go to **https://www.python.org/downloads/** and click the big **Download Python 3.x** button.
2. Run the file it downloads.
3. **On the very first screen, check the box at the bottom: "Add python.exe to PATH."**
   ⚠️ **This is the one step people miss, and skipping it breaks Step 4.** If you're unsure
   whether you checked it, see Troubleshooting → *"python is not recognized."*
4. Click **Install Now**, then **Close** when it finishes.

### Step 2 — Download the tool

1. Go to **https://github.com/QC-Karben4/karben4-qm-yield-tool**
2. Click the green **`< > Code`** button → **Download ZIP**.
3. Find `karben4-qm-yield-tool-main.zip` in your **Downloads** folder.
   Right-click it → **Extract All…** → **Extract**.
4. Move the extracted **`karben4-qm-yield-tool-main`** folder somewhere permanent —
   your **Documents** folder is a good choice.

> ⚠️ **Your saved batch data will live inside this folder.** Once you start using the tool,
> don't delete, rename, or move it. If you must move it, move the whole folder intact.

### Step 3 — Open a command window inside the folder

1. Open the `karben4-qm-yield-tool-main` folder in File Explorer.
2. Click the **address bar** at the top (the strip showing the folder path).
3. Type **`cmd`** and press **Enter**.

A black command window opens, already pointed at the right folder. *(If you open a command
window any other way, it will be pointed somewhere else and the next steps won't work.)*

### Step 4 — Install the tool's components

In that black window, type each line and press **Enter**. Wait for each to finish before
typing the next.

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

The last line downloads what the tool needs. **It takes a few minutes the first time** and
prints a lot of text — that's normal. You're done when it stops and shows the prompt again.

*(After the second line, you'll see `(.venv)` at the start of the prompt line. That's the
sign it worked.)*

### Step 5 — Start it

```
streamlit run app.py
```

The tool opens by itself in your web browser at **http://localhost:8501**.

**That's it — you're running.** Nothing further to install, ever.

---

<div style="page-break-after: always;"></div>

## Part 2 — Daily use

### Starting the tool (every time)

1. Open the `karben4-qm-yield-tool-main` folder, click the **address bar**, type `cmd`, press **Enter**.
2. Type these two lines:

```
.venv\Scripts\activate
streamlit run app.py
```

> **Leave the black window open** the whole time you're using the tool. Closing it stops the tool.
> You can minimize it.

### Stopping the tool

1. Close the browser tab.
2. Click the black command window and press **Ctrl + C**.

### The tabs

| Tab | What it's for |
|---|---|
| **Add batch** | Type in a batch's numbers. Your main data-entry screen. |
| **Model** | The brewhouse constants the math runs on. Don't change these unless you and Keshav have agreed to. |
| **Trends** | Aggregate trends across batches — for recipe formulation. |
| **Levers** | Efficiency vs. lauter loading and vs. mash thickness. The core yield question. |
| **By beer** | Everything broken out per beer. |
| **Re-fit** | Re-fits the lauter-curve parameters on current data. |
| **Transcription card** | One batch's computed values, formatted to copy into paper brewlogs / Ekos. |
| **Manage manual batches** | Review or delete batches you typed in. |
| **Data** | The full table, one row per batch. Download buttons live here. |

### Entering a batch

**Add batch** tab → fill in → **Save batch** at the bottom.

You can save a batch before it ever lands in a spreadsheet — you don't have to wait.

**Always filled in:**
- Beer *(pick from the list, or choose to type a new beer name)*
- Batch Number
- Brew date
- Strike water temp (°F)
- Strike water vol (gal)
- Lauter runoff vol (bbl)
- Lauter runoff extract (°P)

**Optional — tick "Add knockout (Brewhouse) data" to show:**
- End-of-boil extract (°P)
- Kettle/whirlpool hops (lb)
- Sugar additions (lb): Brewers Crystals, Sucrose, DME, Lactose, Dextrose, Maltodextrin

**Optional — tick "Add cellar data" to show:**
- Effective FV wort vol (bbl)
- Effective FV wort OG (°P)
- Centrifuge vol out, actual (bbl) *— optional*
- Packaged vol (bbl) *— optional*
- Dry hops (lb)

> A **live preview** of the computed loading and thickness appears as you type, before you save
> — use it to catch a typo (a decimal in the wrong place shows up immediately as a wild number).

**There is no separate save or export step.** Clicking **Save batch** writes it to your data
file straight away.

---

<div style="page-break-after: always;"></div>

## Part 3 — Your data

### Where it lives

**On the web link (normal use):** in Karben4's SharePoint, at
`Production Ops/R&D/brewery_data.xlsx` — the same folder as `Lauter_Checks_2.xlsx` and
`Brewery_Yields.xlsx`. It's a normal Excel file; you can open it in Excel Online to look. It's
covered by Karben4's normal SharePoint backup, so there's nothing for you to do.

The sidebar tells you which storage you're on: a green **SHAREPOINT** badge means saved permanently.
An amber **LOCAL ONLY** badge means you're on a local install (or something's wrong — see below).

**On a local install:** `brewery_data.xlsx` inside the `karben4-qm-yield-tool-main` folder.

That file *is* your saved history. It's a normal Excel file — you can open it directly in Excel
to look, though you should do your **editing through the tool** so the numbers stay consistent.

*(If you're using the web link instead, there is no such file and nothing persists — see Part 2 of
section 2.)*

### Back it up

**On the web link: nothing to do.** It's in SharePoint, backed up like any other company file.

**On a local install: copy `brewery_data.xlsx` somewhere else every so often** — OneDrive or a USB
drive, once a month, more after a big data-entry session. This is the one genuine risk of running
locally: the file lives on a single computer, and if it dies without a copy, that history is gone.

### Getting data out

**Data** tab → **Download Excel (.xlsx)** or **Download CSV**.

That's a full computed snapshot — every batch with all calculated values — for sharing, reporting,
or archiving. The **Re-fit** tab has its own **Download fitted params (CSV)** button.

---

## Part 4 — Updating to a newer version

When Keshav tells you there's a new version:

1. Download the ZIP again (Part 1, Step 2) and extract it into a **new** folder — leave the old one alone.
2. **Copy `brewery_data.xlsx` from the old folder into the new folder.**
   ⚠️ **Don't skip this — this is your history.** Do it before you start using the new folder.
3. Repeat Steps 3, 4 and 5 in the new folder.
4. Use the new folder from then on. Once you've confirmed your batches are all there, you can
   delete the old folder.

*(Using the web link? It updates itself. Nothing to do.)*

---

<div style="page-break-after: always;"></div>

## Part 5 — Troubleshooting

| What you see | What it means | Fix |
|---|---|---|
| **`'python' is not recognized…`** | Python wasn't added to PATH during install. | Re-run the Python installer → choose **Modify** → make sure **"Add python.exe to PATH"** is checked. Or reinstall and check the box on the first screen. Then close the black window, open a new one, and redo Step 4. |
| **`'streamlit' is not recognized…`** | You skipped the `.venv\Scripts\activate` line, or the `pip install` in Step 4 didn't finish. | Run `.venv\Scripts\activate` first (you should see `(.venv)` appear), then `pip install -r requirements.txt` again. |
| **Browser didn't open** | The tool is running fine, it just didn't launch the browser. | Open your browser yourself and go to **http://localhost:8501**. |
| **Page won't load / "can't reach this page"** | The tool isn't running — the black window was closed or Ctrl+C was pressed. | Start it again (Part 2). |
| **Amber "LOCAL ONLY" badge on the web link** | Not expected — the web link should show green SHAREPOINT. The connection dropped to fallback, usually an expired credential. | Your batches are **not** being saved permanently. Stop entering data, use **Data → Download Excel** to save what's on screen, and tell Keshav. |
| **Spinner for a minute or two on first open** | The app was asleep. | Wait up to 2 minutes, then reload once. Normal for the first open of the day. |
| **Web link: "Sign in with your Karben4 account"** | Expected — the web version requires your M365 login. | Sign in with your normal Karben4 email account. If it refuses your account, contact Keshav. |
| **Batches I typed are missing** | Most likely you entered them on a *local install* and are now looking at the web link (or vice versa) — the two keep separate histories. | Check the sidebar badge to see which storage you're on. If it says SHAREPOINT and data is genuinely missing, tell Keshav — don't re-enter it yet. |
| **A number looks obviously wrong** | Usually a typo in an entered value (decimal place), or a wrong unit — check gal vs. bbl, °F vs. °C. | Find the batch under **Manage manual batches**, delete it, re-enter it. Watch the live preview as you type. |
| **Nothing above works** | — | Close the black window entirely, open a fresh one from the folder (Part 1, Step 3), and start again from `.venv\Scripts\activate`. If it still fails, contact Keshav — include a photo of the black window's text. |

> **The safe move for anything you're unsure about:** close the browser tab, press **Ctrl + C** in
> the black window, and start over. Nothing in this tool can be broken by restarting it, and your
> saved data is untouched by it.

---

<div style="page-break-after: always;"></div>

## Part 6 — Quick reference card

*Print this page and keep it near the computer.*

### Start it
> Open `karben4-qm-yield-tool-main` → click address bar → type `cmd` → Enter
> ```
> .venv\Scripts\activate
> streamlit run app.py
> ```

### Stop it
> Close browser tab → click black window → **Ctrl + C**

### If the browser doesn't open
> Go to **http://localhost:8501**

### Everyday use — the web link
> **https://karben4-qm-yield-tool.streamlit.app/** — Karben4 M365 login
> Saves permanently · spreadsheets load themselves · slow first open is normal

### Your data
> Web link → saved in SharePoint, `Production Ops/R&D/brewery_data.xlsx`, nothing to back up
> Local install → `brewery_data.xlsx` in the tool's folder — **you** back that one up

### Enter a batch
> **Add batch** tab → fill in → **Save batch**. Saves immediately, no export step.

### Get data out
> **Data** tab → **Download Excel** / **Download CSV**

### Two things to watch
> ✅ Sidebar badge should read green **SHAREPOINT** on the web link
> ❌ Don't move or rename the folder if you installed it locally

### Help
> Keshav Shah — include a photo of the black command window if something errored.

---

## Related

- [README.md](README.md) — technical overview of the tool
- [SETUP.md](SETUP.md) — the short local-install guide this expands on
- [DEPLOYMENT_RUNBOOK.md](DEPLOYMENT_RUNBOOK.md) — deployment/admin side (not for the QM)
