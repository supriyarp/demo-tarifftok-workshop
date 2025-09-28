# 📊 Retail Tariff Data Viewer

A comprehensive data visualization tool for synthetic tariff and retail scenario planning datasets.

## 🚀 **Quick Access**

| Feature | Command | URL |
|---------|---------|-----|
| **CRUD Editor** (Recommended) | `python3 start_crud_system.py` | `http://localhost:5001` |
| **Read-Only Viewer** | `python3 start_web_server.py` | `http://localhost:5200` |
| **Manual CRUD Setup** | `python3 crud_server.py` | `http://localhost:5001` |

## 🚀 Quick Start

### 0. Install Dependencies
```bash
pip install -r requirements.txt
```
Or for minimal installation:
```bash
pip install pandas numpy
```

### Option 1: CRUD System (Recommended) - **Editable Data**
```bash
python3 start_crud_system.py
```
**Full-featured system with:**
- ✅ **Create, Edit, Delete rows** - Full data management
- ✅ **Data validation** - Real-time error checking
- ✅ **Real-time CSV updates** - Changes saved immediately
- ✅ **Interactive filtering** and export functionality
- 🌐 **Access at:** `http://localhost:5001`

### Option 2: Read-Only Viewer
```bash
# 1. Generate data
python3 "Generate synthetic datasets for tariff.py"

# 2. Generate HTML viewer
python3 generate_dynamic_html_viewer.py

# 3. View data
python3 start_web_server.py
```
**Simple viewer for:**
- 📊 Data viewing and filtering
- 📥 CSV export
- 🔄 Dynamic data loading
- 🌐 **Access at:** `http://localhost:5200`

## 🎯 **Quick Access to CRUD Editor**

### **One-Command Setup:**
```bash
python3 start_crud_system.py
```

### **Manual Setup:**
```bash
# 1. Generate data
python3 "Generate synthetic datasets for tariff.py"

# 2. Generate CRUD viewer
python3 generate_crud_html_viewer.py

# 3. Start CRUD server
python3 crud_server.py

# 4. Open browser to: http://localhost:5001
```

### **CRUD Features Available:**
- **➕ Add Rows** - Click "Add Row" button
- **✏️ Edit Rows** - Click edit icon on any row
- **🗑️ Delete Rows** - Click delete icon with confirmation
- **🔍 Filter Data** - Use dropdown filters for each column
- **📥 Export CSV** - Export filtered data
- **✅ Validation** - Real-time field validation

### **Access URLs:**
- **CRUD Editor:** `http://localhost:5001` (Port 5001)
- **Read-Only Viewer:** `http://localhost:5200` (Port 5200)

## 📖 **Detailed Usage Instructions**

### **CRUD System Usage (Recommended)**

#### **Step 1: Start the CRUD System**
```bash
python3 start_crud_system.py
```
This will:
- Generate synthetic data
- Create the CRUD HTML viewer
- Start the Flask server on port 5001
- Open your browser automatically

#### **Step 2: Using the CRUD Interface**
1. **Select a Table**: Choose from dropdown (products, suppliers, tariffs, etc.)
2. **View Data**: See paginated data (50 records per page)
3. **Navigate**: Use pagination controls at bottom
4. **Add New Row**: Click "Add Row" button
5. **Edit Row**: Click ✏️ icon on any row
6. **Delete Row**: Click 🗑️ icon (with confirmation)
7. **Filter Data**: Use dropdown filters for each column
8. **Export**: Click "Export CSV" to download filtered data

#### **Step 3: CRUD Operations**
- **Create**: Fill out the form and click "Save"
- **Read**: Data loads automatically with pagination
- **Update**: Edit form fields and click "Update"
- **Delete**: Confirm deletion in the popup dialog

### **Dynamic HTML Viewer Usage**

#### **Step 1: Start the Read-Only Viewer**
```bash
python3 start_web_server.py
```
This will:
- Start a simple HTTP server on port 5200
- Open the dynamic viewer in your browser

#### **Step 2: Using the Dynamic Viewer**
1. **Select a Table**: Choose from dropdown
2. **View Data**: See all data in interactive tables
3. **Filter Data**: Use dropdown filters for each column
4. **Clear Filters**: Click "Clear Filters" button
5. **Export Data**: Click "Export CSV" button
6. **Refresh**: Click "Refresh" to reload data

