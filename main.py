from urllib.parse import quote_plus
import pandas as pd
import time
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import streamlit as st
import matplotlib.pyplot as plt
from google import genai

load_dotenv()
AIClient = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

mongo_uri = os.getenv("MONGODB_URI")

client = MongoClient(mongo_uri)
db = client["expense_tracker"]
collection = db["expense_tracker"]

def predict_category(note: str) -> str:
    prompt = f"""
    Categorize this expense note into one of these categories:
    Food, Transportation, Entertainment, Other.
    Return only the category name.
    Note: {note}
    """
    try:
        time.sleep(4)
        response = AIClient.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={"max_output_tokens": 10, "temperature": 0}
        )
        cat = response.text.strip()
        return cat if cat in {"Food", "Transportation", "Entertainment", "Other"} else "Other"
    except Exception:
        return "Other"

def load_data():
    try:
        docs = list(collection.find({}, {"_id": 0}))
        return pd.DataFrame(docs)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

data = load_data()

st.title("Smart Expense Tracker")

with st.form("expense_form"):
    date = st.date_input("Date")
    description = st.text_input("Description / Note")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    category_input = st.text_input("Category (leave blank for AI)")
    entry_type = st.selectbox("Type", ["Expense", "Income"])
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        final_category = category_input.strip()

        if not final_category and description:
            with st.spinner("AI is categorizing..."):
                final_category = predict_category(description)
        elif not final_category:
            final_category = "Other"

        new_doc = {
            "Date": date.strftime("%m/%d/%Y"),
            "Category": final_category,
            "Note": description,
            "Amount": float(amount),
            "Type": entry_type
        }

        try:
            collection.insert_one(new_doc)
            st.success(f"Saved as '{final_category}'")
            st.rerun()
        except Exception as e:
            st.error(f"MongoDB insert failed: {e}")

st.subheader("Recent Entries")

if not data.empty:
    st.dataframe(data)

    data["Amount"] = pd.to_numeric(data["Amount"], errors="coerce").fillna(0)
    expenses = data[data["Type"] == "Expense"]

    if not expenses.empty:
        summary = expenses.groupby("Category")["Amount"].sum()

        col1, col2 = st.columns(2)
        with col1:
            st.write("Expenses by Category")
            fig, ax = plt.subplots()
            summary.plot(kind="bar", ax=ax)
            st.pyplot(fig)

        with col2:
            st.write("Distribution")
            fig2, ax2 = plt.subplots()
            summary.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
            ax2.set_ylabel("")
            st.pyplot(fig2)
