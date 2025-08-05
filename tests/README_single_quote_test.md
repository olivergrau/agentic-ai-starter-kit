# Single Quote Request Test

## Usage

The `test_one_quote_request.py` script processes a single quote request through the complete orchestrator pipeline.

### Basic Usage

```bash
# Test with quote.txt and initialize database
python tests/test_one_quote_request.py quote.txt 2025-08-01

# Test without reinitializing database (use existing data)
python tests/test_one_quote_request.py --no-init-db quote.txt 2025-08-01

# Test with a different quote file
python tests/test_one_quote_request.py data/sample_quote.txt 2025-07-15
```

### Parameters

- `quote_file`: Path to the text file containing the quote request
- `request_date`: Date in YYYY-MM-DD format when the quote was requested
- `--no-init-db`: Optional flag to skip database initialization

### Features

✅ **Complete Pipeline Testing**: Tests all 5 agents (Parser, Inventory, Quote, Order, Reporting)
✅ **Financial Tracking**: Shows before/after financial state and changes
✅ **Detailed Output**: Comprehensive logging with emojis for easy reading
✅ **Error Handling**: Graceful error handling with detailed stack traces
✅ **Quote Details**: Shows line items, pricing, and totals when successful
✅ **CLI Interface**: Easy command-line usage with help and examples

### Output

The script provides:
- Initial financial state (cash, inventory, total assets)
- Quote processing results with detailed line items
- Final financial state with changes highlighted
- Processing status and response summary
- Business impact analysis

### Examples

```bash
# Process the included quote.txt for August 1st, 2025
cd /path/to/project
python tests/test_one_quote_request.py quote.txt 2025-08-01

# Use existing database data (no reinitialization)
python tests/test_one_quote_request.py --no-init-db quote.txt 2025-08-01
```

### Sample Output

