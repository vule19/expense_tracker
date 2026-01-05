import pandas as pd
import re
from google import genai
import os
from dotenv import load_dotenv
import time
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_gsheets import GSheetsConnection

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

conn = st.connection("gsheets", type=GSheetsConnection)

def predict_category(note):
    prompt = f"""
    Categorize this expense note into one of these categories: 
    Food, Transportation, Entertainment, Other.
    Return only the category name as a single word.
    Note: {note}
    """
    try:
        time.sleep(4)
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt,
            config={"max_output_tokens": 10, "temperature": 0}
        )
        category = response.text.strip()
        if category in ["Food", "Transportation", "Entertainment", "Other"]:
            return category
        return "Other"
    except Exception:
        return "Other"

try:
    data = conn.read(spreadsheet=st.secrets["gsheets_url"], ttl=0)
except Exception:
    data = pd.DataFrame(columns=["Date", "Category", "Note", "Amount", "Type"])

st.title("Smart Expense Tracker")

with st.form("expense_form"):
    date = st.date_input("Date")
    description = st.text_input("Description/Note")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    category_input = st.text_input("Category (leave blank for AI prediction)")
    entry_type = st.selectbox("Type", ["Expense", "Income"])
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        final_category = category_input.strip()
        
        if not final_category and description:
            with st.spinner("AI is categorizing..."):
                final_category = predict_category(description)
        elif not final_category:
            final_category = "Other"

        new_row = pd.DataFrame([{
            "Date": str(date),
            "Category": final_category,
            "Note": description,
            "Amount": amount,
            "Type": entry_type
        }])

        updated_data = pd.concat([data, new_row], ignore_index=True)
        conn.update(spreadsheet=st.secrets["gsheets_url"], data=updated_data)
        
        st.success(f"Saved to Google Sheets as '{final_category}'!")
        st.rerun()

st.subheader("Recent Entries")
st.dataframe(data)

if not data.empty:
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce').fillna(0)
    expense_only = data[data['Type'] == 'Expense']
    
    if not expense_only.empty:
        expense_summary = expense_only.groupby("Category")["Amount"].sum()
        
        if expense_summary.sum() > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.write("Expenses by Category")
                fig, ax = plt.subplots()
                expense_summary.plot(kind="bar", ax=ax)
                st.pyplot(fig)
            with col2:
                st.write("Distribution")
                fig2, ax2 = plt.subplots()
                expense_summary.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
                ax2.set_ylabel("")
                st.pyplot(fig2)