# 📊 Data Dictionary - Retail Tariff Datasets

This document describes all datasets generated for tariff and retail scenario planning analysis.

## 🎯 **Recent Updates for Realism (2024)**

**All data has been updated to reflect realistic shipping and supply chain patterns:**

- **Lead Times**: Now reflect actual geographic proximity (Mexico: 3-4 days, USA: 1.5-3 days, Asia: 19-28 days)
- **Freight Costs**: Distance-based pricing with proximity advantages (Mexico: 65% reduction, USA: 80% reduction)
- **Quality Scores**: Realistic distribution across countries with at least 2 suppliers having poor quality (score 1)
- **Transit vs Lead Time**: Separated pure transportation time from total lead time (includes processing)
- **Processing Times**: Added realistic customs and documentation delays by country

## 📁 Dataset Overview

| Dataset | File | Records | Description |
|---------|------|---------|-------------|
| Tariffs | `tariffs.csv` | 60 | Tariff rates by country, product type, and time periods |
| Products | `products.csv` | 100 | Product catalog with SKUs, pricing, and supplier information |
| Suppliers | `suppliers.csv` | 10 | Supplier details including capacity, lead times, and risk levels |
| Markets | `markets.csv` | 4 | Destination markets with currency and timezone information |
| Cost & Transit | `cost_transit.csv` | 142 | Shipping lanes with costs, transit times, and incoterms |
| Sales Daily | `sales_daily.csv` | 27,300 | Daily sales forecasts and actuals for all products |
| Sales Weekly | `sales_weekly.csv` | 4,000 | Weekly aggregated sales data |

**Total Records: 31,616**

---

## 📈 Tariffs Dataset (`tariffs.csv`)

**Purpose**: Track tariff rates by country, product type, and time periods for scenario planning.

### Columns:
| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| `country` | String | Country of origin | "China", "Vietnam", "Mexico", "India", "USA" |
| `product_type` | String | Product category | "Electronics", "Apparel", "Home", "Toys" |
| `current_tariff` | Float | Tariff rate (decimal) | 0.1353, 0.1036, 0.0975 |
| `start_time` | Date | When tariff rate becomes effective | "2025-01-01", "2025-04-01", "2025-07-01" |

### Business Logic:
- Base tariff rates vary by product type (Electronics: 8%, Apparel: 12%, Home: 6%, Toys: 5%)
- Country-specific adjustments (China: +2%, Vietnam: -1%, Mexico: -0.5%, India: -0.2%, USA: 0%)
- Tariff changes occur quarterly in 2025
- Rates capped between 0% and 40%

---

## 🛍️ Products Dataset (`products.csv`)

**Purpose**: Complete product catalog with pricing, specifications, and supplier assignments.

### Columns:
| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| `product_id` | String | Unique SKU identifier | "SKU-0001", "SKU-0002" |
| `product_name` | String | Product display name | "ELE Item 1", "APP Item 25" |
| `product_type` | String | Product category | "Electronics", "Apparel", "Home", "Toys" |
| `country_of_origin` | String | Manufacturing country | "China", "Vietnam", "Mexico", "India", "USA" |
| `AUR` | Float | Average Unit Retail price (USD) | 135.02, 159.30, 177.53 |
| `base_cost` | Float | Manufacturing cost (USD) | 137.76, 110.70, 136.82 |
| `weight_kg` | Float | Product weight in kilograms | 1.468, 1.472, 1.341 |
| `supplier_id` | String | Assigned supplier | "CN_Supplier_A", "VN_Supplier_X" |

### Business Logic:
- 25 products per product type (100 total)
- AUR varies by product type: Electronics ($180±10%), Apparel ($35±10%), Home ($60±10%), Toys ($25±10%)
- Base cost typically 60-80% of AUR
- Weight follows log-normal distribution
- Supplier assignment based on country of origin

---

## 🏭 Suppliers Dataset (`suppliers.csv`)

**Purpose**: Supplier information including capacity, lead times, risk assessment, quality scores, and delivery reliability.

