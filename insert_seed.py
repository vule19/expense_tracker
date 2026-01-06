from urllib.parse import quote_plus
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

load_dotenv()
password = quote_plus(os.getenv("MONGODB_PASSWORD"))
mongo_uri = f"mongodb+srv://anhvle1901_db_user:{password}@cluster0.ymjq4sv.mongodb.net/?authSource=admin"

client = MongoClient(mongo_uri)
db = client["expense_tracker"]
collection = db["expense_tracker"]

rows = [
    {"Date":"1/2/2026","Account":"Main Bank","Category":"Income","Note":"Monthly Paycheck","Amount":4500.0,"Type":"Income"},
    {"Date":"1/3/2026","Account":"Credit Card","Category":"Personal","Note":"Barber Shop","Amount":16.9,"Type":"Expense"},
    {"Date":"1/4/2026","Account":"Cash","Category":"Health","Note":"Painkillers","Amount":71.75,"Type":"Expense"},
    {"Date":"1/5/2026","Account":"Main Bank","Category":"Rent","Note":"Monthly Rent Payment","Amount":1600.0,"Type":"Expense"},
    {"Date":"1/6/2026","Account":"Cash","Category":"Entertainment","Note":"Movie Tickets","Amount":7.76,"Type":"Expense"},
    {"Date":"1/7/2026","Account":"Credit Card","Category":"Housing","Note":"Plumbing Repair","Amount":92.37,"Type":"Expense"},
    {"Date":"1/8/2026","Account":"Main Bank","Category":"Utilities","Note":"Quarterly Bill","Amount":100.18,"Type":"Expense"},
    {"Date":"1/9/2026","Account":"Cash","Category":"Entertainment","Note":"PSN Subscription","Amount":42.5,"Type":"Expense"},
    {"Date":"1/10/2026","Account":"Main Bank","Category":"Utilities","Note":"Quarterly Bill","Amount":47.89,"Type":"Expense"},
    {"Date":"1/11/2026","Account":"Cash","Category":"Shopping","Note":"New Shirt","Amount":25.99,"Type":"Expense"},
    {"Date":"1/12/2026","Account":"Credit Card","Category":"Entertainment","Note":"Netflix","Amount":38.13,"Type":"Expense"},
    {"Date":"1/13/2026","Account":"Cash","Category":"Food","Note":"Weekly Groceries","Amount":82.23,"Type":"Expense"},
    {"Date":"1/14/2026","Account":"Cash","Category":"Shopping","Note":"Jeans","Amount":31.43,"Type":"Expense"},
    {"Date":"1/15/2026","Account":"Credit Card","Category":"Transportation","Note":"Uber to Work","Amount":104.56,"Type":"Expense"}
]

result = collection.insert_many(rows)
print(f"Inserted {len(result.inserted_ids)} documents into {collection.full_name}")
