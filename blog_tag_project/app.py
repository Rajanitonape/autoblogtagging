import streamlit as st
import sqlite3
from auth import create_user, login_user
from model import predict_tags, predict_category
from utils import get_summary, platform_tags
from database import init_db

# -------------------------
# PAGE CONFIG (MUST BE FIRST STREAMLIT COMMAND)
# -------------------------
import base64

def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# -------------------------
# COLORFUL BACKGROUND
# -------------------------
st.markdown(
    """
    <style>

    /* 📱 Social media style background */
    .stApp {
        background-image: url("data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD...PASTE_CONTINUED_BASE64...");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    /* Soft glass effect for readability */
    .block-container {
        background-color: rgba(255,255,255,0.75);
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(6px);
    }

    /* Text styling */
    h1, h2, h3 {
        color: #1f2937 !important;
    }

    p, label, span {
        color: #374151 !important;
    }

    /* Input fields */
    .stTextInput input,
    .stTextArea textarea {
        background-color: rgba(255,255,255,0.9) !important;
        border-radius: 10px !important;
        border: 1px solid #e5e7eb !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #ff4b91, #ff8fab);
        color: white !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        border: none !important;
    }

    .stButton>button:hover {
        transform: scale(1.03);
        transition: 0.2s;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# -------------------------
# INIT DATABASE
# -------------------------
init_db()

# -------------------------
# SESSION STATE
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# -------------------------
# DB HELPER
# -------------------------
def get_connection():
    conn = sqlite3.connect("app.db", timeout=10, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

# -------------------------
# HEADER (UPDATED TITLE)
# -------------------------
st.title("🧠 Automated Content Tagging for Blogs")
st.caption("AI-powered tagging, summarization & categorization system")

# -------------------------
# SIDEBAR MENU
# -------------------------
menu = ["Login", "Signup", "App"]
choice = st.sidebar.radio("Navigation", menu)

# -------------------------
# LOGOUT
# -------------------------
if st.session_state.logged_in:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# =========================
# SIGNUP
# =========================
if choice == "Signup":
    st.subheader("🆕 Create Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        if username and password:
            if create_user(username, password):
                st.success("Account created successfully ✅")
            else:
                st.error("Username already exists ❌")
        else:
            st.warning("Please fill all fields")

# =========================
# LOGIN
# =========================
elif choice == "Login":
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)

        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful 🎉")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")

# =========================
# MAIN APP
# =========================
elif choice == "App":

    if not st.session_state.logged_in:
        st.warning("🔒 Please login first")
        st.stop()

    st.success(f"Welcome {st.session_state.username} 👋")

    tab1, tab2 = st.tabs(["✍️ Tag Generator", "📜 History"])

    # -------------------------
    # TAG GENERATOR
    # -------------------------
    with tab1:
        st.subheader("AI Blog Analyzer")

        content = st.text_area("Enter your blog content", height=200)
        platform = st.selectbox("Select Platform", ["Instagram", "YouTube", "Blog"])

        if st.button("Generate AI Insights 🚀"):

            if not content.strip():
                st.warning("⚠️ Please enter content")
            else:
                try:
                    tags = predict_tags(content)
                    category = predict_category(content)
                    summary = get_summary(content)
                    p_tags = platform_tags(platform)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.info("🏷️ Tags")
                        st.write(tags)

                        st.info("📂 Category")
                        st.write(category)

                    with col2:
                        st.info("🧾 Summary")
                        st.write(summary)

                        st.info("🌐 Platform Tags")
                        st.write(p_tags)

                    # Save to DB
                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute(
                        "INSERT INTO history(username, content, tags, category) VALUES (?,?,?,?)",
                        (st.session_state.username, content, str(tags), category)
                    )

                    conn.commit()
                    conn.close()

                    st.success("Saved to history ✅")

                except Exception as e:
                    st.error(f"Error: {e}")

    # -------------------------
    # HISTORY
    # -------------------------
    with tab2:
        st.subheader("Your Activity History")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT content, tags, category FROM history WHERE username=? ORDER BY id DESC",
            (st.session_state.username,)
        )

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            st.info("No history found yet 📭")
        else:
            for i, row in enumerate(rows, 1):
                with st.container():
                    st.markdown(f"### Post {i}")
                    st.write("📄 Content:", row[0])
                    st.write("🏷️ Tags:", row[1])
                    st.write("📂 Category:", row[2])
                    st.divider()


