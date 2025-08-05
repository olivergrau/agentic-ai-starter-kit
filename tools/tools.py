import pandas as pd
import os
import time
import dotenv
from datetime import datetime, timedelta
from typing import Dict, List, Union

# Import database components from db.py
from tools.db import db_engine, INITIAL_CASH_BALANCE, mission_supplies, generate_sample_inventory, init_database

def create_transaction(
    item_name: str,
    transaction_type: str,
    quantity: int,
    price: float,
    date: Union[str, datetime],
) -> int:
    """
    This function records a transaction of type 'stock_orders' or 'sales' with a specified
    item name, quantity, total price, and transaction date into the 'transactions' table of the database.

    Args:
        item_name (str): The name of the item involved in the transaction.
        transaction_type (str): Either 'stock_orders' or 'sales'.
        quantity (int): Number of units involved in the transaction.
        price (float): Total price of the transaction.
        date (str or datetime): Date of the transaction in ISO 8601 format.

    Returns:
        int: The ID of the newly inserted transaction.

    Raises:
        ValueError: If `transaction_type` is not 'stock_orders' or 'sales'.
        Exception: For other database or execution errors.
    """
    try:
        # Convert datetime to ISO string if necessary
        date_str = date.isoformat() if isinstance(date, datetime) else date

        # Validate transaction type
        if transaction_type not in {"stock_orders", "sales"}:
            raise ValueError("Transaction type must be 'stock_orders' or 'sales'")

        # Prepare transaction record as a single-row DataFrame
        transaction = pd.DataFrame([{
            "item_name": item_name,
            "transaction_type": transaction_type,
            "units": quantity,
            "price": price,
            "transaction_date": date_str,
        }])

        # Insert the record into the database
        transaction.to_sql("transactions", db_engine, if_exists="append", index=False)

        # Fetch and return the ID of the inserted row
        result = pd.read_sql("SELECT last_insert_rowid() as id", db_engine)
        return int(result.iloc[0]["id"])

    except Exception as e:
        print(f"Error creating transaction: {e}")
        raise

def get_all_inventory(as_of_date: str) -> Dict[str, Dict]:
    """
    Retrieve a snapshot of available inventory as of a specific date.

    This function calculates the net quantity of each item by summing 
    all stock orders and subtracting all sales up to and including the given date.
    It also includes buy price, sell price, and category information from the inventory table.

    Only items with positive stock are included in the result.

    Args:
        as_of_date (str): ISO-formatted date string (YYYY-MM-DD) representing the inventory cutoff.

    Returns:
        Dict[str, Dict]: A dictionary mapping item names to their details:
            {
                "item_name": {
                    "stock": int,
                    "buy_unit_price": float,
                    "sell_unit_price": float,
                    "category": str
                }
            }
    """
    # SQL query to compute stock levels per item as of the given date
    # with buy price, sell price, and category from inventory table
    query = """
        SELECT
            t.item_name,            
            SUM(CASE
                WHEN t.transaction_type = 'stock_orders' THEN t.units
                WHEN t.transaction_type = 'sales' THEN -t.units
                ELSE 0
            END) as stock,
            i.buy_unit_price,
            i.sell_unit_price,
            i.category
        FROM transactions t
        LEFT JOIN inventory i ON t.item_name = i.item_name
        WHERE t.item_name IS NOT NULL
        AND t.transaction_date <= :as_of_date
        GROUP BY t.item_name, i.buy_unit_price, i.sell_unit_price, i.category
        HAVING stock > 0
    """

    # Execute the query with the date parameter
    result = pd.read_sql(query, db_engine, params={"as_of_date": as_of_date})

    # Convert the result into a nested dictionary
    inventory_dict = {}
    for _, row in result.iterrows():
        inventory_dict[row["item_name"]] = {
            "stock": int(row["stock"]),
            "buy_unit_price": float(row["buy_unit_price"]) if row["buy_unit_price"] is not None else 0.0,
            "sell_unit_price": float(row["sell_unit_price"]) if row["sell_unit_price"] is not None else 0.0,
            "category": row["category"] if row["category"] is not None else "unknown"
        }
    
    return inventory_dict