#### **Step 3: Features Available**
- **Real-time Loading**: Data loads from CSV files dynamically
- **Column Filtering**: Filter by any column value
- **Data Export**: Export filtered results to CSV
- **Responsive Design**: Works on mobile and desktop

## 🔄 **CRUD vs Dynamic Viewer Comparison**

| Feature | CRUD System | Dynamic Viewer |
|---------|-------------|----------------|
| **Data Editing** | ✅ Full CRUD (Create, Edit, Delete) | ❌ Read-only |
| **Data Validation** | ✅ Real-time validation | ❌ No validation |
| **Pagination** | ✅ 50 records per page | ❌ Shows all records |
| **Performance** | ✅ Fast loading | ⚠️ Slower with large datasets |
| **Data Updates** | ✅ Real-time CSV updates | ❌ No updates |
| **Server Required** | ✅ Flask server (port 5001) | ✅ HTTP server (port 5200) |
| **Setup Complexity** | ⚠️ Requires Flask installation | ✅ Simple HTTP server |
| **Use Case** | Data management & editing | Data viewing & analysis |

### **When to Use CRUD System:**
- ✅ You need to **edit, add, or delete** data
- ✅ You want **data validation** and error checking
- ✅ You're working with **large datasets** (pagination)
- ✅ You need **real-time updates** to CSV files
- ✅ You want a **professional data management** interface

### **When to Use Dynamic Viewer:**
- ✅ You only need to **view and analyze** data
- ✅ You want **simple setup** without dependencies
- ✅ You're doing **data exploration** and filtering
- ✅ You need **quick access** to data visualization
- ✅ You want **lightweight** solution

## 🚀 **Quick Reference Commands**

### **CRUD System Commands**
```bash
# Start complete CRUD system
python3 start_crud_system.py

# Manual CRUD setup
python3 "Generate synthetic datasets for tariff.py"
python3 generate_crud_html_viewer.py
python3 crud_server.py

# Access CRUD interface
open http://localhost:5001
```

### **Dynamic Viewer Commands**
```bash
# Start read-only viewer
python3 start_web_server.py

# Manual dynamic viewer setup
python3 "Generate synthetic datasets for tariff.py"
python3 generate_dynamic_html_viewer.py
python3 -m http.server 5200

# Access dynamic viewer
open http://localhost:5200/data_viewer_dynamic.html
```

### **Common Tasks**
```bash
# Generate new data
python3 "Generate synthetic datasets for tariff.py"

# Install dependencies
pip install -r requirements.txt

# Check server status
curl http://localhost:5001/api/tables  # CRUD server
curl http://localhost:5200/data_viewer_dynamic.html  # Dynamic viewer

# Stop servers
pkill -f crud_server.py
pkill -f "http.server"
```

## 📁 Project Structure

```
wwc_code/
├── README.md                                    # This file
├── requirements.txt                             # Python dependencies
├── DATA_QUICK_REFERENCE.md                     # Quick reference guide
├── FILTERING_DEMO.md                           # Filtering usage guide
├── QUICK_START.md                              # Quick start guide
├── Generate synthetic datasets for tariff.py    # Main data generator
├── generate_dynamic_html_viewer.py             # Dynamic HTML viewer generator
├── generate_crud_html_viewer.py               # CRUD HTML viewer generator
├── crud_server.py                             # Flask backend for CRUD operations
├── start_crud_system.py                       # CRUD system launcher
├── start_web_server.py                        # Web server launcher for dynamic viewer
├── update_data.py                              # Automated update script
├── data_viewer_dynamic.html                    # Dynamic HTML viewer
├── data_viewer_crud.html                      # CRUD-enabled HTML viewer
└── retail_tariff_data/                         # Generated CSV data
    ├── DATA_DICTIONARY.md                      # Complete data documentation
    ├── tariffs.csv                             # Tariff rates by country/type
    ├── products.csv                            # Product catalog
    ├── suppliers.csv                           # Supplier information
    ├── markets.csv                             # Destination markets
    ├── cost_transit.csv                        # Shipping lanes & costs
    ├── sales_daily.csv                         # Daily sales data
    └── sales_weekly.csv                        # Weekly sales data
```

