"""Karben4 SSO login gate for the Streamlit app.

Uses Streamlit's native OIDC auth (st.login / st.user / st.logout, stable since
Streamlit 1.42) pointed at Microsoft Entra. The gate only activates when the
[auth] section is present in secrets — otherwise the app runs OPEN, exactly as it
did before (so local dev and any un-configured deploy are unchanged).

This is a SEPARATE credential from the app-only Graph creds in onedrive.py /
sharepoint_store.py:
  • those use client-credentials (the app acts as itself, no human) to read/write
    the SharePoint workbook;
  • this uses a user sign-in (delegated OIDC) so a person logs in with their
    Karben4 Microsoft 365 account before they can see the app.

A single-tenant Entra app registration already limits sign-in to the Karben4
tenant; the optional allowed-domains check below is belt-and-suspenders (and also
filters out guest accounts invited into the tenant on other domains).

Config — in .streamlit/secrets.toml locally, or Streamlit Cloud → Settings → Secrets:

    [auth]
    redirect_uri        = "https://<your-app>.streamlit.app/oauth2callback"
    cookie_secret       = "<a long random string>"
    client_id           = "<Entra app (client) id>"
    client_secret       = "<Entra app client secret value>"
    server_metadata_url = "https://login.microsoftonline.com/<tenant-id>/v2.0/.well-known/openid-configuration"

    # Optional. Restrict to one or more email domains. Unset → any user the Entra
    # app admits is allowed (a single-tenant app already limits to the org).
    [karben4]
    allowed_domains = ["karben4.com"]

See DEPLOYMENT_RUNBOOK.md (Phase 3C / Phase 4) for the one-time Entra steps.
"""
import streamlit as st

_AUTH_KEYS = ("redirect_uri", "cookie_secret", "client_id", "client_secret", "server_metadata_url")


def _secrets_section(name: str) -> dict:
    """A secrets subsection as a plain dict, or {} if absent — never raises even when
    no secrets.toml exists at all (fresh local checkout, un-configured deploy)."""
    try:
        return dict(st.secrets.get(name, {}))
    except Exception:
        return {}


def is_configured() -> bool:
    """True only when [auth] carries every OIDC essential — otherwise the gate stays
    off and the app runs open (unchanged behavior)."""
    auth = _secrets_section("auth")
    return all(auth.get(k) for k in _AUTH_KEYS)


def _allowed_domains() -> list[str]:
    doms = _secrets_section("karben4").get("allowed_domains", [])
    if isinstance(doms, str):          # tolerate a single string instead of a list
        doms = [doms]
    return [str(d).lower().lstrip("@") for d in doms if d]


def _user_email():
    """Best-effort email/UPN from the ID-token claims. Entra populates `email` when a
    mailbox exists, else `preferred_username` / `upn` carry the user@domain UPN."""
    for key in ("email", "preferred_username", "upn"):
        try:
            val = st.user.get(key)
        except Exception:
            val = getattr(st.user, key, None)
        if val:
            return str(val)
    return None


def _domain_ok(email) -> bool:
    doms = _allowed_domains()
    if not doms:
        return True                    # no restriction configured
    if not email or "@" not in email:
        return False
    return email.rsplit("@", 1)[-1].lower() in doms


def _login_screen():
    import theme  # local import keeps auth.py importable without the theme module
    st.markdown(theme.HEX_RULE_HTML, unsafe_allow_html=True)
    st.title("Karben4 QM Yield Tool")
    st.subheader("Sign in with your Karben4 account")
    st.write(
        "This tool is restricted to Karben4 staff. Log in with your Microsoft 365 "
        "(Karben4) account to continue."
    )
    st.button("Log in with Microsoft", on_click=st.login, type="secondary")


def _rejected_screen(email):
    st.title("Karben4 QM Yield Tool")
    doms = ", ".join(_allowed_domains()) or "Karben4"
    st.error(
        f"**Access restricted to {doms} accounts.** "
        f"The account `{email or '(unknown)'}` isn't permitted here."
    )
    st.button("Log out and try another account", on_click=st.logout, type="secondary")


def require_login():
    """Gate the app behind Karben4 SSO when configured.

    Returns a small dict describing the signed-in user, or None when auth isn't
    configured (open mode). Halts the script via st.stop() for anyone not signed in
    or outside the allowed domain — so callers can treat a returned value as "access
    granted" and everything after it renders only for authorized users."""
    if not is_configured():
        return None                    # open mode — unchanged behavior

    if not st.user.is_logged_in:
        _login_screen()
        st.stop()

    email = _user_email()
    if not _domain_ok(email):
        _rejected_screen(email)
        st.stop()

    name = None
    try:
        name = st.user.get("name")
    except Exception:
        name = getattr(st.user, "name", None)
    return {"name": name or email, "email": email}


def sidebar_account(user):
    """Signed-in identity + a Log out button in the sidebar. No-op in open mode."""
    if not user:
        return
    st.sidebar.divider()
    st.sidebar.caption(f"Signed in as **{user['name']}**")
    if user.get("email") and user["email"] != user["name"]:
        st.sidebar.caption(f"`{user['email']}`")
    st.sidebar.button("Log out", on_click=st.logout, use_container_width=True)
