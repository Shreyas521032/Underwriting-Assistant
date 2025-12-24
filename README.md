# 🛡️ Underwriting Assistant AI: Multi-Agent Risk Assessment

The **Underwriting Assistant AI** is a Streamlit application designed to streamline and enhance the insurance underwriting process. It utilizes a powerful **Multi-Agent System** powered by a Large Language Model (Mixtral-8x7B via Hugging Face) for nuanced risk assessment and provides a robust **rule-based fallback mode** for guaranteed, transparent results.

This tool helps underwriters quickly assess an applicant's risk profile based on demographic data, claims history, health factors, and external reports, generating an actionable recommendation.

🔗 **Live Deployed Project:** [https://shreyas-underwriting-assistant.streamlit.app](https://shreyas-underwriting-assistant.streamlit.app/)

---

## ✨ Features

* **Dual-Mode Analysis:** Seamlessly switch between **AI Agent Mode** (LLM-powered) and **Rule-based Mode** (deterministic logic).
* **Multi-Agent Architecture:** A chain of four specialized agents works together to provide a comprehensive analysis:
    1.  **Data Summarization Agent**
    2.  **Claims Analysis Agent**
    3.  **Risk Factor Agent**
    4.  **Recommendation Agent**
* **Dynamic Risk Scoring:** A consistent, weighted algorithm calculates a numerical risk score (0-100) and assigns a risk category (Low, Medium, High).
* **LLM Fallback Logic:** If the Hugging Face API key is missing or the LLM call fails, the application automatically provides rule-based analysis outputs instead of breaking.
* **Comprehensive Reporting:** Downloadable reports in both **JSON** and **TXT** formats containing all raw data and agent outputs.
* **Interactive UI:** Intuitive Streamlit interface with tabs for application input, analysis results, system flow visualization, and sample data.

---

## 🛠️ Technology Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | `streamlit`, `custom CSS` | Interactive UI, data input, and results visualization. |
| **Backend** | `Python`, `Session State` | Data processing, state management, and orchestration. |
| **LLM Orchestration** | `langchain`, `ChatHuggingFace` | Framework for connecting Python code to the LLM endpoint. |
| **Large Language Model** | `Mixtral-8x7B-Instruct-v0.1` | Generative AI for advanced reasoning and analysis. |
| **API** | `HuggingFaceEndpoint` | Access to the Mixtral model via Hugging Face API. |

---

## 🚀 Quickstart

### Prerequisites

You need a **Python 3.8+** environment and a **Hugging Face API Key** to run the AI Agent Analysis mode.

1.  **Install Dependencies:**

    Create a file named `requirements.txt` with the following content:

    ```text
    streamlit
    pandas
    requests
    python-dateutil
    langchain
    langchain-huggingface
    ```

    Then, install them using pip:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Get Your API Key:**

    Obtain your free API key from the [Hugging Face website](https://huggingface.co/settings/tokens).

### Running the Application

1.  Save the entire provided code as a Python file (e.g., `app.py`).
2.  Run the application from your terminal:

    ```bash
    streamlit run app.py
    ```

3.  The app will open in your browser.

---

## 💻 Usage Guide

### 1. Application Form (Tab 1)

* Fill in all applicant details, including age, occupation, health, and coverage amount.
* Use the expanders to enter detailed **Claims History**.
* Input data from **External Reports** (Credit Score, Criminal Record, Driving Record).
* **Crucially, click the "💾 Save Application Data" button** to store the data in the application's memory for analysis.

### 2. API Configuration (Sidebar)

* Enter your **Hugging Face API Key** in the sidebar's text input.
* A success message will confirm if the key is configured and the **AI Mode** is available.

### 3. Running the Analysis

#### **🌐 AI Agent Analysis (Tab 3)**

* Requires a valid Hugging Face API Key.
* Click **"🛡️ Run AI Agent Analysis"**.
* The system will prompt the four LLM agents in sequence to produce a nuanced, context-aware assessment.

#### **📊 Rule-based Analysis (Tab 2)**

* Always available, even without an API key.
* Click **"📊 Run Rule-based Analysis"**.
* The system uses the deterministic, rule-based logic within each agent to provide a fast and transparent assessment.

### 4. Review & Export

* The results are displayed with a risk score, category, and individual outputs from each agent.
* Use the **"📄 Download JSON Report"** or **"📝 Download Text Report"** buttons to export the full assessment for documentation.

---

## ⚙️ Core Components: Agent Flow

The system orchestrates a chain of LLM calls (or rule-based functions) to build a cohesive risk profile.

1.  **Agent 1 (Data Summarization):** Creates a professional summary from raw applicant data.
2.  **Agent 2 (Claims Analysis):** Analyzes the total and individual claims to identify patterns in frequency, severity, and type.
3.  **Agent 3 (Risk Factor Identification):** Consolidates all data to identify the top 3-5 most critical risk factors.
4.  **Risk Score Calculation (Deterministic):** Calculates the final numerical score based on a fixed, auditable rule set.
5.  **Agent 4 (Recommendation Generation):** Takes the score, category, and all preceding agent outputs to generate an actionable decision (APPROVE, APPROVE WITH CONDITIONS, MANUAL REVIEW, DECLINE).
