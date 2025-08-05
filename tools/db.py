import pandas as pd
import numpy as np
import ast
from datetime import datetime
from typing import Dict, List
from sqlalchemy import create_engine, Engine

INITIAL_CASH_BALANCE = 50000.0

# Create an SQLite database
db_engine = create_engine("sqlite:///db/polaris_outfitting.db")

# List containing the different kinds of missions 
# Inventory for Polaris Outfitting Co. – Lunar & Orbital Supply Components
mission_supplies = [
    # Materials (priced per unit)
    {"item_name": "Carbon mesh panel",                  "category": "material",         "unit_price": 5.00},
    {"item_name": "Cryo-sealant cartridge",             "category": "material",         "unit_price": 3.50},
    {"item_name": "Thermal insulation sheet",           "category": "material",         "unit_price": 2.75},
    {"item_name": "Reflective heatfoil wrap",           "category": "material",         "unit_price": 3.20},
    {"item_name": "Nano-fiber bonding strip",           "category": "material",         "unit_price": 1.50},
    {"item_name": "Pressure-rated hull plate",          "category": "material",         "unit_price": 7.25},
    {"item_name": "EVA-rated patch film",               "category": "material",         "unit_price": 2.00},
    {"item_name": "Structural foam tile",               "category": "material",         "unit_price": 1.80},
    {"item_name": "Polymer containment bag",            "category": "material",         "unit_price": 0.90},
    {"item_name": "Radiation barrier mesh",             "category": "material",         "unit_price": 4.40},
    {"item_name": "Aerogel sheet",                      "category": "material",         "unit_price": 6.00},
    {"item_name": "Solar panel film (roll)",            "category": "material",         "unit_price": 3.75},
    {"item_name": "Atmospheric seal strip",             "category": "material",         "unit_price": 1.10},

    # Equipment (priced per item)
    {"item_name": "Ion charge kit",                     "category": "equipment",        "unit_price": 25.00},
    {"item_name": "Portable power node",                "category": "equipment",        "unit_price": 18.00},
    {"item_name": "Modular light fixture",              "category": "equipment",        "unit_price": 8.50},
    {"item_name": "Cryo-storage unit",                  "category": "equipment",        "unit_price": 35.00},
    {"item_name": "Mission data tablet",                "category": "equipment",        "unit_price": 22.00},
    {"item_name": "Field diagnostic scanner",           "category": "equipment",        "unit_price": 42.00},
    {"item_name": "EVA helmet light",                   "category": "equipment",        "unit_price": 6.00},
    {"item_name": "Rapid-assemble toolset",             "category": "equipment",        "unit_price": 15.00},
    {"item_name": "Biometric ID badge",                 "category": "equipment",        "unit_price": 2.50},
    {"item_name": "Holographic label tags",             "category": "equipment",        "unit_price": 1.20},
    {"item_name": "Secure cargo case",                  "category": "equipment",        "unit_price": 12.00},
    {"item_name": "Compressed air canister",            "category": "equipment",        "unit_price": 10.00},
    {"item_name": "Environmental sensor puck",          "category": "equipment",        "unit_price": 7.00},

    # Large-format components (priced per unit)
    {"item_name": "Telescopic support beam",            "category": "large_component",  "unit_price": 55.00},
    {"item_name": "Deployable antenna array",           "category": "large_component",  "unit_price": 95.00},

    # Specialty gear
    {"item_name": "Hydrophobic coating kit",            "category": "specialty",        "unit_price": 12.00},
    {"item_name": "Zero-gravity adhesive pack",         "category": "specialty",        "unit_price": 6.50},
    {"item_name": "Multi-layer thermal blanket",        "category": "specialty",        "unit_price": 14.00},
    {"item_name": "Quantum marker dye",                 "category": "specialty",        "unit_price": 3.80},
]