```
🏗️  Polaris Outfitting Co. Company - SINGLE QUOTE REQUEST TEST
======================================================================

🔧 Initializing Database...
✅ Database initialized successfully

📂 Loading quote request from: space_mission_quote.txt
✅ Quote request loaded successfully
📝 Request preview: I would like to request the following space mission supplies for our upcoming lunar base expansion p...
📅 Request Date: 2025-08-10

💰 Initial Financial State (2025-08-10):
   Cash Balance: $42385.65
   Inventory Value: $7614.35
   Total Assets: $50000.00

🤖 Initializing Multi-Agent Orchestrator...
✅ Orchestrator initialized with 5 agents

🚀 Processing quote request...
----------------------------------------------------------------------
🔄 Running orchestrator pipeline...

============================================================
📋 STEP: PARSE
============================================================
📝 Original Request: I would like to request the following space mission supplies for our upcoming lunar base expansion project:

- 150 thermal insulation sheets for habitat module construction
- 25 EVA helmet lights for our astronaut operations
- 8 field diagnostic scanners for equipment maintenance
- 50 portable power nodes for mobile power requirements
- 12 cryo-storage units for biological sample preservation
- 200 polymer containment bags for waste management
- 15 mission data tablets for crew coordination

This equipment is critical for our September 2025 lunar mission deployment. I need these supplies delivered by August 25, 2025 to our Kennedy Space Center facility for pre-launch preparation.

Thank you for your prompt attention to this space mission supply request.

Best regards,
Commander Sarah Chen
Lunar Operations Division
NASA Johnson Space Center
📅 Quote Request Date: 2025-08-10
✅ Successfully parsed 7 items:
   • Thermal insulation sheet: 150 units
   • EVA helmet light: 25 units
   • Field diagnostic scanner: 8 units
   • Portable power node: 50 units
   • Cryo-storage unit: 12 units
   • Polymer containment bag: 200 units
   • Mission data tablet: 15 units
   No unmatched items found.
🚚 Requested Delivery Date: 2025-08-25
FUNC (get_supplier_delivery_date): Calculating for qty 150 from date string '2025-08-10'
FUNC (get_supplier_delivery_date): Calculating for qty 25 from date string '2025-08-10'
FUNC (get_supplier_delivery_date): Calculating for qty 8 from date string '2025-08-10'
FUNC (get_supplier_delivery_date): Calculating for qty 50 from date string '2025-08-10'
FUNC (get_supplier_delivery_date): Calculating for qty 200 from date string '2025-08-10'

============================================================
📋 STEP: CHECK_INVENTORY
============================================================
💰 Current Financial Position:
   Cash Balance: $40,407.15
   Inventory Value: $9,592.85
   Total Assets: $50,000.00

📦 Inventory Analysis:
   ✅ Fulfillable Items: 7
   ❌ Unfulfillable Items: 0
   🔄 Restockable Items: 5
   📋 Stock Orders Created: 5

✅ Items Available for Fulfillment:
   • Cryo-storage unit: 12 units
   • Mission data tablet: 15 units
   • Thermal insulation sheet: 150 units
   • EVA helmet light: 25 units
   • Field diagnostic scanner: 8 units
   • Portable power node: 50 units
   • Polymer containment bag: 200 units

🔄 Items Available for Restocking:
   • Thermal insulation sheet: Can be restocked from suppliers
   • EVA helmet light: Can be restocked from suppliers
   • Field diagnostic scanner: Can be restocked from suppliers
   • Portable power node: Can be restocked from suppliers
   • Polymer containment bag: Can be restocked from suppliers

📋 Stock Orders Created:
   • Thermal insulation sheet: 150 units @ $412.50
   • EVA helmet light: 25 units @ $150.00
   • Field diagnostic scanner: 8 units @ $336.00
   • Portable power node: 50 units @ $900.00
   • Polymer containment bag: 200 units @ $180.00
   💰 Total Order Cost: $1978.50

🎯 Status: ALL ITEMS AVAILABLE - Full order possible
   📋 Note: 5 items required restocking (orders placed)

============================================================
📋 STEP: GENERATE_QUOTE
============================================================
💰 Quote Generated:
   Total Amount: $4,506.52 USD
   Line Items: 7

📋 Quote Breakdown:
   • Cryo-storage unit: 12 units @ $57.96/unit
     Subtotal: $695.52
   • Mission data tablet: 15 units @ $36.05/unit
     Subtotal: $540.75
   • Thermal insulation sheet: 150 units @ $4.04/unit
     Discount: 10.0%
     Subtotal: $606.15
   • EVA helmet light: 25 units @ $11.36/unit
     Subtotal: $284.00
   • Field diagnostic scanner: 8 units @ $75.55/unit
     Subtotal: $604.40
   • Portable power node: 50 units @ $29.97/unit
     Subtotal: $1498.50
   • Polymer containment bag: 200 units @ $1.39/unit
     Discount: 10.0%
     Subtotal: $277.20

📊 Quote Summary:
   Total Quantity: 460 units
   Average Price per Unit: $9.80

📝 Notes: 10% bulk discount applied for Thermal insulation sheet and Polymer containment bag orders based on quantity.

============================================================
📋 STEP: FINALIZE_ORDER
============================================================
📋 Order Processing:
   ✅ Order Status: SUCCESSFUL
   🔢 Order ID: ORD-1754411432
   📝 Message: Order completed successfully. Created 7 transactions. Total: $4506.52.

💰 Financial Impact:
   Revenue Generated: $4,506.52
   Updated Cash Balance: $44,913.67
   Updated Inventory Value: $6,864.35
   Updated Total Assets: $51,778.02

============================================================
📋 STEP: REPORTING
============================================================
📊 Final Business Report:
   Status: SUCCESS
   Message: Order placed successfully.

💼 Business Metrics:
   Order Value: $4,506.52
   Items Sold: 7
   ✅ Transaction: COMPLETED

💰 Quote Details:
   Total Price: $4506.52
   Line Items: 7
   1. Cryo-storage unit: 12 units @ $57.96
   2. Mission data tablet: 15 units @ $36.05
   3. Thermal insulation sheet: 150 units @ $4.04
   4. EVA helmet light: 25 units @ $11.36
   5. Field diagnostic scanner: 8 units @ $75.55
   6. Portable power node: 50 units @ $29.97
   7. Polymer containment bag: 200 units @ $1.39

✅ Status: success
📝 Message: Order placed successfully.

📊 Final Financial State (2025-08-10):
   Cash Balance: $44913.67 (change: +2528.02)
   Inventory Value: $6864.35 (change: -750.00)
   Total Assets: $51778.02 (change: +1778.02)

======================================================================
🏆 SINGLE QUOTE REQUEST TEST SUMMARY
======================================================================
📂 Quote File: space_mission_quote.txt
📅 Request Date: 2025-08-10
🎯 Processing Status: SUCCESS
📝 Response: [SUCCESS] Order placed successfully.
💰 Quote Generated: $4506.52 for 7 items
📈 Financial Impact:
   Cash: +2528.02
   Inventory: -750.00
   Net Assets: +1778.02

🎯 Single quote request test completed!
```