## 🔄 Dynamic Data Loading

### When Adding New Synthetic Data

1. **Modify the data generator** (`Generate synthetic datasets for tariff.py`):
   - Add new product types, countries, or markets
   - Adjust date ranges or data parameters
   - Add new data tables or columns

2. **Update the HTML generator** (`generate_html_viewer.py`):
   - Add new files to the `data_files` list:
   ```python
   data_files = [
       # ... existing files ...
       {'id': 'new-data', 'name': 'New Data', 'file': 'new_data.csv', 'icon': '🆕'}
   ]
   ```

3. **Regenerate everything**:
   ```bash
   # Generate new data
   python3 "Generate synthetic datasets for tariff.py"
   
   # Update HTML viewer
   python3 generate_html_viewer.py
   
   # View updated data
   open data_viewer_embedded.html
   ```

### Adding New Data Tables

To add a completely new data table:

1. **In the data generator**, add a new function:
   ```python
   def generate_new_data() -> pd.DataFrame:
       # Your data generation logic
       return pd.DataFrame(data)
   ```

2. **Call the function** in the main section:
   ```python
   new_data = generate_new_data()
   new_data.to_csv(OUT_DIR / "new_data.csv", index=False)
   ```

3. **Update the HTML generator**:
   ```python
   data_files = [
       # ... existing files ...
       {'id': 'new-data', 'name': 'New Data', 'file': 'new_data.csv', 'icon': '🆕'}
   ]
   ```

4. **Regenerate**:
   ```bash
   python3 "Generate synthetic datasets for tariff.py"
   python3 generate_html_viewer.py
   ```

## ⚙️ Configuration Options

### Data Generation Parameters

Edit `Generate synthetic datasets for tariff.py`:

```python
# Number of products per type
N_PRODUCTS_PER_TYPE = 25

# Product categories
PRODUCT_TYPES = ["Electronics", "Apparel", "Home", "Toys"]

# Countries of origin
COUNTRIES = ["China", "Vietnam", "Mexico", "India", "USA"]

# Destination markets
DEST_MARKETS = ["USA-West", "USA-East", "EU-West", "EU-Central"]

# Date range
START_DATE = pd.Timestamp("2025-01-01")
END_DATE = pd.Timestamp("2025-09-30")
```

### HTML Viewer Settings

Edit `generate_html_viewer.py`:

```python
# Maximum rows to display per table (for performance)
max_rows = 100

# Table icons and names
data_files = [
    {'id': 'tariffs', 'name': 'Tariffs', 'file': 'tariffs.csv', 'icon': '📈'},
    # Add more tables here...
]
```

## 🛠️ Troubleshooting

### Common Issues

1. **"File not found" errors**:
   - Ensure `retail_tariff_data/` folder exists
   - Run the data generator first: `python3 "Generate synthetic datasets for tariff.py"`

2. **HTML not loading data**:
   - Use `data_viewer_embedded.html` 
   - The embedded version has all data included

3. **Performance issues with large datasets**:
   - Reduce `max_rows` in `generate_html_viewer.py`
   - Consider pagination for very large tables

4. **Import errors**:
   - Install required packages: `pip install -r requirements.txt`
   - Or minimal install: `pip install pandas numpy`
   - Ensure Python 3.6+ is being used

5. **Dynamic viewer CORS errors**:
   - **Automatic fix**: Use `python3 update_data.py` (starts web server automatically)
   - **Manual fix**: Run `python3 start_web_server.py` or `python3 -m http.server 5200`
   - **URL**: Open `http://localhost:5200/data_viewer_dynamic.html`

6. **CRUD server port conflicts**:
   - **Port 5000 in use**: Server automatically uses port 5001
   - **Manual port change**: Edit `PORT = 5001` in `crud_server.py`
   - **Check running servers**: `ps aux | grep crud_server`
   - **CRUD URL**: `http://localhost:5001`