### Columns:
| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| `supplier_id` | String | Unique supplier identifier | "CN_Supplier_A", "VN_Supplier_X" |
| `country` | String | Supplier location | "China", "Vietnam", "Mexico", "India", "USA" |
| `risk` | String | Risk assessment level | "Low", "Medium", "High" |
| `capacity_limit_qtr` | Integer | Quarterly capacity limit (units) | 255878, 474767, 214044 |
| `lead_time_days` | Integer | Average lead time in days | 21, 28, 4 |
| `base_cost_multiplier` | Float | Cost adjustment factor | 1.044, 0.976, 1.038 |
| `freight_adj` | Float | Freight cost adjustment | 0.30, 0.46, 0.20 |
| `supplier_quality_score` | Integer | Quality rating (1-5 scale) | 1, 2, 4, 5 |
| `lead_time_variation` | Float | Delivery deviation percentage | 5.4, 8.5, 15.2, 22.8 |

### Business Logic:
- 2 suppliers per country (10 total)
- Risk distribution: Low (50%), Medium (10%), High (40%)
- Capacity ranges from 150K to 800K units per quarter
- **Lead times vary by country (2-29 days) - Realistic shipping times:**
  - **Mexico**: 4-5 days (truck/rail proximity, quick processing)
  - **USA**: 2-3 days (domestic shipping, minimal processing)
  - **China**: 21-23 days (transpacific shipping, standard processing)
  - **India**: 28 days (transpacific shipping, standard processing)
  - **Vietnam**: 28-29 days (transpacific shipping, standard processing)
- Cost multipliers reflect local manufacturing costs
- Freight adjustments based on shipping distance
- Quality scores correlate with risk levels (High risk = lower quality)
- Lead time variation represents delivery reliability (lower % = more reliable)
- **Quality score distribution: Score 1 (20%), Score 2 (10%), Score 3 (20%), Score 4 (40%), Score 5 (10%)**

### Quality Score Definitions:
- **5** → Excellent quality, consistent performance, premium supplier
- **4** → Good quality, reliable performance, preferred supplier
- **3** → Moderate quality, acceptable performance, standard supplier
- **2** → Poor quality, inconsistent performance, problematic supplier
- **1** → Very poor quality, unreliable performance, avoid if possible

### Lead Time Variation Definitions:
- **< 10%** → Very reliable delivery, minimal deviation from promised dates
- **10-15%** → Reliable delivery, occasional minor delays
- **15-20%** → Moderate reliability, some delivery uncertainty
- **> 20%** → Unreliable delivery, frequent delays and variations

### Risk Level Definitions:
- **Low** → Suppliers are generally dependable with fewer disruptions
- **Medium** → There's some uncertainty, such as possible delays or constraints
- **High** → A higher chance of supply problems, like delays, shortages, or quality issues

---

## 🌍 Markets Dataset (`markets.csv`)

**Purpose**: Destination market information including currency and timezone.

### Columns:
| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| `market_code` | String | Market identifier | "USA-West", "USA-East", "EU-West", "EU-Central" |
| `currency` | String | Local currency | "USD", "EUR" |
| `timezone` | String | Market timezone | "America/Los_Angeles", "Europe/Dublin" |

### Business Logic:
- 4 destination markets
- USA markets use USD, EU markets use EUR
- Timezones correspond to major business centers

---

## 🚚 Cost & Transit Dataset (`cost_transit.csv`)

**Purpose**: Shipping lane information including costs, transit times, and incoterms.

### Columns:
| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| `product_id` | String | Product SKU | "SKU-0001", "SKU-0002" |
| `origin_country` | String | Shipping origin | "China", "Vietnam", "Mexico" |
| `destination_market` | String | Shipping destination | "USA-West", "EU-Central" |
| `lane` | String | Shipping lane identifier | "China->USA-East", "Vietnam->EU-West" |
| `lead_time_days` | Integer | Total lead time in days (transit + processing) | 19, 26, 3 |
| `transit_time_days` | Integer | Pure transportation time in days | 16, 22, 2 |
| `cost_of_sourcing` | Float | Sourcing cost (USD) | 143.82, 108.04, 135.45 |
| `freight_per_unit` | Float | Freight cost per unit (USD) | 0.13, 1.50, 0.06 |
| `incoterm` | String | Shipping terms | "FOB", "CIF", "DDP" |

### Business Logic:
- Each product has 1-2 destination markets
- **Lead time = Transit time + Processing time:**
  - **Mexico**: 2-3 days transit + 1-2 days processing = 3-4 days total
  - **USA**: 1-2 days transit + 0.5-1 days processing = 1.5-3 days total
  - **China**: 16-18 days transit + 3-4 days processing = 19-22 days total
  - **India**: 21-23 days transit + 4-6 days processing = 26-28 days total
  - **Vietnam**: 18-21 days transit + 3-4 days processing = 21-25 days total
