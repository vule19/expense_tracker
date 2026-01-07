# 💰 Smart Expense Tracker (AI-Powered)

## Check it out here: https://expensetracker-mxhkljqx8kedpbthwvrtvb.streamlit.app/

A sleek, modern expense management application built with **Streamlit** and powered by **Google Gemini 2.0**. This app automatically predicts the category of your expenses based on your descriptions, saving you time on manual data entry.

## ✨ Features
* **AI Auto-Categorization:** Uses Google Gemini to intelligently suggest categories (Food, Transportation, Entertainment, etc.) as you type.
* **Interactive Visualizations:** View your spending habits through dynamic bar charts and pie charts.
* **Persistent Storage:** MongoDB
* **Smart Parsing:** Automatically handles currency symbols and formatting.

## 🚀 Getting Started

### Prerequisites
* Python 3.9 or higher
* A Google AI API Key (Get one for free at [Google AI Studio](https://aistudio.google.com/))

### Installation
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/expense-tracker.git](https://github.com/yourusername/expense-tracker.git)
    cd expense-tracker
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your API key:
    ```text
    GOOGLE_API_KEY=your_actual_api_key_here
    ```

### Running the App
```bash
streamlit run main.py