def get_stock_level(item_name: str, as_of_date: Union[str, datetime]) -> pd.DataFrame:
    """
    Retrieve the stock level of a specific item as of a given date.

    This function calculates the net stock by summing all 'stock_orders' and 
    subtracting all 'sales' transactions for the specified item up to the given date.

    Args:
        item_name (str): The name of the item to look up.
        as_of_date (str or datetime): The cutoff date (inclusive) for calculating stock.

    Returns:
        pd.DataFrame: A single-row DataFrame with columns 'item_name' and 'current_stock'.
    """
    # Convert date to ISO string format if it's a datetime object
    if isinstance(as_of_date, datetime):
        as_of_date = as_of_date.isoformat()

    # SQL query to compute net stock level for the item
    stock_query = """
        SELECT
            item_name,
            COALESCE(SUM(CASE
                WHEN transaction_type = 'stock_orders' THEN units
                WHEN transaction_type = 'sales' THEN -units
                ELSE 0
            END), 0) AS current_stock
        FROM transactions
        WHERE item_name = :item_name
        AND transaction_date <= :as_of_date
    """

    # Execute query and return result as a DataFrame
    return pd.read_sql(
        stock_query,
        db_engine,
        params={"item_name": item_name, "as_of_date": as_of_date},
    )

def get_buy_unit_price(item_name: str) -> pd.DataFrame:
    """
    Retrieve the buy unit price of a specific item from the inventory table.

    This function queries the inventory table to get the buy unit price for the specified item.
    Buy prices are assumed to be static in the current implementation.

    Args:
        item_name (str): The name of the item to look up.        

    Returns:
        pd.DataFrame: A single-row DataFrame with columns 'item_name' and 'buy_unit_price'.
                     Returns empty DataFrame if item is not found.
    """
    
    # SQL query to get buy unit price for the item from inventory table
    price_query = """
        SELECT
            item_name,
            buy_unit_price
        FROM inventory
        WHERE item_name = :item_name
    """

    # Execute query and return result as a DataFrame
    return pd.read_sql(
        price_query,
        db_engine,
        params={"item_name": item_name},
    )

def get_sell_unit_price(item_name: str) -> pd.DataFrame:
    """
    Retrieve the sell unit price of a specific item from the inventory table.

    This function queries the inventory table to get the sell unit price for the specified item.
    Sell prices are assumed to be static in the current implementation.

    Args:
        item_name (str): The name of the item to look up.        

    Returns:
        pd.DataFrame: A single-row DataFrame with columns 'item_name' and 'sell_unit_price'.
                     Returns empty DataFrame if item is not found.
    """
    
    # SQL query to get sell unit price for the item from inventory table
    price_query = """
        SELECT
            item_name,
            sell_unit_price
        FROM inventory
        WHERE item_name = :item_name
    """

    # Execute query and return result as a DataFrame
    return pd.read_sql(
        price_query,
        db_engine,
        params={"item_name": item_name},
    )

def get_unit_price(item_name: str) -> pd.DataFrame:
    """
    Retrieve both buy and sell unit prices of a specific item from the inventory table.

    This function queries the inventory table to get both prices for the specified item.
    Prices are assumed to be static in the current implementation.

    Args:
        item_name (str): The name of the item to look up.        

    Returns:
        pd.DataFrame: A single-row DataFrame with columns 'item_name', 'buy_unit_price', and 'sell_unit_price'.
                     Returns empty DataFrame if item is not found.
    """
    
    # SQL query to get both unit prices for the item from inventory table
    price_query = """
        SELECT
            item_name,
            buy_unit_price,
            sell_unit_price
        FROM inventory
        WHERE item_name = :item_name
    """

    # Execute query and return result as a DataFrame
    return pd.read_sql(
        price_query,
        db_engine,
        params={"item_name": item_name},
    )