- Sourcing cost = base_cost × supplier_multiplier
- **Freight costs reflect realistic distance-based pricing:**
  - **Mexico → USA**: $0.08-0.18 per unit (65% reduction due to proximity)
  - **USA Domestic**: $0.03-0.08 per unit (80% reduction for domestic shipping)
  - **China → USA**: $0.91-2.10 per unit (20% increase for transpacific distance)
  - **India → USA**: $1.02-2.44 per unit (15% increase for transpacific distance)
  - **Vietnam → USA**: $0.87-1.90 per unit (10% increase for transpacific distance)
- Incoterm distribution: FOB (50%), CIF (30%), DDP (20%)

---

## 📅 Sales Daily Dataset (`sales_daily.csv`)

**Purpose**: Daily sales forecasts and actuals for demand planning and analysis.

### Columns:
| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| `date` | Date | Sales date | "2025-01-01", "2025-01-02" |
| `product_id` | String | Product SKU | "SKU-0001", "SKU-0002" |
| `prod_type` | String | Product category | "Electronics", "Apparel" |
| `sales_forecast` | Float | Forecasted sales (units) | 7.95, 11.46, 8.08 |
| `actual_sales` | Float | Actual sales (units) | 13.31, 12.55, 8.38 |

### Business Logic:
- Daily data from 2025-01-01 to 2025-09-30 (273 days)
- Base daily sales vary by product type: Electronics (8), Apparel (14), Home (10), Toys (9)
- Weekend boost: Saturday (+20%), Sunday (+25%)
- Seasonal trend: ±2% monthly variation
- Actual sales = forecast ± random variation (σ=2.5)

---

## 📊 Sales Weekly Dataset (`sales_weekly.csv`)

**Purpose**: Weekly aggregated sales data for higher-level analysis and reporting.

### Columns:
| Column | Type | Description | Example Values |
|--------|------|-------------|----------------|
| `week_start` | Date | Week start date (Monday) | "2024-12-30", "2025-01-06" |
| `year` | Integer | ISO year | 2025 |
| `week` | Integer | ISO week number | 1, 2, 3 |
| `product_id` | String | Product SKU | "SKU-0001", "SKU-0002" |
| `prod_type` | String | Product category | "Electronics", "Apparel" |
| `sales_forecast` | Float | Weekly forecast total (units) | 47.83, 40.41 |
| `actual_sales` | Float | Weekly actual total (units) | 47.85, 35.38 |

### Business Logic:
- Aggregated from daily sales data
- Uses ISO week numbering (Monday start)
- 39 weeks of data (2025 weeks 1-39)
- Weekly totals = sum of daily values per week

---

## 🔗 Data Relationships

### Primary Keys:
- **Products**: `product_id`
- **Suppliers**: `supplier_id`
- **Markets**: `market_code`

### Foreign Keys:
- **Products** → **Suppliers**: `supplier_id`
- **Cost & Transit** → **Products**: `product_id`
- **Sales** → **Products**: `product_id`

### Join Examples:
```sql
-- Products with their suppliers
SELECT p.*, s.country, s.risk 
FROM products p 
JOIN suppliers s ON p.supplier_id = s.supplier_id;

-- Sales with product details
SELECT s.*, p.product_name, p.AUR 
FROM sales_daily s 
JOIN products p ON s.product_id = p.product_id;
```

---

## 📝 Data Quality Notes

### Completeness:
- ✅ All required fields populated
- ✅ No missing primary keys
- ✅ Consistent data types

### Consistency:
- ✅ Date formats standardized (YYYY-MM-DD)
- ✅ Currency amounts in USD
- ✅ Consistent naming conventions

### Business Rules:
- ✅ Tariff rates within 0-40% range
- ✅ Lead times realistic (18-40 days)
- ✅ Sales values non-negative
- ✅ Product weights positive

---

## 🚀 Usage Examples

### Scenario Planning:
- **Tariff Impact**: Join tariffs with products to calculate cost impact
- **Supplier Risk**: Analyze supplier capacity vs. demand
- **Market Analysis**: Compare sales performance across markets

### Analytics:
- **Demand Forecasting**: Use sales_forecast vs. actual_sales for accuracy analysis
- **Cost Optimization**: Analyze cost_transit for shipping optimization
- **Product Performance**: Compare AUR vs. sales volume by product type

---

*Generated: 2025-09-14*  
*Data Period: 2025-01-01 to 2025-09-30*  
*Total Records: 31,616*
