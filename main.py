import streamlit as st

st.set_page_config(
    page_title="Daniel's Projects",
    page_icon="👑",
    layout="wide"
)

# --- Title ---
st.title("👑 Daniel's Projects")

# --- About me ---
st.subheader("Hi! I'm Daniel 👋")
st.write("""
I'm a developer, and here you can explore all the projects I've built.  
Choose a project from the left sidebar or from the list below.
""")

st.divider()

# --- Projects list ---
st.header("📂 Project List")

st.write("Click a project name below to open its page:")

st.markdown("""
### 🔹 [Guessing Game](/Guessing_Game)
A Python guessing/alias-style game I created.
""")
