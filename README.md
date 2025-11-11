# 🧠 AI Assistant for Data Science

## An intelligent Streamlit application that performs Exploratory Data Analysis (EDA) and allows **interactive dataset exploration through natural language chat**, powered by Hugging Face and LangChain.

---

## 🗒️ Table of Contents

1. [Overview](#overview)
2. [Motivation](#motivation)
3. [Features](#features)
4. [Architecture](#architecture)
5. [Technology Stack](#technology-stack)
6. [Setup & Installation](#setup--installation)
7. [Running the App](#running-the-app)
8. [Project Structure](#project-structure)
9. [Detailed Workflow](#detailed-workflow)
10. [Chat with Your Dataset](#chat-with-your-dataset)
11. [How the AI Works](#how-the-ai-works)
12. [Data Visualization Guide](#data-visualization-guide)
13. [Screenshot Uploads](#screenshot-uploads)
14. [SQLite Integration](#sqlite-integration)
15. [Security & Environment Variables](#security--environment-variables)
16. [Example Outputs](#example-outputs)
17. [Use Cases](#use-cases)
18. [Future Enhancements](#future-enhancements)
19. [Contributing](#contributing)
20. [License](#license)
21. [Author](#author)

---

## 🧭 Overview

**AI Assistant for Data Science** is an **AI-powered EDA and conversational analytics app** that transforms how data professionals explore datasets.
Users can upload their CSV/Excel files, visualize them, generate insights, and — most importantly — **ask questions about their data directly through a chatbot interface**.

The system uses **LangChain’s Pandas Agent** combined with **Hugging Face’s Flan-T5 / TabT5** models to convert your natural language queries into pandas operations and descriptive insights.


## 🖼️ Screenshot Uploads

<img width="1470" height="789" alt="Homepage" src="https://github.com/user-attachments/assets/72ec6160-8c93-4381-b9ed-d9a58ee7be5a" />
<img width="1470" height="789" alt="EDA" src="https://github.com/user-attachments/assets/64297f36-8b9f-41e9-bf69-475a277cc0d7" />

---

## 💡 Motivation

Data exploration is typically code-heavy and repetitive — requiring dozens of Python commands to understand even a small dataset.
This project aims to make data understanding **intuitive and conversational**.

Instead of writing:

```python
df.groupby('Region')['Sales'].mean()
```

You can simply ask:

“What’s the average sales by region?”

and get both the computed result and an explanation instantly.

This fusion of EDA + Conversational AI bridges the gap between data science, analytics, and user-friendly intelligence systems.

---

## 🚀 Features

| Category                      | Description                                                                         |
| ----------------------------- | ----------------------------------------------------------------------------------- |
| **Data Upload**               | Upload `.csv` or `.xlsx` files using Streamlit UI.                                  |
| **Automated EDA**             | Displays total records, column names, and summary statistics.                       |
| **Interactive Visualization** | Choose between scatter plots, histograms, bar charts, and box plots.                |
| **Conversational AI**         | Ask questions about your dataset in plain English through the chatbox.              |
| **LangChain Integration**     | Natural language queries executed directly on pandas DataFrames.                    |
| **AI-Powered Reasoning**      | Uses google/flan-t5-large and google/tabt5-large for understanding tabular context. |
| **Memory-Based Chat**         | Maintains session history so conversation feels continuous.                         |
| **Local LLM Demo**            | Includes a lightweight test using flan-t5-small to verify local inference.          |
| **SQLite Support**            | Demonstrates backend persistence and extension capability.                          |
| **Custom UI**                 | Responsive Streamlit design with a floating chat window and centered header.        |

---

## 🏗️ Architecture

```
 ┌────────────────────────────┐
 │     User Interaction Layer │
 │  (Streamlit + Chat Interface)
 └──────────────┬─────────────┘
                │
 ┌──────────────▼─────────────┐
 │  Data Layer (Pandas, Seaborn)
 │   ↳ EDA, summary stats, charts
 └──────────────┬─────────────┘
                │
 ┌──────────────▼─────────────┐
 │ LangChain Pandas Agent     │
 │  ↳ Converts questions into pandas code
 └──────────────┬─────────────┘
                │
 ┌──────────────▼─────────────┐
 │ Hugging Face API (Flan-T5) │
 │  ↳ Generates natural language insights
 └──────────────┬─────────────┘
                │
 ┌──────────────▼─────────────┐
 │ SQLite & Local Storage     │
 │  ↳ Test persistence layer  │
 └────────────────────────────┘
```

---

## ⚙️ Technology Stack

| Layer                   | Tools & Frameworks                        |
| ----------------------- | ----------------------------------------- |
| **Frontend / UI**       | Streamlit, HTML, CSS                      |
| **EDA & Visualization** | Pandas, Seaborn, Matplotlib               |
| **AI Reasoning**        | LangChain, Hugging Face Hub, Transformers |
| **Data Storage**        | SQLite, CSV/Excel                         |
| **Configuration**       | python-dotenv                             |
| **Language**            | Python 3.10+                              |

---

## 🧰 Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/AI_Data_Assistant.git
cd AI_Data_Assistant
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate     # macOS / Linux
venv\\Scripts\\activate        # Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

If missing:

```bash
pip install streamlit pandas seaborn matplotlib requests python-dotenv langchain langchain-experimental huggingface_hub transformers Pillow
pip freeze > requirements.txt
```

### 4. Add Environment Variables

Create a `.env` file in the project root:

```bash
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
```

Get your token from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

---

## ▶️ Running the App

```bash
streamlit run app.py
```

The app will open automatically at:

```
http://localhost:8501
```

---

## 🗂️ Project Structure

```
AI_Data_Assistant/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Dependencies
├── .env.example           # Sample environment file
├── logo.png               # App logo
│
├── data/
│   └── sample.csv         # Sample dataset
│
├── utils/
│   └── db_check.py        # SQLite test script
│
└── README.md              # Documentation
```

---

## 🔍 Detailed Workflow

* **Upload**: User uploads CSV/Excel → DataFrame created.
* **EDA**: Summary statistics auto-generated.
* **Visualization**: Choose chart type → Seaborn renders inline.
* **AI Integration**: LangChain agent + Hugging Face model.
* **Chat**: Conversational interface for querying datasets.
* **Session History**: Chat stored via Streamlit session state.
* **SQLite**: Confirms DB connectivity for expansion.

---

## 💬 Chat with Your Dataset

Interact directly with your dataset through the right-hand chatbox.

Examples:

* “What columns have missing values?”
* “Which product category has the highest revenue?”
* “Show correlation between age and income.”
* “Summarize this dataset in one sentence.”

Under the hood:

* LangChain interprets queries → executes pandas code.
* Hugging Face (Flan-T5 / TabT5) summarizes and formats output.
* Chat history updated for contextual conversation.

Result: A **conversational interface for structured data**.

---

## 🧩 How the AI Works

### 1. LangChain Pandas Agent

Executes pandas logic from text queries.

```python
df.groupby('city')['income'].mean().sort_values(ascending=False).head(5)
```

### 2. Hugging Face API

Generates human-readable responses and contextual insights.

Both layers combine for **LLM-driven reasoning** on tabular data.

---

## 📊 Data Visualization Guide

| Chart            | Description                                          |
| ---------------- | ---------------------------------------------------- |
| **Scatter Plot** | Compare relationships between two numeric variables. |
| **Bar Chart**    | Frequency of categorical values.                     |
| **Histogram**    | Value distribution overview.                         |
| **Box Plot**     | Detect spread and outliers.                          |

---

```markdown
![App Header](docs/header.png)
![EDA Summary](docs/summary.png)
![Chat Interface](docs/chat.png)
```

This will allow GitHub to render the screenshots directly within your README for better visual presentation.

---

## 💾 SQLite Integration

Example:

```python
import sqlite3
conn = sqlite3.connect("test.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
conn.commit()
conn.close()
```

Expandable for logging, authentication, or caching.

---

## 🔐 Security & Environment Variables

* `.env` stores API tokens safely.
* Never commit `.env`.
* Add to `.gitignore`:

```
.env
venv/
__pycache__/
test.db
```

---

## 📸 Example Outputs

| Section             | Example       |
| ------------------- | ------------- |
| Dataset Summary     | *(add image)* |
| Chart Visualization | *(add image)* |
| Chat Interface      | *(add image)* |

---

## 🧮 Use Cases

* Rapid EDA & Data Discovery
* Conversational Analytics
* Data Education & Training
* AI Research on Tabular Reasoning
* Analyst Copilot for Business Teams

---

## 🔮 Future Enhancements

| Feature              | Description                                       |
| -------------------- | ------------------------------------------------- |
| Automated Reports    | Generate full-text EDA summaries as PDF/Markdown. |
| RAG Integration      | Add vector database for contextual retrieval.     |
| Drift Detection      | Time-series data drift analysis.                  |
| Database Integration | Connect to Snowflake, Redshift, BigQuery.         |
| Dashboard Mode       | Convert chat results to dashboard widgets.        |
| Model Comparison     | Evaluate multiple LLMs for tabular tasks.         |

---

## 🤝 Contributing

1. Fork the repo
2. Create branch `feature-name`
3. Commit changes
4. Push & open PR

Follow PEP8 & document code clearly.

---

## 📄 License

MIT License. See [LICENSE](LICENSE).

---

## 👤 Author

**Kiran Ranganalli**
Data Engineer / Data Scientist
📍 San Francisco, CA
📧 [ranganallikiran@gmail.com](mailto:ranganallikiran@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/kiranranganalli/) | [GitHub](https://github.com/<your-username>)

> “Bridging data exploration and AI — because understanding data should be as easy as asking a question.”
