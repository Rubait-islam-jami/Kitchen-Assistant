import streamlit as st
import requests

st.set_page_config(
    page_title="AI Kitchen Assistant",
    page_icon="🍽️",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
    background-color:#0f172a;
}

.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
}

.stTextInput > div > div > input{
    border-radius:12px;
    height:55px;
    font-size:17px;
}

.stButton > button{
    width:100%;
    height:55px;
    border-radius:12px;
    font-size:18px;
    font-weight:bold;
    background:#2563eb;
    color:white;
}

.stButton > button:hover{
    background:#1d4ed8;
    color:white;
}

.recipe-card{
    background:#1e293b;
    border:1px solid #334155;
    border-radius:15px;
    padding:22px;
    color:white;
    font-size:17px;
    line-height:1.8;
}

.footer{
    text-align:center;
    color:#94a3b8;
    margin-top:50px;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# Banner
st.image("images/banner.png", use_container_width=True)

st.write("")

question = st.text_input(
    "🍳 Ask your cooking question",
    placeholder="Example: I have tomatoes and eggs. What can I cook?"
)

if st.button("🔍 Get Recipe", use_container_width=True):

    if not question.strip():

        st.warning("Please enter a cooking question.")

    else:

        with st.spinner("Generating recipe recommendation..."):

            try:

                response = requests.post(
                    "http://localhost:5000/ask",
                    json={
                        "question": question
                    },
                    timeout=120
                )

                if response.status_code == 200:

                    result = response.json()

                    st.subheader("🍽️ Recipe Recommendation")

                    st.markdown(
                        f"""
<div class="recipe-card">

{result["answer"]}

</div>
""",
                        unsafe_allow_html=True
                    )

                    st.write("")
                    st.divider()

                    st.subheader("📊 Model Usage")

                    c1, c2, c3, c4 = st.columns(4)

                    c1.metric(
                        "🤖 Model",
                        result["usage"]["model"]
                    )

                    c2.metric(
                        "📝 Prompt Tokens",
                        result["usage"]["prompt_tokens"]
                    )

                    c3.metric(
                        "💬 Completion Tokens",
                        result["usage"]["completion_tokens"]
                    )

                    c4.metric(
                        "💲 Cost ($)",
                        f'{result["usage"]["cost"]:.6f}'
                    )

                else:

                    st.error("Flask API returned an error.")

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to the Flask API.\n\nRun:\n\npython app.py"
                )

            except Exception as e:

                st.error(f"Unexpected Error:\n\n{e}")

st.markdown("""
<div class="footer">

Built with ❤️ using Flask • Streamlit • Google Gemini • MinSearch • SQLite • Grafana

</div>
""", unsafe_allow_html=True)