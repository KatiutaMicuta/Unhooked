import base64
from pathlib import Path

import streamlit as st

from src.url_analyzer import url_analysis
from src.email_analyzer import email_analysis, extract_links

LOGO = Path(__file__).parent / "assets" / "logo.png"
# The square version reads better as a browser-tab icon than the wide wordmark.
ICON = Path(__file__).parent / "assets" / "logo-original.png"
LOGO_WIDTH = 320  # on-screen width in pixels — change this to resize the logo
CURSOR = Path(__file__).parent / "assets" / "cursor.png"

# --- edit me -----------------------------------------------------------------
# Your own words go here. Say plainly what the tool looks at.
DESCRIPTION = (
    "Paste a link or an email and Unhooked will check it for the tricks phishing uses: undercover email addresses, links that don't go where they say they go, and phrases made to panic you."
)
# -----------------------------------------------------------------------------

PINK_BUTTONS = """
<style>
.stButton > button[kind="primary"] {
    background-color: #F6C3D6;
    color: #40262F;
    border: 1px solid #E7A5BF;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[kind="primary"]:focus {
    background-color: #EFAEC8;
    color: #40262F;
    border: 1px solid #DC90AF;
}
</style>
"""


def fishing_cursor_css():
    """A 🎣 cursor everywhere, except text fields which keep the typing caret."""
    if not CURSOR.exists():
        return ""

    encoded = base64.b64encode(CURSOR.read_bytes()).decode()
    url = f'url("data:image/png;base64,{encoded}") 4 4, auto'
    return f"""
<style>
html, body, .stApp, .stApp * {{ cursor: {url}; }}
input, textarea {{ cursor: text; }}
</style>
"""


def verdict(score):
    """Turn a numeric score into a headline and a severity level."""
    if score == 0:
        return "Looks clean", "safe"
    if score <= 1:
        return "Worth a second look", "caution"
    return "Likely phishing", "danger"


def show_result(result, subject):
    """Render the verdict banner and the list of reasons."""
    headline, level = verdict(result["score"])

    if level == "safe":
        st.success(f"**{headline}** — nothing suspicious found in this {subject}.")
    elif level == "caution":
        st.warning(f"**{headline}** — phishing score {result['score']}")
    else:
        st.error(f"**{headline}** — phishing score {result['score']}")

    if result["reasons"]:
        st.write("**What was flagged:**")
        for reason in result["reasons"]:
            st.write(f"- {reason}")


st.set_page_config(page_title="Unhooked", page_icon=str(ICON) if ICON.exists() else None)
st.markdown(PINK_BUTTONS, unsafe_allow_html=True)
st.markdown(fishing_cursor_css(), unsafe_allow_html=True)

if LOGO.exists():
    # Send the full-resolution PNG and let CSS do the sizing. Passing width= to
    # st.image resamples server-side, which looks soft on high-density screens.
    encoded = base64.b64encode(LOGO.read_bytes()).decode()
    st.markdown(
        f'<img src="data:image/png;base64,{encoded}" '
        f'style="width:{LOGO_WIDTH}px; max-width:100%; display:block; '
        f'margin:0 0 1.4rem;">',
        unsafe_allow_html=True,
    )
else:
    st.title("Unhooked")

st.caption(DESCRIPTION)

mode = st.radio("What do you want to check?", ["A link", "An email"], horizontal=True)

if mode == "A link":
    url = st.text_input("Paste the link", placeholder="https://example.com/login")

    if st.button("Analyse link", type="primary"):
        if not url.strip():
            st.info("Paste a link above to analyse it.")
        else:
            show_result(url_analysis(url.strip()), "link")

else:
    sender = st.text_input("Sender's email address", placeholder="billing@example.com")

    st.markdown("**Email source**")
    st.caption(
        'In Gmail: open the email → ⋮ menu → "Show original". Pasting the source '
        "rather than the plain text lets Unhooked see where the links really go."
    )
    body = st.text_area(
        "Email source",
        height=220,
        placeholder="<p>Paste the email here…</p>",
        label_visibility="collapsed",
    )

    if st.button("Analyse email", type="primary"):
        if not sender.strip():
            st.info("Enter the sender's address above to analyse the email.")
        else:
            result = email_analysis(sender.strip(), body)

            if result is False:
                st.error(
                    "That doesn't look like an email address — it has no '@'. "
                    "Check the sender field and try again."
                )
            else:
                show_result(result, "email")

                if not extract_links(body):
                    st.info(
                        "No links were found, so link checking was skipped. "
                        "If you pasted plain text rather than the email source, "
                        "paste the source instead to check where links really go."
                    )
