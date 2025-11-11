import os
import streamlit as st
import base64
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from PIL import Image
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.llms import HuggingFaceHub  # ✅ Import Hugging Face Model Wrapper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Hugging Face API Key from Environment Variable
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Check if API Key is available
if not HF_API_KEY:
    st.error("❌ Hugging Face API Key is missing. Please add it to your .env file.")
    st.stop()

# Set page layout to wide for full-width capability
st.set_page_config(layout="wide")

# Function to read image as base64
def read_image_as_base64(filename):
    with open(filename, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Read logo as base64
try:
    logo_base64 = read_image_as_base64("logo.png")
except Exception as e:
    st.error(f"Error loading image: {e}")
    st.stop()

# Apply custom CSS to position elements properly
st.markdown(
    """
    <style>
        .main {
            margin: 0 auto;
            width: 100% !important;
            padding: 0 !important;
        }
        
        .header-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            width: 100%;
            margin: 0 auto;
        }

        .content-section {
            margin-left: 96px;
            margin-right: 96px;
            padding-top: 20px;
        }

        .chatbox {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgb(0 0 0 / 10%);
            width: 320px;
            position: fixed;
            right: 96px !important;
            top: 80px;
            z-index: 2;
        }

        .stFileUploader {
            margin-left: 0 !important;
            padding-left: 0 !important;
        }

        .stFileUploader label {
            transform: none !important;
            display: block;
        }

        .stFileUploader input[type="file"] {
            margin-right: 10px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Full-width header section for logo and title
st.markdown('<div class="header-section">', unsafe_allow_html=True)
st.markdown(f'<img src="data:image/png;base64,{logo_base64}" width="250" style="display: block; margin-left: auto; margin-right: auto; margin-bottom: 10px;" />', unsafe_allow_html=True)
st.markdown('<h1 style="text-align: center;"> AI Assistant for Data Science</h1>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Centered content section for EDA and chatbox
st.markdown('<div class="content-section">', unsafe_allow_html=True)
st.header("Exploratory Data Analysis (EDA)")
st.subheader("🔍 Solution")

# ✅ Initialize Hugging Face LLM (Fix for the error)
llm = HuggingFaceHub(
    repo_id="google/flan-t5-large",
    task="text2text-generation",  # ✅ Add this line
    model_kwargs={"temperature": 0.3, "max_length": 512},
    huggingfacehub_api_token=HF_API_KEY
)


# Create two columns within the content section (Left: EDA, Right: Chatbox)
left_col, right_col = st.columns([3, 1])

# Left Column: EDA Content
with left_col:
    uploaded_file = st.file_uploader("📂 Upload your CSV/Excel dataset", type=["csv", "xls", "xlsx"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)

            # ✅ Fix: Use the Hugging Face LLM instead of None
            agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)

            num_records = df.shape[0]
            st.subheader(f"📊 Number of Records: {num_records}")

            st.subheader("📌 Variables in Dataset:")
            st.write(list(df.columns))

            st.subheader("📊 Summary Statistics:")
            st.write(df.describe().T[["mean", "50%", "min", "max"]].rename(columns={"50%": "median"}))

            st.subheader("📊 Data Visualization")
            chart_type = st.selectbox("Choose a Chart Type", ["Scatter Plot", "Bar Chart", "Histogram", "Box Plot"])
            available_columns = df.columns.tolist()
            x_axis = st.selectbox("Select X-axis", available_columns, key="x_axis")
            if chart_type in ["Scatter Plot", "Box Plot"]:
                y_axis = st.selectbox("Select Y-axis", available_columns, key="y_axis")

            if chart_type == "Scatter Plot" and x_axis and y_axis:
                fig, ax = plt.subplots()
                sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
                st.pyplot(fig)
            elif chart_type == "Bar Chart" and x_axis:
                fig, ax = plt.subplots()
                sns.countplot(data=df, x=x_axis, ax=ax)
                st.pyplot(fig)
            elif chart_type == "Histogram" and x_axis:
                fig, ax = plt.subplots()
                sns.histplot(data=df, x=x_axis, kde=True, ax=ax)
                st.pyplot(fig)
            elif chart_type == "Box Plot" and x_axis and y_axis:
                fig, ax = plt.subplots()
                sns.boxplot(data=df, x=x_axis, y=y_axis, ax=ax)
                st.pyplot(fig)
        except Exception as e:
            st.error(f"❌ Error reading file or creating agent: {e}")

# ✅ Right Column: Chatbox Content (Updated)
with right_col:
    st.markdown('<div class="chatbox">', unsafe_allow_html=True)
    st.header("💬 Chat with AI")
    st.write("Ask AI anything about your dataset!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_question = st.text_input("💡 Type your question:")

    if uploaded_file and user_question:
        # ✅ Process dataset summary before sending to API
        df_summary = df.describe().to_string()  # Convert summary to string

        # ✅ Define Hugging Face API function
        def query_huggingface_api(question, df_summary):
            api_url = "https://api-inference.huggingface.co/models/google/tabt5-large"  # ✅ Use TabT5 Model
            headers = {"Authorization": f"Bearer {HF_API_KEY}"}

            # ✅ Format input for API
            formatted_input = f"Question: {question} \n Table: {df_summary}"

            response = requests.post(api_url, headers=headers, json={"inputs": formatted_input})

            if response.status_code == 200:
                return response.json()[0]["generated_text"]
            else:
                return "⚠️ Error: Unable to get a response. Try again later."

        # ✅ Get AI response
        ai_response = query_huggingface_api(user_question, df_summary)

        # ✅ Store conversation history
        st.session_state.chat_history.append(("You", user_question))
        st.session_state.chat_history.append(("AI", ai_response))

    # ✅ Display chat history
    for role, text in st.session_state.chat_history:
        if role == "You":
            st.markdown(f"**🧑 You:** {text}")
        else:
            st.markdown(f"**🤖 AI:** {text}")

    st.markdown('</div>', unsafe_allow_html=True)






from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model_name = "google/flan-t5-small"  # Try "t5-small" if needed
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def ask_model(question):
    inputs = tokenizer(question, return_tensors="pt")
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Test the Model
print(ask_model("What is the highest value in Quantity: [1, 5, 10, 3, 7, 8, 2]?"))