def generate_sample_inventory(mission_supplies: list, coverage: float = 1.0, seed: int = 137) -> pd.DataFrame:
    """
    Generate inventory for exactly a specified percentage of items from the full mission supply list.

    This function randomly selects exactly `coverage` × N items from the `mission_supplies` list,
    and assigns each selected item:
    - a random stock quantity between 5 and 30,
    - a minimum stock level between 2 and 10,
    - buy_unit_price from the original unit_price,
    - sell_unit_price 60-90% higher than buy_unit_price.

    The random seed ensures reproducibility of selection and stock levels.

    Args:
        mission_supplies (list): A list of dictionaries, each representing a mission item with
                               keys 'item_name', 'category', and 'unit_price'.
        coverage (float, optional): Fraction of items to include in the inventory (default is 0.4, or 40%).
        seed (int, optional): Random seed for reproducibility (default is 137).

    Returns:
        pd.DataFrame: A DataFrame with the selected items and assigned inventory values, including:
                      - item_name
                      - category
                      - buy_unit_price
                      - sell_unit_price
                      - current_stock
                      - min_stock_level
    """
    # Ensure reproducible random output
    np.random.seed(seed)

    # Calculate number of items to include based on coverage
    num_items = int(len(mission_supplies) * coverage)

    # Randomly select item indices without replacement
    selected_indices = np.random.choice(
        range(len(mission_supplies)),
        size=num_items,
        replace=False
    )

    # Extract selected items from mission_supplies list
    selected_items = [mission_supplies[i] for i in selected_indices]

    # Construct inventory records
    inventory = []
    for item in selected_items:
        buy_price = item["unit_price"]
        sell_price = round(buy_price * np.random.uniform(1.60, 1.90), 2)
        
        inventory.append({
            "item_name": item["item_name"],
            "category": item["category"],
            "buy_unit_price": buy_price,
            "sell_unit_price": sell_price,
            "current_stock": np.random.randint(5, 30),  # Realistic stock range
            "min_stock_level": np.random.randint(2, 10)  # Reasonable threshold for reordering
        })

    # Return inventory as a pandas DataFrame
    return pd.DataFrame(inventory)


def init_database(db_engine: Engine, seed: int = 137, debug: bool = False) -> Engine:
    """
    Set up the Polaris Outfitting database with all required tables and initial records.

    Args:
        db_engine (Engine): A SQLAlchemy engine connected to the SQLite database.
        seed (int, optional): A random seed used to control reproducibility of inventory stock levels.
        debug (bool, optional): If True, prints out debug info including inventory and transactions.
                                Default is False.

    Returns:
        Engine: The same SQLAlchemy engine, after initializing all necessary tables and records.

    Raises:
        Exception: If an error occurs during setup, the exception is printed and raised.
    """
    try:
        # ----------------------------
        # 1. Create an empty 'transactions' table schema
        # ----------------------------
        transactions_schema = pd.DataFrame({
            "id": [],
            "item_name": [],
            "transaction_type": [],
            "units": [],
            "price": [],
            "transaction_date": [],
        })
        transactions_schema.to_sql("transactions", db_engine, if_exists="replace", index=False)

        # Set a consistent starting date
        initial_date = datetime(2025, 1, 1).isoformat()

        # ----------------------------
        # 2. Load and initialize 'quote_requests' table
        # ----------------------------
        quote_requests_df = pd.read_csv("data/quote_requests.csv")
        quote_requests_df["id"] = range(1, len(quote_requests_df) + 1)
        quote_requests_df.to_sql("quote_requests", db_engine, if_exists="replace", index=False)

        # ----------------------------
        # 3. Load and transform 'quotes' table
        # ----------------------------
        quotes_df = pd.read_csv("data/quotes.csv")
        quotes_df["request_id"] = range(1, len(quotes_df) + 1)
        quotes_df["order_date"] = initial_date

        if "request_metadata" in quotes_df.columns:
            quotes_df["request_metadata"] = quotes_df["request_metadata"].apply(
                lambda x: ast.literal_eval(x) if isinstance(x, str) else x
            )
            quotes_df["job_type"] = quotes_df["request_metadata"].apply(lambda x: x.get("job_type", ""))
            quotes_df["order_size"] = quotes_df["request_metadata"].apply(lambda x: x.get("order_size", ""))
            quotes_df["event_type"] = quotes_df["request_metadata"].apply(lambda x: x.get("event_type", ""))

        quotes_df = quotes_df[[
            "request_id", "total_amount", "quote_explanation",
            "order_date", "job_type", "order_size", "event_type"
        ]]
        quotes_df.to_sql("quotes", db_engine, if_exists="replace", index=False)

        # ----------------------------
        # 4. Generate inventory and seed stock
        # ----------------------------
        inventory_df = generate_sample_inventory(mission_supplies, seed=seed, coverage=1.0)

        if debug:
            print("\n--- Polaris INVENTORY CREATED ---")
            for _, row in inventory_df.iterrows():
                print(row.to_dict())

        initial_transactions = []

        for _, item in inventory_df.iterrows():
            initial_transactions.append({
                "item_name": item["item_name"],
                "transaction_type": "stock_orders",
                "units": item["current_stock"],
                "price": item["current_stock"] * item["buy_unit_price"],
                "transaction_date": initial_date,
            })

        if debug:
            print("\n--- INITIAL TRANSACTIONS ---")
            for tx in initial_transactions:
                print(tx)

        pd.DataFrame(initial_transactions).to_sql("transactions", db_engine, if_exists="append", index=False)
        inventory_df.to_sql("inventory", db_engine, if_exists="replace", index=False)

        return db_engine

    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
