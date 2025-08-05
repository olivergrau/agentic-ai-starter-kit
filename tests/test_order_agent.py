# set cwd directory to the root of the project
import os
import sys
from pathlib import Path

# Get the absolute path to the current file (inside tests/)
current_file_path = Path(__file__).resolve()

# Set working directory to the parent of 'tests'
project_root = current_file_path.parent.parent
os.chdir(project_root)

# (Optional) Add root to sys.path if you want to import project modules directly
sys.path.insert(0, str(project_root))

print(f"Changed working directory to: {os.getcwd()}")

from agents.order_agent import OrderAgent
from protocol import QuoteItem, QuoteResult
from dotenv import load_dotenv

load_dotenv()

from tools.db import db_engine, init_database

# Initialize the database engine and create sample inventory
print("Initializing Polaris Outfitting database and generating space mission inventory...\n")
init_database(db_engine=db_engine, seed=0, debug=True)

print("Space mission supply inventory generated successfully.\n")

# --- Create a test quote result to process ---
test_line_items = [
    QuoteItem(
        name="Thermal insulation sheet", 
        quantity=100, 
        unit="sheets",
        unit_price=2.75,
        discount_percent=10.0,
        subtotal=247.50  # 100 * 2.75 * 0.9 (10% discount)
    ),
    QuoteItem(
        name="EVA helmet light", 
        quantity=25, 
        unit="units",
        unit_price=6.00,
        discount_percent=0.0,
        subtotal=150.00  # 25 * 6.00
    ),
    QuoteItem(
        name="Portable power node", 
        quantity=200, 
        unit="units",
        unit_price=18.00,
        discount_percent=10.0,
        subtotal=3240.00  # 200 * 18.00 * 0.9 (10% discount)
    )
]

test_quote_result = QuoteResult(
    success=True,
    total_price=3637.50,
    currency="USD",
    line_items=test_line_items,
    notes="Bulk discounts applied for space mission orders >= 100 units."
)

print("Testing OrderAgent with quote result...\n")
print("Quote Result:")
print(f"  Total Price: ${test_quote_result.total_price}")
print(f"  Currency: {test_quote_result.currency}")
print(f"  Line Items:")
for item in test_quote_result.line_items:
    discount_text = f" ({item.discount_percent}% discount)" if item.discount_percent and item.discount_percent > 0 else ""
    print(f"    • {item.name}: {item.quantity} @ ${item.unit_price:.2f}{discount_text} = ${item.subtotal:.2f}")
print()

quote_request_date = "2025-08-01"  # Example date, adjust as needed
print(f"Quote Request Date: {quote_request_date}\n")

# --- Run the agent ---
print("Running OrderAgent test...\n")

# Create fresh order agent instance
order_agent = OrderAgent()

result = order_agent.run(test_quote_result, quote_request_date=quote_request_date)

# --- Pretty print result ---
import json
print("OrderAgent Output:")
print(result.model_dump_json(indent=2))

# --- Additional analysis ---
print("\n" + "="*50)
print("ORDER ANALYSIS")
print("="*50)
print(f"✅ Order Success: {result.success}")
print(f"📦 Order ID: {result.order_id}")
print(f"📝 Message: {result.message}")

print("\n✅ OrderAgent test completed!")
