import pandas as pd
import re
from google import genai
import os
from dotenv import load_dotenv
import time
import matplotlib.pyplot as plt
import streamlit as st


load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# send a note and return a category
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
            config={
                "max_output_tokens": 10,
                "temperature": 0,
            }
        )
        category = response.text.strip()
        if category in ["Food", "Transportation", "Entertainment", "Other"]:
            return category
        return "Other"
    except Exception as e:
        return "Other"
    
def parse_amount(s):
    if pd.isna(s) or s == '':
        return 0.0
    s = re.sub(r'[^\d\.-]', '', str(s))
    return float(s)

def add_expense(date, category, note, amount, type):
    global data
    new_expense = {
        "Date": date,
        "Category": category,
        "Note": note,
        "Amount": amount,
        "Type": type
    }
    new_row_df = pd.DataFrame([new_expense])
    data = pd.concat([data, new_row_df], ignore_index=True)


csv_file = "Expense_data_1.csv"
if os.path.exists(csv_file):
    data = pd.read_csv(csv_file, converters={"Amount": parse_amount})
else:
    data = pd.DataFrame(columns=["Date", "Category", "Note", "Amount", "Type"])

st.title("Smart Expense Tracker")

with st.form("expense_form"):
    date = st.date_input("Date")
    description = st.text_input("Description/Note")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")

    predicted_category = ""
    if description:
        predicted_category = predict_category(description)

    category = st.text_input("Category (you can edit the predicted category)", value=predicted_category)
    type = st.selectbox("Type", ["Expense", "Income"])
    submitted = st.form_submit_button("Add Expense/Income")

    if submitted:
        add_expense(date, category, description, amount, type)
        data.to_csv(csv_file, index=False)
        st.success("Expense/Income added successfully!")

st.subheader("All Expenses/Incomes")
st.dataframe(data)

if not data.empty:
    st.subheader("Expense Summary by Category")
    
    expense_summary = data[data['Type'] != 'Income'].groupby("Category")["Amount"].sum()
    
    # Bar Chart
    fig, ax = plt.subplots()
    expense_summary.plot(kind="bar", ax=ax)
    ax.set_ylabel("Amount")
    st.pyplot(fig)

    # Pie Chart
    st.subheader("Category Distribution")
    fig2, ax2 = plt.subplots()
    expense_summary.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
    st.pyplot(fig2)
