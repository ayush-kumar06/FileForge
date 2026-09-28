"""
🔥 FileForge
Create, read, update and delete files with Python + Streamlit.

Run with:
    streamlit run fileforge_app.py
"""

import html
from pathlib import Path

import streamlit as st

# ----------------------------- PAGE CONFIG ----------------------------- #
st.set_page_config(
    page_title="FileForge",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed",
)

APP_FILE = Path(__file__).resolve()

# ------------------------------- STYLING -------------------------------- #
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono&display=swap');

        html, body, [class*="css"], .stApp {
            font-family: 'Space Grotesk', sans-serif;
        }
        .stApp {
            background:
                radial-gradient(circle at 15% 0%, rgba(255, 81, 47, 0.18) 0%, transparent 40%),
                radial-gradient(circle at 90% 10%, rgba(221, 36, 118, 0.18) 0%, transparent 40%),
                #0b0b12;
            color: #e8e8f0;
        }
        #MainMenu, footer { visibility: hidden; }
        header[data-testid="stHeader"] { background: transparent; }
        .block-container { padding-top: 2rem; max-width: 780px; }

        /* ---------- HERO ---------- */
        .hero { text-align: center; padding: 1.5rem 0 1rem 0; }
        .hero-badge {
            display: inline-block;
            padding: 0.3rem 0.9rem;
            border: 1px solid rgba(255, 121, 63, 0.5);
            border-radius: 999px;
            font-size: 0.75rem;
            letter-spacing: 0.15em;
            color: #ff9a6b;
            background: rgba(255, 121, 63, 0.08);
        }
        .hero-title {
            font-size: 4.2rem;
            font-weight: 700;
            line-height: 1.05;
            margin: 0.6rem 0 0.2rem 0;
            color: #ffffff;
            letter-spacing: -0.03em;
        }
        .hero-title span {
            background: linear-gradient(90deg, #ff512f 0%, #f09819 50%, #dd2476 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-sub { color: #9a9ab0; font-size: 1.05rem; margin: 0; }

        /* ---------- STAT CARDS ---------- */
        .stat-card {
            background: linear-gradient(145deg, #15151f, #10101a);
            border: 1px solid #23233a;
            border-radius: 16px;
            padding: 1rem 1.1rem;
            text-align: center;
        }
        .stat-num {
            font-size: 1.8rem; font-weight: 700;
            background: linear-gradient(90deg, #ff512f, #f09819);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .stat-label { color: #8a8aa0; font-size: 0.8rem; letter-spacing: 0.08em; text-transform: uppercase; }

        /* ---------- TABS ---------- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: #12121b;
            padding: 0.4rem;
            border-radius: 14px;
            border: 1px solid #23233a;
        }
        .stTabs [data-baseweb="tab"] {
            height: 44px;
            border-radius: 10px;
            padding: 0 1.1rem;
            color: #9a9ab0;
            font-weight: 500;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, #ff512f, #dd2476);
            color: #ffffff !important;
        }
        .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

        /* ---------- INPUTS ---------- */
        label, .stMarkdown p { color: #c9c9da; }
        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div,
        div[data-baseweb="select"] > div {
            background-color: #14141e !important;
            border: 1px solid #2a2a40 !important;
            border-radius: 12px !important;
        }
        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea { color: #f1f1f8 !important; }
        div[data-baseweb="input"] > div:focus-within,
        div[data-baseweb="textarea"] > div:focus-within {
            border-color: #ff7a3f !important;
            box-shadow: 0 0 0 3px rgba(255, 122, 63, 0.18) !important;
        }

        /* ---------- BUTTONS ---------- */
        .stButton > button, .stDownloadButton > button {
            width: 100%;
            border: none;
            border-radius: 12px;
            padding: 0.7rem 0;
            font-weight: 700;
            font-size: 1rem;
            color: #fff;
            background: linear-gradient(90deg, #ff512f 0%, #dd2476 100%);
            box-shadow: 0 6px 22px rgba(255, 81, 47, 0.28);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 28px rgba(255, 81, 47, 0.45);
            color: #fff;
        }

        /* ---------- FEEDBACK BOXES ---------- */
        .result-box {
            padding: 0.9rem 1.1rem; border-radius: 12px; margin-top: 1rem;
            font-size: 0.95rem; border: 1px solid transparent;
        }
        .ok   { background: rgba(34,197,94,0.10);  border-color: rgba(34,197,94,0.4);  color: #86efac; }
        .err  { background: rgba(239,68,68,0.10);  border-color: rgba(239,68,68,0.4);  color: #fca5a5; }
        .info { background: rgba(59,130,246,0.10); border-color: rgba(59,130,246,0.4); color: #93c5fd; }

        /* ---------- FILE PREVIEW ---------- */
        .preview {
            background: #07070c;
            border: 1px solid #23233a;
            border-left: 4px solid #ff7a3f;
            color: #e2e8f0;
            padding: 1rem 1.2rem;
            border-radius: 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.88rem;
            white-space: pre-wrap;
            max-height: 340px;
            overflow-y: auto;
            margin-top: 1rem;
        }

        /* ---------- FILE CHIPS ---------- */
        .chip {
            display: inline-block; margin: 0.25rem 0.3rem 0.25rem 0;
            padding: 0.35rem 0.8rem; border-radius: 999px;
            background: #15151f; border: 1px solid #2a2a40;
            color: #d6d6e6; font-size: 0.85rem;
        }
        .section-title { font-size: 1.15rem; font-weight: 700; margin: 0.6rem 0 0.2rem 0; color: #fff; }
        .section-sub { color: #8a8aa0; font-size: 0.9rem; margin-bottom: 0.8rem; }
        .footer { text-align: center; color: #5d5d75; font-size: 0.8rem; margin-top: 2.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------ HELPERS ---------------------------------- #
def bold(text: str) -> str:
    return f"<b>{html.escape(text)}</b>"


def notify(kind: str, icon: str, message_html: str) -> None:
    st.markdown(
        f'<div class="result-box {kind}">{icon} {message_html}</div>',
        unsafe_allow_html=True,
    )


def ok(msg: str) -> None:
    notify("ok", "✅", msg)


def err(msg: str) -> None:
    notify("err", "❌", msg)


def info(msg: str) -> None:
    notify("info", "💡", msg)


def section(title: str, sub: str) -> None:
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-sub">{sub}</div>', unsafe_allow_html=True)


def workspace_files() -> list[Path]:
    return sorted(
        p
        for p in Path(".").iterdir()
        if p.is_file() and not p.name.startswith(".") and p.resolve() != APP_FILE
    )


def human_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


# -------------------------------- HERO ----------------------------------- #
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">🔥 PYTHON · STREAMLIT</div>
        <h1 class="hero-title">File<span>Forge</span></h1>
        <p class="hero-sub">Forge it. Read it. Reshape it. Burn it.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------- STATS ----------------------------------- #
files = workspace_files()
total_bytes = sum(f.stat().st_size for f in files)

c1, c2, c3 = st.columns(3)
for col, num, label in (
    (c1, str(len(files)), "Files"),
    (c2, human_size(total_bytes), "Total size"),
    (c3, "4", "Operations"),
):
    col.markdown(
        f'<div class="stat-card"><div class="stat-num">{num}</div>'
        f'<div class="stat-label">{label}</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

# -------------------------------- TABS ----------------------------------- #
tab_create, tab_read, tab_update, tab_delete = st.tabs(
    ["🔨 Create", "🔍 Read", "✏️ Update", "🔥 Delete"]
)

# ------------------------------ CREATE ----------------------------------- #
with tab_create:
    section("Forge a new file", "Give it a name, drop in some content, and it's made.")
    name = st.text_input("File name", placeholder="notes.txt", key="create_name")
    data = st.text_area("Content", height=150, placeholder="Write something...", key="create_data")

    if st.button("🔨 Forge File", key="create_btn"):
        try:
            if not name.strip():
                err("Please enter a file name.")
            else:
                path = Path(name.strip())
                if path.exists():
                    err(f"{bold(name)} already exists.")
                else:
                    path.write_text(data, encoding="utf-8")
                    ok(f"{bold(name)} forged successfully!")
                    st.toast("File created", icon="🔨")
        except Exception as e:
            err(f"Something went wrong: {html.escape(str(e))}")

# ------------------------------- READ ------------------------------------ #
with tab_read:
    section("Inspect a file", "Open any file in the workspace and view its content.")
    name = st.text_input("File name", placeholder="notes.txt", key="read_name")

    if st.button("🔍 Open File", key="read_btn"):
        try:
            if not name.strip():
                err("Please enter a file name.")
            else:
                path = Path(name.strip())
                if not path.is_file():
                    err(f"No such file: {bold(name)}")
                else:
                    content = path.read_text(encoding="utf-8")
                    ok(f"Loaded {bold(name)} ({human_size(path.stat().st_size)})")
                    shown = html.escape(content) if content.strip() else "(file is empty)"
                    st.markdown(f'<div class="preview">{shown}</div>', unsafe_allow_html=True)
                    st.write("")
                    st.download_button(
                        "⬇️ Download copy", data=content, file_name=path.name, key="read_dl"
                    )
        except Exception as e:
            err(f"Something went wrong: {html.escape(str(e))}")

# ------------------------------ UPDATE ----------------------------------- #
with tab_update:
    section("Reshape a file", "Rename it, add to it, or replace everything inside.")
    name = st.text_input("File name", placeholder="notes.txt", key="update_name")

    if not name.strip():
        info("Enter a file name to see the update options.")
    else:
        path = Path(name.strip())
        if not path.is_file():
            err(f"No such file: {bold(name)}")
        else:
            action = st.radio(
                "What do you want to do?",
                ["Rename", "Append", "Overwrite"],
                horizontal=True,
                key="update_action",
            )

            if action == "Rename":
                new_name = st.text_input("New file name", key="update_new_name")
                if st.button("✏️ Rename File", key="rename_btn"):
                    try:
                        if not new_name.strip():
                            err("Please enter a new file name.")
                        elif Path(new_name.strip()).exists():
                            err(f"{bold(new_name)} already exists.")
                        else:
                            path.rename(new_name.strip())
                            ok(f"Renamed to {bold(new_name)}")
                    except Exception as e:
                        err(f"Something went wrong: {html.escape(str(e))}")

            elif action == "Append":
                extra = st.text_area("Content to add", height=120, key="append_data")
                if st.button("➕ Append Content", key="append_btn"):
                    try:
                        with open(path, "a", encoding="utf-8") as fs:
                            fs.write("\n" + extra)
                        ok("Content appended.")
                    except Exception as e:
                        err(f"Something went wrong: {html.escape(str(e))}")

            else:
                new_data = st.text_area(
                    "New content (replaces everything)", height=150, key="overwrite_data"
                )
                if st.button("♻️ Overwrite File", key="overwrite_btn"):
                    try:
                        path.write_text(new_data, encoding="utf-8")
                        ok("File overwritten.")
                    except Exception as e:
                        err(f"Something went wrong: {html.escape(str(e))}")

# ------------------------------ DELETE ----------------------------------- #
with tab_delete:
    section("Burn a file", "Permanently remove a file. This can't be undone.")
    name = st.text_input("File name", placeholder="notes.txt", key="delete_name")
    confirm = st.checkbox("Yes, I want to delete this file permanently", key="delete_confirm")

    if st.button("🔥 Delete File", key="delete_btn"):
        try:
            if not name.strip():
                err("Please enter a file name.")
            elif not confirm:
                info("Tick the confirmation box first.")
            else:
                path = Path(name.strip())
                if not path.is_file():
                    err(f"No such file: {bold(name)}")
                elif path.resolve() == APP_FILE:
                    err("You can't delete the app itself.")
                else:
                    path.unlink()
                    ok(f"{bold(name)} burned.")
                    st.toast("File deleted", icon="🔥")
        except Exception as e:
            err(f"Something went wrong: {html.escape(str(e))}")

# ----------------------------- WORKSPACE --------------------------------- #
st.write("")
with st.expander("📂 Files in workspace", expanded=False):
    current = workspace_files()
    if current:
        chips = "".join(
            f'<span class="chip">📄 {html.escape(f.name)} · {human_size(f.stat().st_size)}</span>'
            for f in current
        )
        st.markdown(chips, unsafe_allow_html=True)
    else:
        st.markdown('<span class="section-sub">No files yet. Forge your first one!</span>', unsafe_allow_html=True)

st.markdown('<div class="footer">FileForge · Built with Python & Streamlit</div>', unsafe_allow_html=True)