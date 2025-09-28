# 🔍 Filtering Demo Guide

## How to Use the Interactive Filters

### 1. **Column Dropdown Filters**
Each table now has dropdown filters for every column:
- **Tariffs Table**: Filter by country, product_type, current_tariff, start_time
- **Products Table**: Filter by product_id, product_name, product_type, country_of_origin, AUR, base_cost, weight_kg, supplier_id
- **Suppliers Table**: Filter by supplier_id, country, risk, capacity_limit_qtr, lead_time_days, base_cost_multiplier, freight_adj
- **And more...**

### 2. **Real-time Filtering**
- Select any value from any dropdown
- Table updates instantly to show only matching rows
- Multiple filters work together (AND logic)
- Row count updates automatically

### 3. **Example Filtering Scenarios**

#### Filter Products by Type and Country:
1. Go to Products table
2. Select "Electronics" in product_type filter
3. Select "China" in country_of_origin filter
4. See only Chinese electronics products

#### Filter Tariffs by Country:
1. Go to Tariffs table
2. Select "China" in country filter
3. See only Chinese tariff rates

#### Filter Sales by Product Type:
1. Go to Sales Daily table
2. Select "Electronics" in prod_type filter
3. See only electronics sales data

### 4. **Clear and Export**
- **Clear All**: Resets all filters for that table
- **Export CSV**: Downloads filtered data as CSV file

### 5. **Filter Features**
- ✅ **Case-insensitive** matching
- ✅ **Partial matching** (contains logic)
- ✅ **Multiple filters** simultaneously
- ✅ **Real-time updates**
- ✅ **Visual feedback** (row count updates)
- ✅ **Export filtered data**

## 🎯 Pro Tips

1. **Start broad, then narrow**: Apply one filter, then add more
2. **Use Clear All** to start fresh
3. **Export filtered data** for further analysis
4. **Check row counts** to see how many records match
5. **Combine filters** for precise data selection

## 📊 Example Use Cases

- **Find all high-risk suppliers**: Filter suppliers by risk = "High"
- **View electronics from China**: Filter products by type = "Electronics" AND country = "China"
- **See recent tariffs**: Filter tariffs by start_time = "2025-07-01"
- **Analyze specific sales periods**: Filter sales by date ranges
- **Export specific data subsets**: Apply filters then export CSV

---

**Try it out! The filters make it easy to explore and analyze your data interactively.** 🚀
