# 🏪 Retail Tariff Data Management System

A comprehensive data management system for retail tariff scenario planning with synthetic data generation, interactive viewers, and full CRUD operations.

## 🎯 **Realistic Data Updates (2024)**

**All datasets have been updated to reflect realistic shipping and supply chain patterns:**

- **Lead Times**: Now reflect actual geographic proximity
  - Mexico: 3-4 days (truck/rail proximity)
  - USA: 1.5-3 days (domestic shipping)
  - Asia: 19-28 days (transpacific shipping)
- **Freight Costs**: Distance-based pricing with proximity advantages
- **Quality Scores**: Realistic distribution with poor quality suppliers
- **Transit vs Lead Time**: Separated pure transportation from total lead time
- **Processing Times**: Added realistic customs and documentation delays

## 🚀 Quick Start

### **Option 1: CRUD System (Recommended) - Editable Data**
```bash
python3 src/server/start_crud_system.py
```
**Access:** `http://localhost:5001`

### **Option 2: Read-Only Viewer**
```bash
python3 src/server/start_web_server.py
```
**Access:** `http://localhost:5200/data_viewer_dynamic.html`

## 📁 Project Structure

```
wwc_code/
├── README.md                                    # This file
├── requirements.txt                             # Python dependencies
├── data_viewer_crud.html                        # CRUD-enabled HTML viewer
├── data_viewer_dynamic.html                     # Dynamic HTML viewer
├── src/                                        # Source code
│   ├── data_generation/                        # Data generation scripts
│   │   └── Generate synthetic datasets for tariff.py
│   ├── viewers/                                # HTML viewers and generators
│   │   ├── generate_crud_html_viewer.py
│   │   └── generate_dynamic_html_viewer.py
│   └── server/                                 # Server and startup scripts
│       ├── crud_server.py
│       ├── start_crud_system.py
│       └── start_web_server.py
├── scripts/                                    # Utility scripts
│   └── update_data.py
├── docs/                                       # Documentation
│   ├── README.md                              # Detailed documentation
│   ├── QUICK_START.md                         # Quick start guide
│   ├── FILTERING_DEMO.md                      # Filtering demo guide
│   └── DATA_QUICK_REFERENCE.md               # Data reference
└── retail_tariff_data/                        # Generated data
    ├── DATA_DICTIONARY.md                     # Data documentation
    ├── tariffs.csv                           # Tariff data
    ├── products.csv                          # Product catalog
    ├── suppliers.csv                         # Supplier information
    ├── markets.csv                           # Market definitions
    ├── cost_transit.csv                      # Cost and transit data
    ├── sales_daily.csv                       # Daily sales data
    └── sales_weekly.csv                      # Weekly sales data
```

## 📖 Documentation

- **[Complete Documentation](docs/README.md)** - Full project documentation
- **[Quick Start Guide](docs/QUICK_START.md)** - Get started quickly
- **[Filtering Demo](docs/FILTERING_DEMO.md)** - Learn filtering features
- **[Data Reference](docs/DATA_QUICK_REFERENCE.md)** - Data structure reference
- **[Data Dictionary](retail_tariff_data/DATA_DICTIONARY.md)** - Detailed data documentation

## 🔧 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Generate data
python3 src/data_generation/"Generate synthetic datasets for tariff.py"
```

## 🌐 Access URLs

- **CRUD Editor:** `http://localhost:5001` (Port 5001)
- **Read-Only Viewer:** `http://localhost:5200` (Port 5200)

## 📊 Features

### CRUD System
- ✅ **Full CRUD Operations** - Create, Read, Update, Delete
- ✅ **Data Validation** - Real-time field validation
- ✅ **Pagination** - 50 records per page for performance
- ✅ **Real-time Updates** - CSV files updated immediately
- ✅ **Data Filtering** - Filter by any column
- ✅ **Export Functionality** - Export filtered data to CSV

### Dynamic Viewer
- ✅ **Read-Only Access** - View and analyze data
- ✅ **Column Filtering** - Filter by any column value
- ✅ **Data Export** - Export filtered results
- ✅ **Real-time Loading** - Dynamic CSV loading
- ✅ **Responsive Design** - Works on all devices

## 🛠️ Development

### Generate New Data
```bash
python3 src/data_generation/"Generate synthetic datasets for tariff.py"
```

### Regenerate Viewers
```bash
# CRUD viewer
python3 src/viewers/generate_crud_html_viewer.py

# Dynamic viewer
python3 src/viewers/generate_dynamic_html_viewer.py
```

### Start Servers Manually
```bash
# CRUD server
python3 src/server/crud_server.py

# HTTP server (for dynamic viewer)
python3 -m http.server 5200
```

## 📋 Requirements

- Python 3.6+
- pandas
- numpy
- flask
- flask-cors

## 🆘 Troubleshooting

### Common Issues
1. **Port conflicts**: Check `lsof -i :5001` and `lsof -i :5200`
2. **Missing dependencies**: Run `pip install -r requirements.txt`
3. **CORS errors**: Use `http://localhost:5200` not `file://`
4. **Server not starting**: Check Python version and dependencies

### Server Management
```bash
# Check server status
curl http://localhost:5001/api/tables  # CRUD server
curl http://localhost:5200/data_viewer_dynamic.html  # Dynamic viewer

# Stop servers
pkill -f crud_server.py
pkill -f "http.server"
```

## 📝 License

This project is for educational and demonstration purposes.

---

**For detailed documentation, see [docs/README.md](docs/README.md)**