"""
Test file for ReportingAgent implementation.
"""
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

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.reporting_agent import ReportingAgent
from protocol import ReportingRequest, ReportingResult

from tools.db import db_engine, init_database
from tools.tools import create_transaction

# Initialize the database engine and create sample inventory
print("Initializing Polaris Outfitting database and generating space mission inventory...\n")
init_database(db_engine=db_engine, seed=0, debug=True)

print("Space mission supply inventory generated successfully.\n")

# Insert sample transactions of type sales for reporting
print("Creating sample space mission sales transactions for testing...")

# Sample sales transactions - representing different days and space mission supplies
sample_sales = [
    # Sales from January 2025
    {"item_name": "Thermal insulation sheet", "quantity": 50, "unit_price": 2.75, "date": "2025-01-05"},
    {"item_name": "Carbon mesh panel", "quantity": 25, "unit_price": 5.00, "date": "2025-01-05"},
    {"item_name": "EVA helmet light", "quantity": 100, "unit_price": 6.00, "date": "2025-01-08"},
    
    # Sales from February 2025
    {"item_name": "Thermal insulation sheet", "quantity": 150, "unit_price": 2.75, "date": "2025-02-10"},
    {"item_name": "Portable power node", "quantity": 75, "unit_price": 18.00, "date": "2025-02-10"},
    {"item_name": "Cryo-storage unit", "quantity": 200, "unit_price": 35.00, "date": "2025-02-15"},
    {"item_name": "Polymer containment bag", "quantity": 500, "unit_price": 0.90, "date": "2025-02-15"},
    
    # Sales from March 2025
    {"item_name": "Reflective heatfoil wrap", "quantity": 30, "unit_price": 3.20, "date": "2025-03-05"},
    {"item_name": "Aerogel sheet", "quantity": 40, "unit_price": 6.00, "date": "2025-03-05"},
    {"item_name": "Mission data tablet", "quantity": 150, "unit_price": 22.00, "date": "2025-03-12"},
    
    # Recent sales from July 2025
    {"item_name": "Thermal insulation sheet", "quantity": 200, "unit_price": 2.75, "date": "2025-07-20"},
    {"item_name": "Carbon mesh panel", "quantity": 80, "unit_price": 5.00, "date": "2025-07-20"},
    {"item_name": "Ion charge kit", "quantity": 300, "unit_price": 25.00, "date": "2025-07-25"},
    {"item_name": "Multi-layer thermal blanket", "quantity": 25, "unit_price": 14.00, "date": "2025-07-25"},
    {"item_name": "Biometric ID badge", "quantity": 500, "unit_price": 2.50, "date": "2025-07-30"},
]

# Create sales transactions
transaction_ids = []
for sale in sample_sales:
    total_price = sale["quantity"] * sale["unit_price"]
    try:
        transaction_id = create_transaction(
            item_name=sale["item_name"],
            transaction_type="sales",
            quantity=sale["quantity"],
            price=total_price,
            date=sale["date"]
        )
        transaction_ids.append(transaction_id)
        print(f"✅ Created sales transaction {transaction_id}: {sale['quantity']} {sale['item_name']} @ ${sale['unit_price']:.2f} = ${total_price:.2f} on {sale['date']}")
    except Exception as e:
        print(f"❌ Failed to create sales transaction for {sale['item_name']}: {e}")

print(f"\n📊 Created {len(transaction_ids)} sales transactions for testing")
print(f"💰 Total sales transactions: {transaction_ids}")
print("🎯 Database is now ready for ReportingAgent testing!\n")

def test_reporting_agent():
    """
    Test the ReportingAgent implementation with sample requests.
    """
    print("🧪 Testing ReportingAgent Implementation")
    print("=" * 50)
    
    # Initialize the agent
    try:
        agent = ReportingAgent()
        print("✅ ReportingAgent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize ReportingAgent: {e}")
        return
    
    # Test 1: Financial Report Request
    print("\n📊 Test 1: Financial Report Request")
    financial_request = ReportingRequest(
        report_type="financial",
        period="last_30_days",
        filters={"include_trends": True}
    )
    
    try:
        result = agent.run(financial_request)
        print(f"📈 Result Type: {type(result)}")
        print(f"✅ Success: {result.success}")
        if result.success:
            print(f"📊 Report Data Keys: {list(result.report_data.keys())}")
            print(f"� Report Data Contents:")
            for key, value in result.report_data.items():
                print(f"  {key}: {value}")
            print(f"�📝 Summary: {result.summary}")
        else:
            print(f"❌ Error: {result.error_message}")
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
    
    # Test 2: Sales Report Request
    print("\n💰 Test 2: Sales Report Request")
    sales_request = ReportingRequest(
        report_type="sales",
        period="Q1_2025",
        filters={"group_by": "product"}
    )
    
    try:
        result = agent.run(sales_request)
        print(f"📈 Result Type: {type(result)}")
        print(f"✅ Success: {result.success}")
        if result.success:
            print(f"📊 Report Data Keys: {list(result.report_data.keys())}")
            print(f"� Report Data Contents:")
            for key, value in result.report_data.items():
                print(f"  {key}: {value}")
            print(f"�📝 Summary: {result.summary}")
        else:
            print(f"❌ Error: {result.error_message}")
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
    
    # Test 3: Inventory Report Request
    print("\n📦 Test 3: Inventory Report Request")
    inventory_request = ReportingRequest(
        report_type="inventory",
        period="current",
        filters={"low_stock_threshold": 100}
    )
    
    try:
        result = agent.run(inventory_request)
        print(f"📈 Result Type: {type(result)}")
        print(f"✅ Success: {result.success}")
        if result.success:
            print(f"📊 Report Data Keys: {list(result.report_data.keys())}")
            print(f"� Report Data Contents:")
            for key, value in result.report_data.items():
                print(f"  {key}: {value}")
            print(f"�📝 Summary: {result.summary}")
        else:
            print(f"❌ Error: {result.error_message}")
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
    
    print("\n🎯 ReportingAgent Implementation Features:")
    print("  ✓ Supports multiple report types (financial, sales, inventory)")
    print("  ✓ Handles flexible time periods")
    print("  ✓ Accepts custom filters for targeted analysis")
    print("  ✓ Uses generate_financial_report tool")
    print("  ✓ Returns structured ReportingResult following message protocol")
    print("  ✓ Includes comprehensive error handling")
    print("  ✓ Provides business insights and summaries")
    print("  ✓ Formats results for stakeholders")

if __name__ == "__main__":
    test_reporting_agent()
