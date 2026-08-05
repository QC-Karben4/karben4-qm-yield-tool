# QM Yield Tool — Deployment Runbook (the one doc to follow)

> **This is the single, self-contained path to a live, Karben4-owned, logged-in, SharePoint-backed app.**
> It supersedes the earlier setup docs — everything you need is here (main path + Appendices A/B).
> Follow it top to bottom.
> Prepared by Keshav Shah · 2026-07-14 · Root: [[Karben4-Lauter-Yields-MOC]]
>
> Leadership/IT meeting version (value pitch + ownership/offboarding, same facts, non-technical audience):
> [[projects/Karben4-Lauter-Yields-DOE/Process/IT Setup Walkthrough — QM Yield Tool Microsoft Integration|IT Setup Walkthrough]]

**Owner tags:** 🧑‍💻 = Keshav · 🏢 = Karben4 IT/admin · 👔 = Leadership decision

---

## The order matters (read this first)

There's one dependency loop: **IT can't register the login redirect URI until the app has a
public URL, and the app gets its URL when it's first deployed.** So the sequence is:
**own the repo → deploy open → get the URL → IT registers Entra → paste secrets → verify.**
Don't try to do secrets before the app is deployed.

---

## Phase 0 — Decisions (before touching anything) 👔🏢

- [ ] **Confirm Karben4 is on Microsoft 365 / Entra** (Business/Enterprise — confirmed). 🏢
- [ ] **Agree the app's home = a Karben4 GitHub org** (not Keshav's personal account), so the app
      survives offboarding and IT can rotate secrets. 👔🏢 → *why: [[projects/Karben4-Lauter-Yields-DOE/Process/IT Setup Walkthrough — QM Yield Tool Microsoft Integration|IT Walkthrough §7]]*
- [ ] **Agree the SharePoint home for data:** which **site → document library → folder/filename**
      (e.g. `Brewing/brewery_data.xlsx`). This is the single source of truth. 👔🏢
- [ ] **Confirm Karben4's sign-in email domain** (for the login allow-list, e.g. `karben4.com`). 🏢
- [ ] **Keshav's new Karben4 account is live and signed in on this device** *before* deploying —
      it's the account you'll (a) add to the GitHub org, (b) test the login gate with in Phase 5, and
      (c) whose domain sets `allowed_domains`. 🧑‍💻

---

## Phase 1 — Put the code in a Karben4 GitHub org 🧑‍💻🏢

- [ ] 🏢 Karben4 creates/nominates a **GitHub Organization** (e.g. `karben4-brewing`), owned by a
      brewery admin (ideally a shared/service account, or ≥2 admins).
- [ ] 🧑‍💻 Create a **public** repo in that org (free Streamlit tier needs public; `.gitignore`
      already excludes `*.xlsx`, `manual_batches.json`, `.streamlit/secrets.toml` — no data leaks).
- [ ] 🧑‍💻 Push the tool from this folder:
      ```bash
      cd projects/Karben4-Lauter-Yields-DOE/Process/qm_yield_tool
      git init
      git add .
      git commit -m "QM Yield Tool — initial deploy"
      git branch -M main
      git remote add origin https://github.com/<karben4-org>/karben4-qm-yield-tool.git
      git push -u origin main
      ```
- [ ] 🧑‍💻 Confirm no secrets/workbooks got committed: `git ls-files | grep -Ei 'xlsx|secret'`
      should return **nothing**.

---

## Phase 2 — First deploy (open mode) → get the URL 🧑‍💻

Deploy with **no secrets yet** — the app runs open (no login, local file storage). This just
gets you the public URL that IT needs.

