# 🚀 Quick Start Guide

## 🎯 **Realistic Data Updates (2024)**

**All datasets now reflect realistic shipping and supply chain patterns:**
- **Lead Times**: Geographic proximity-based (Mexico: 3-4 days, Asia: 19-28 days)
- **Freight Costs**: Distance-based pricing with proximity advantages
- **Quality Scores**: Realistic distribution with poor quality suppliers
- **Transit vs Lead Time**: Separated transportation from processing time

## Install Dependencies
```bash
pip install -r requirements.txt
```

## One-Command Update
```bash
python3 update_data.py
```
*This does everything: generates data, creates HTML viewer, and opens it*

## Manual Steps
```bash
# 1. Generate data
python3 "Generate synthetic datasets for tariff.py"

# 2. Create HTML viewer  
python3 generate_dynamic_html_viewer.py

# 3. Start web server and open viewer
python3 start_web_server.py
```

## Web Server Launcher
```bash
python3 start_web_server.py
```

## What Gets Generated
- 📁 `retail_tariff_data/` - 7 CSV files with 31,616 records
- 🌐 `data_viewer_dynamic.html` - Interactive data viewer
- 📊 Dynamic loading from CSV files (real-time updates)

## Adding New Data
1. Edit `Generate synthetic datasets for tariff.py`
2. Add new table to `data_files` in `generate_dynamic_html_viewer.py`
3. Run `python3 update_data.py`

## Troubleshooting
- **Missing packages**: `pip install -r requirements.txt`
- **File not found**: Run data generator first
- **CORS errors**: Run `python3 start_web_server.py` or `python3 -m http.server 5200`

---
*For detailed instructions, see README.md*