def get_supplier_delivery_date(input_date_str: str, quantity: int) -> str:
    """
    Estimate the supplier delivery date based on the requested order quantity and a starting date.

    Delivery lead time increases with order size:
        - ≤10 units: same day
        - 11–100 units: 1 day
        - 101–1000 units: 4 days
        - >1000 units: 7 days

    Args:
        input_date_str (str): The starting date in ISO format (YYYY-MM-DD).
        quantity (int): The number of units in the order.

    Returns:
        str: Estimated delivery date in ISO format (YYYY-MM-DD).
    """
    # Debug log (comment out in production if needed)
    print(f"FUNC (get_supplier_delivery_date): Calculating for qty {quantity} from date string '{input_date_str}'")

    # Attempt to parse the input date
    try:
        input_date_dt = datetime.fromisoformat(input_date_str.split("T")[0])
    except (ValueError, TypeError):
        # Fallback to current date on format error
        print(f"WARN (get_supplier_delivery_date): Invalid date format '{input_date_str}', using today as base.")
        input_date_dt = datetime.now()

    # Determine delivery delay based on quantity
    if quantity <= 10:
        days = 0
    elif quantity <= 100:
        days = 1
    elif quantity <= 1000:
        days = 4
    else:
        days = 7

    # Add delivery days to the starting date
    delivery_date_dt = input_date_dt + timedelta(days=days)

    # Return formatted delivery date
    return delivery_date_dt.strftime("%Y-%m-%d")

def get_cash_balance(as_of_date: Union[str, datetime]) -> float:
    """
    Calculate the current cash balance as of a specified date.

    The balance is computed by subtracting total stock purchase costs ('stock_orders')
    from total revenue ('sales') recorded in the transactions table up to the given date.

    Args:
        as_of_date (str or datetime): The cutoff date (inclusive) in ISO format or as a datetime object.

    Returns:
        float: Net cash balance as of the given date. Returns 0.0 if no transactions exist or an error occurs.
    """

    initial_cash = INITIAL_CASH_BALANCE

    try:
        # Convert date to ISO format if it's a datetime object
        if isinstance(as_of_date, datetime):
            as_of_date = as_of_date.isoformat()

        # Query all transactions on or before the specified date
        transactions = pd.read_sql(
            "SELECT * FROM transactions WHERE transaction_date <= :as_of_date",
            db_engine,
            params={"as_of_date": as_of_date},
        )

        # Compute the difference between sales and stock purchases
        if not transactions.empty:
            total_sales = transactions.loc[transactions["transaction_type"] == "sales", "price"].sum()
            total_purchases = transactions.loc[transactions["transaction_type"] == "stock_orders", "price"].sum()
            return float(initial_cash +total_sales - total_purchases)

        return 0.0

    except Exception as e:
        print(f"Error getting cash balance: {e}")
        return 0.0