- [ ] 🧑‍💻 Go to **[share.streamlit.io](https://share.streamlit.io)** → sign in with a GitHub
      account that's a **member of the Karben4 org**.
- [ ] 🧑‍💻 **New app** → pick the org repo, branch `main`, main file **`app.py`** → **Deploy**.
- [ ] 🧑‍💻 Wait for the build, then **copy the app URL** (e.g.
      `https://karben4-qm-yield-tool.streamlit.app`). **You need this for Phase 3.**
- [ ] 🧑‍💻 Sanity check: the app loads, tabs work, "Add batch" computes. (Storage says *local only*,
      no login — expected at this stage.)

---

## Phase 3 — IT registers ONE Entra app (storage + login) 🏢

Give IT the app URL from Phase 2 and the SharePoint location from Phase 0. **One app registration
covers both** the SharePoint write-back and the login. IT does:

**A. Register + secret**
- [ ] Entra → **App registrations → New registration**, name `Karben4 QM Yield Tool`,
      **single-tenant** ("this organizational directory only").
- [ ] **Certificates & secrets → New client secret** → copy the **Value** + note expiry.

**B. SharePoint storage (app-only)**
- [ ] **API permissions →** Microsoft Graph → **Application** → add **`Sites.Selected`** →
      **Grant admin consent**.
- [ ] Grant the app **write** on the chosen site:
      ```
      POST https://graph.microsoft.com/v1.0/sites/{site-id}/permissions
      { "roles":["write"],
        "grantedToIdentities":[{"application":{"id":"{client-id}","displayName":"Karben4 QM Yield Tool"}}] }
      ```
- [ ] Get the library **Drive ID**: `GET https://graph.microsoft.com/v1.0/sites/{site-id}/drives`
      → copy the target library's `id`.

**C. Login (delegated OIDC)**
- [ ] **Authentication → Add a platform → Web**, add **both** redirect URIs:
      - `http://localhost:8501/oauth2callback` (local testing)
      - `https://<app-url>/oauth2callback` (the Phase 2 URL)
- [ ] **API permissions →** Microsoft Graph → **Delegated** → add **`openid`**, **`profile`**,
      **`email`** (grant consent if the tenant requires it).

**D. Hand back to Keshav** (secret via a secure channel, not plain email):
- [ ] **Tenant ID**, **Client ID**, **Client secret (value)**, **Drive ID**, **file path**
      (e.g. `Brewing/brewery_data.xlsx`).

---

## Phase 4 — Paste secrets into Streamlit 🧑‍💻

- [ ] 🧑‍💻 Generate a cookie secret: `python3 -c "import secrets; print(secrets.token_hex(32))"`
- [ ] 🧑‍💻 In **Streamlit Cloud → your app → ⋮ Settings → Secrets**, paste (TOML), filling every `…`:
      ```toml
      # ── SharePoint storage (app-only Graph) ──
      MS_TENANT_ID      = "…"
      MS_CLIENT_ID      = "…"
      MS_CLIENT_SECRET  = "…"
      MS_DRIVE_ID       = "…"
      # MS_DATA_ITEM_PATH — optional. Defaults in code to the real Karben4 location,
      # "Production Ops/R&D/brewery_data.xlsx". Only set it to override.

      # ── Karben4 SSO login (delegated OIDC) ──
      [auth]
      redirect_uri        = "https://<app-url>/oauth2callback"   # EXACT match to the registered URI
      cookie_secret       = "<the token_hex value above>"
      client_id           = "…"        # same Client ID as above
      client_secret       = "…"        # same Client secret as above
      server_metadata_url = "https://login.microsoftonline.com/<TENANT-ID>/v2.0/.well-known/openid-configuration"

      [karben4]
      allowed_domains = ["karben4.com"]   # Karben4's real sign-in domain(s)
      ```
- [ ] 🧑‍💻 **Save** — the app reboots. *(`Authlib` is already in `requirements.txt`, so Cloud
      installs it automatically.)*

---

## Phase 5 — Verify end-to-end 🧑‍💻

- [ ] **Login gate:** open the app URL in a private window → you get the **"Sign in with your
      Karben4 account"** screen; the app is hidden until you log in.
- [ ] **Allowed account:** log in with a Karben4 account → app loads; sidebar shows **"Signed in
      as …"** + **Log out**.
- [ ] **Rejected account** (if testable): a non-Karben4 account is refused with the restriction
      message.
- [ ] **SharePoint storage:** sidebar shows the **green "SharePoint"** badge (not amber "Local
      only"). Add a test batch → confirm it appears in **`brewery_data.xlsx` in SharePoint / Excel
      Online**, then delete it.
- [ ] **Redirect sanity:** if login errors with "redirect_uri mismatch," the `redirect_uri` secret
      and the registered Entra Web URI don't match **exactly** — fix and re-save.

---

## Phase 6 — Lock down & hand off 🧑‍💻🏢

- [ ] 🧑‍💻 Delete any earlier personal-account deployment of this app.
- [ ] 🏢 Add the **client-secret expiry** to a calendar reminder (6–24 mo) — an expired secret
      silently drops SharePoint + login back to fallback.
- [ ] 🏢 **Offboarding note** (when Keshav leaves): rotate the client secret → re-paste into
      Streamlit; remove Keshav's org + Streamlit access; re-run Phase 5.
- [ ] 🧑‍💻 Share the final URL with the QM / whoever needs it.

**Redeploys after this:** just `git push` to `main` — Streamlit Cloud auto-rebuilds. Secrets persist.

---

## Fallback behavior (nothing breaks if a piece is missing)
- No `[auth]` secrets → **app runs open** (no login).
- No `MS_*` secrets → **local-file storage** (durable only on a real disk).
- Bad/expired creds → the app **falls back** with a message; it never crashes.

---

## Appendix A — Optional: auto-read the source workbooks from SharePoint

The main path stores **hand-entered batches** in SharePoint (Phase 3B). Separately, the app can also
**auto-read the two source workbooks** (`Lauter_Checks_2.xlsx`, `Brewery_Yields.xlsx`) live instead of
the QM uploading them each session. This is **secrets-only — no extra Graph permission and no second
admin ask.**

> **Corrected 2026-08-05.** This appendix used to call for a `Files.Read.All` Application permission.
> That is **not needed.** All three files live in the **same SharePoint site** (confirmed 2026-07-22),
> and both readers hit `/drives/{drive_id}/root:/{path}:/content` ([[projects/Karben4-Lauter-Yields-DOE/Process/qm_yield_tool/onedrive.py|onedrive.py]] `fetch_file`,
> [[projects/Karben4-Lauter-Yields-DOE/Process/qm_yield_tool/sharepoint_store.py|sharepoint_store.py]] `_content_url`) — drive-scoped calls that the **Phase 3B `Sites.Selected`
> site grant already covers**. Requesting `Files.Read.All` would be tenant-wide read on every file in
> Karben4 — far more than this app needs, and a much harder sell to the admin.
>
> Only caveat: this holds while all three files stay in one site. If a source workbook moves to a
> *different* site, add a second `Sites.Selected` site grant for that site — still not `Files.Read.All`.

- [x] 🧑‍💻 **Nothing to add — the paths now default in code** (2026-08-05). Both workbooks were
      resolved against Graph to `Production Ops/R&D` in the Karben4 Brewing Home drive, and those are
      the built-in defaults in `app.py`. The live-read turns on as soon as the four credential keys
      (`MS_TENANT_ID/CLIENT_ID/CLIENT_SECRET/DRIVE_ID`) are present.
      Only set `MS_LAUTER_ITEM_PATH` / `MS_YIELDS_ITEM_PATH` to override a moved workbook.
- Effect: the sidebar switches from **Upload** buttons to **"Reading live from OneDrive/SharePoint"**
  (cached 5 min, with a Refresh button). If the fetch fails it falls back to the upload UI.

## Appendix B — Alternative host: private repo via Docker

Streamlit Cloud's free tier requires a **public** repo. If Karben4 ever needs the repo **private**,
skip Phases 1–2 and self-host the included `Dockerfile` on any container host (Render/Railway/Fly.io
~$5–10/mo private, on-prem, or Azure App Service):
```bash
docker build -t qm-yield-tool .
docker run -p 8501:8501 --env-file .env qm-yield-tool
```
`.env` holds the same `MS_*` vars; the `[auth]` login block would move to environment/secret config for
that host. Everything else in this runbook (Entra registration, verify, lock-down) is unchanged.

---

## Related
- [[Karben4-Lauter-Yields-MOC]] · [[projects/Karben4-Lauter-Yields-DOE/Process/qm_yield_tool/README|qm_yield_tool README]]
- Leadership/IT meeting version (pitch + ownership/offboarding): [[projects/Karben4-Lauter-Yields-DOE/Process/IT Setup Walkthrough — QM Yield Tool Microsoft Integration|IT Setup Walkthrough]]