7. **CRUD viewer not loading**:
   - **Check server status**: `curl http://localhost:5001/api/tables`
   - **Install Flask**: `pip install flask flask-cors`
   - **Restart server**: `python3 crud_server.py`
   - **Browser cache**: Try hard refresh (Ctrl+F5 or Cmd+Shift+R)

8. **Dynamic viewer not loading**:
   - **Check server status**: `curl http://localhost:5200/data_viewer_dynamic.html`
   - **Start server**: `python3 -m http.server 5200`
   - **Check file exists**: `ls -la data_viewer_dynamic.html`
   - **CORS issues**: Use `http://localhost:5200` not `file://`

9. **Both viewers not working**:
   - **Check ports**: `lsof -i :5001` and `lsof -i :5200`
   - **Kill processes**: `pkill -f crud_server.py` and `pkill -f "http.server"`
   - **Restart fresh**: Close terminals and restart
   - **Check Python**: `python3 --version` (needs 3.6+)

### Data Validation

Check data integrity:
```bash
# Count records in each file
wc -l retail_tariff_data/*.csv

# Check file sizes
ls -lh retail_tariff_data/

# Validate CSV structure
python3 -c "import pandas as pd; print(pd.read_csv('retail_tariff_data/tariffs.csv').info())"
```

## 📊 Data Overview

| Table | Records | Description |
|-------|---------|-------------|
| Tariffs | 60 | Tariff rates by country, product type, and time |
| Products | 100 | Product catalog with SKUs and pricing |
| Suppliers | 10 | Supplier details and capacity |
| Markets | 4 | Destination markets with currencies |
| Cost & Transit | 142 | Shipping lanes and costs |
| Sales Daily | 27,300 | Daily sales forecasts and actuals |
| Sales Weekly | 4,000 | Weekly aggregated sales data |

**Total: 31,616 records**

📖 **For detailed column descriptions and business logic, see [retail_tariff_data/DATA_DICTIONARY.md](retail_tariff_data/DATA_DICTIONARY.md)**

## 🔍 HTML Viewer

### Dynamic Viewer (`data_viewer_dynamic.html`)
- **Real-time data loading** from CSV files
- **Refresh button** to reload data without regenerating HTML
- **Always up-to-date** with latest CSV data
- **Requires web server** (due to CORS restrictions)
- **Small file size** (no embedded data)
- **Auto-starts web server** when using `python3 update_data.py`

## 🔍 Interactive Features

### Column Filtering
- **Dropdown filters** for each column in every table
- **Real-time filtering** as you select values
- **Multiple filters** can be applied simultaneously
- **Clear All** button to reset all filters
- **Visible row counter** updates dynamically

### Data Export
- **Export filtered data** to CSV format
- **Maintains current filter state** in exported file
- **One-click download** for each table

### Table Navigation
- **Table of Contents** with anchor links
- **Responsive design** for mobile and desktop
- **Scrollable tables** for large datasets
- **Hover effects** for better readability

## 🔧 Advanced Usage

### Custom Data Sources

To use your own CSV files instead of generated data:

1. Place your CSV files in `retail_tariff_data/`
2. Update the `data_files` list in `generate_html_viewer.py`
3. Run: `python3 generate_html_viewer.py`

### Batch Processing

For automated data updates:

```bash
#!/bin/bash
# update_data.sh
echo "Generating new data..."
python3 "Generate synthetic datasets for tariff.py"

echo "Updating HTML viewer..."
python3 generate_html_viewer.py

echo "Opening viewer..."
open data_viewer_embedded.html
```

### Integration with Databricks

For Databricks environments, modify the output directory:

```python
# In Generate synthetic datasets for tariff.py
OUT_DIR = Path("/dbfs/mnt/data/retail_tariff_data")  # Databricks path
```

## 📝 Notes

- The HTML viewer is self-contained and works offline
- Data is embedded directly in the HTML for fast loading
- Tables are limited to 100 rows for performance (configurable)
- All timestamps are in 2025 for the synthetic dataset
- The viewer includes responsive design for mobile/desktop

## 🤝 Contributing

To add new features or data types:

1. Modify the data generator functions
2. Update the HTML generator configuration
3. Test with: `python3 generate_html_viewer.py`
4. Update this README with new instructions

---

**Happy data exploring! 📊✨**