def generate_financial_report(as_of_date: Union[str, datetime]) -> Dict:
    """
    Generate a complete financial report for the company as of a specific date.

    This includes:
    - Cash balance
    - Inventory valuation (using buy prices)
    - Estimated inventory revenue (using sell prices)
    - Combined asset total
    - Itemized inventory breakdown
    - Top 5 best-selling products

    Args:
        as_of_date (str or datetime): The date (inclusive) for which to generate the report.

    Returns:
        Dict: A dictionary containing the financial report fields:
            - 'as_of_date': The date of the report
            - 'cash_balance': Total cash available
            - 'inventory_value': Total value of inventory (at buy prices)
            - 'estimated_inventory_revenue': Estimated revenue if all inventory sold (at sell prices)
            - 'total_assets': Combined cash and inventory value
            - 'inventory_summary': List of items with stock and valuation details
            - 'top_selling_products': List of top 5 products by revenue
    """
    # Normalize date input
    if isinstance(as_of_date, datetime):
        as_of_date = as_of_date.isoformat()

    # Get current cash balance
    cash = get_cash_balance(as_of_date)

    # Get current inventory snapshot
    inventory_df = pd.read_sql("SELECT * FROM inventory", db_engine)
    inventory_value = 0.0
    estimated_inventory_revenue = 0.0
    inventory_summary = []

    # Compute total inventory value and summary by item
    for _, item in inventory_df.iterrows():
        stock_info = get_stock_level(item["item_name"], as_of_date)
        stock = stock_info["current_stock"].iloc[0]
        item_value = stock * item["buy_unit_price"]
        estimated_revenue = stock * item["sell_unit_price"]
        inventory_value += item_value
        estimated_inventory_revenue += estimated_revenue

        inventory_summary.append({
            "item_name": item["item_name"],
            "stock": stock,
            "buy_unit_price": item["buy_unit_price"],
            "sell_unit_price": item["sell_unit_price"],
            "value": item_value,
            "estimated_revenue": estimated_revenue,
        })

    # Identify top-selling products by revenue
    top_sales_query = """
        SELECT item_name, SUM(units) as total_units, SUM(price) as total_revenue
        FROM transactions
        WHERE transaction_type = 'sales' AND transaction_date <= :date AND item_name IS NOT NULL
        GROUP BY item_name
        ORDER BY total_revenue DESC
        LIMIT 5
    """
    top_sales = pd.read_sql(top_sales_query, db_engine, params={"date": as_of_date})
    top_selling_products = top_sales.to_dict(orient="records")

    return {
        "as_of_date": as_of_date,
        "cash_balance": cash,
        "inventory_value": inventory_value,
        "estimated_inventory_revenue": estimated_inventory_revenue,
        "total_assets": cash + inventory_value,
        "inventory_summary": inventory_summary,
        "top_selling_products": top_selling_products,
    }


def search_quote_history(search_terms: List[str], limit: int = 5) -> List[Dict]:
    """
    Retrieve a list of historical quotes that match any of the provided search terms.

    The function searches both the original customer request (from `quote_requests`) and
    the explanation for the quote (from `quotes`) for each keyword. Results are sorted by
    most recent order date and limited by the `limit` parameter.

    Args:
        search_terms (List[str]): List of terms to match against customer requests and explanations.
        limit (int, optional): Maximum number of quote records to return. Default is 5.

    Returns:
        List[Dict]: A list of matching quotes, each represented as a dictionary with fields:
            - original_request
            - total_amount
            - quote_explanation
            - job_type
            - order_size
            - event_type
            - order_date
    """
    conditions = []
    params = {}

    # Build SQL WHERE clause using LIKE filters for each search term
    for i, term in enumerate(search_terms):
        param_name = f"term_{i}"
        conditions.append(
            f"(LOWER(qr.response) LIKE :{param_name} OR "
            f"LOWER(q.quote_explanation) LIKE :{param_name})"
        )
        params[param_name] = f"%{term.lower()}%"

    # Combine conditions; fallback to always-true if no terms provided
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    # Final SQL query to join quotes with quote_requests
    query = f"""
        SELECT
            qr.response AS original_request,
            q.total_amount,
            q.quote_explanation,
            q.job_type,
            q.order_size,
            q.event_type,
            q.order_date
        FROM quotes q
        JOIN quote_requests qr ON q.request_id = qr.id
        WHERE {where_clause}
        ORDER BY q.order_date DESC
        LIMIT {limit}
    """

    # Use pandas for consistent connection management
    try:
        result_df = pd.read_sql(query, db_engine, params=params)
        return result_df.to_dict(orient="records")
    except Exception as e:
        print(f"Error searching quote history: {e}")
        return []
