# 📋 Data Quick Reference

## 🗂️ File Locations
```
retail_tariff_data/
├── tariffs.csv          (60 records)
├── products.csv         (100 records)  
├── suppliers.csv        (10 records)
├── markets.csv          (4 records)
├── cost_transit.csv     (142 records)
├── sales_daily.csv      (27,300 records)
└── sales_weekly.csv     (4,000 records)
```

## 🔑 Key Columns by Dataset

### Tariffs
- `country` → `product_type` → `current_tariff` → `start_time`

### Products  
- `product_id` → `product_name` → `product_type` → `AUR` → `base_cost`

### Suppliers
- `supplier_id` → `country` → `risk` → `capacity_limit_qtr`

### Sales Daily
- `date` → `product_id` → `sales_forecast` → `actual_sales`

### Cost & Transit
- `product_id` → `origin_country` → `destination_market` → `freight_per_unit`

## 🔗 Common Joins

```sql
-- Products with Suppliers
products.supplier_id = suppliers.supplier_id

-- Sales with Products  
sales_daily.product_id = products.product_id

-- Tariffs with Products
tariffs.country = products.country_of_origin
AND tariffs.product_type = products.product_type
```

## 📊 Data Types

| Column Pattern | Type | Example |
|----------------|------|---------|
| `*_id` | String | "SKU-0001", "CN_Supplier_A" |
| `*_date`, `*_time` | Date | "2025-01-01" |
| `*_cost`, `*_price`, `AUR` | Float | 135.02, 0.1353 |
| `*_days`, `*_qtr` | Integer | 24, 255878 |
| `country`, `market_code` | String | "China", "USA-West" |

## 🎯 Business Rules Summary

- **Tariffs**: 0-40% range, quarterly changes
- **Products**: 25 per type, AUR varies by category  
- **Suppliers**: 2 per country, risk levels Low/Medium/High
  - **Low**: Generally dependable with fewer disruptions
  - **Medium**: Some uncertainty, possible delays or constraints
  - **High**: Higher chance of supply problems, delays, shortages, or quality issues
- **Sales**: Daily data with weekend/seasonal patterns
- **Costs**: Include sourcing + freight + tariffs

## 📈 Analytics Examples

- **Tariff Impact**: `tariffs.current_tariff * products.base_cost`
- **Supplier Risk**: `suppliers.risk = 'High'` filter
- **Sales Performance**: `sales_actual / sales_forecast`
- **Cost Analysis**: `cost_transit.cost_of_sourcing + cost_transit.freight_per_unit`

---
*Full details: [retail_tariff_data/DATA_DICTIONARY.md](retail_tariff_data/DATA_DICTIONARY.md)*
