# Generate synthetic datasets for tariff + retail scenario planning
import numpy as np
import pandas as pd
from pathlib import Path
import math, random

# Reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# ------------------
# Config
# ------------------
N_PRODUCTS_PER_TYPE = 25
PRODUCT_TYPES = ["Electronics", "Apparel", "Home", "Toys"]
COUNTRIES = ["China", "Vietnam", "Mexico", "India", "USA"]
DEST_MARKETS = ["USA-West", "USA-East", "EU-West", "EU-Central"]

START_DATE = pd.Timestamp("2025-01-01")
END_DATE   = pd.Timestamp("2025-09-30")

TARIFF_CHANGE_DATES = [
    pd.Timestamp("2025-01-01"),
    pd.Timestamp("2025-04-01"),
    pd.Timestamp("2025-07-01"),
]

OUT_DIR = Path("./retail_tariff_data")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------
# Helpers
# ------------------
def aur_by_type(pt: str) -> float:
    return {
        "Electronics": 180.0,
        "Apparel": 35.0,
        "Home": 60.0,
        "Toys": 25.0,
    }[pt]

def base_cost_mean(pt: str) -> float:
    return {
        "Electronics": 120.0,
        "Apparel": 20.0,
        "Home": 42.0,
        "Toys": 14.0,
    }[pt]

def daterange(start: pd.Timestamp, end: pd.Timestamp):
    cur = start
    while cur <= end:
        yield cur
        cur += pd.Timedelta(days=1)

# ------------------
# 1) Tariffs (country, product_type, current_tariff, start_time)
# ------------------
def generate_tariffs() -> pd.DataFrame:
    rows = []
    base_map = {"Electronics": 0.08, "Apparel": 0.12, "Home": 0.06, "Toys": 0.05}
    country_bias = {"China": 0.02, "Vietnam": -0.01, "Mexico": -0.005, "India": -0.002, "USA": 0.00}
    for c in COUNTRIES:
        for pt in PRODUCT_TYPES:
            cur = max(0.0, base_map[pt] + country_bias.get(c, 0.0) + np.random.normal(0, 0.01))
            for d in TARIFF_CHANGE_DATES:
                cur = float(max(0.0, min(0.40, cur + np.random.normal(0, 0.01))))
                rows.append({
                    "country": c,
                    "product_type": pt,
                    "current_tariff": round(cur, 4),
                    "start_time": d.normalize(),
                })
    df = pd.DataFrame(rows).sort_values(["product_type", "country", "start_time"]).reset_index(drop=True)
    return df

# ------------------
# 2) Suppliers & Markets
# ------------------
SUPPLIER_NAMES = {
    "China":   ["CN_Supplier_A", "CN_Supplier_B"],
    "Vietnam": ["VN_Supplier_X", "VN_Supplier_Y"],
    "Mexico":  ["MX_Supplier_M", "MX_Supplier_N"],
    "India":   ["IN_Supplier_I", "IN_Supplier_J"],
    "USA":     ["US_Supplier_U1","US_Supplier_U2"],
}
RISK_LEVELS = ["Low", "Medium", "High"]

def generate_suppliers() -> pd.DataFrame:
    rows = []
    for c, names in SUPPLIER_NAMES.items():
        for name in names:
            rows.append({
                "supplier_id": name,
                "country": c,
                "risk": np.random.choice(RISK_LEVELS, p=[0.5, 0.4, 0.1]),
                "capacity_limit_qtr": int(np.random.randint(150_000, 800_000)),
                "lead_time_days": int(np.random.randint(18, 40)),
                "base_cost_multiplier": round(float(np.random.normal(1.03 if c != "China" else 1.0, 0.03)), 3),
                "freight_adj": round(max(0.0, float(np.random.normal(0.4, 0.2))), 2),
            })
    return pd.DataFrame(rows)

def generate_markets() -> pd.DataFrame:
    tz_map = {
        "USA-West": "America/Los_Angeles",
        "USA-East": "America/New_York",
        "EU-West": "Europe/Dublin",
        "EU-Central": "Europe/Berlin",
    }
    rows = []
    for m in DEST_MARKETS:
        rows.append({
            "market_code": m,
            "currency": "USD" if m.startswith("USA") else "EUR",
            "timezone": tz_map[m],
        })
    return pd.DataFrame(rows)

# ------------------
# 3) Products catalog (with AUR)
# ------------------
def generate_products(suppliers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    pid = 1
    for pt in PRODUCT_TYPES:
        for _ in range(N_PRODUCTS_PER_TYPE):
            origin = random.choice(COUNTRIES)
            aur = max(5.0, float(np.random.normal(aur_by_type(pt), aur_by_type(pt) * 0.1)))
            base_cost = max(1.0, float(np.random.normal(base_cost_mean(pt), base_cost_mean(pt) * 0.1)))
            s_choices = suppliers[suppliers.country == origin]
            supplier_id = s_choices.sample(1).iloc[0].supplier_id if not s_choices.empty else None
            rows.append({
                "product_id": f"SKU-{pid:04d}",
                "product_name": f"{pt[:3].upper()} Item {pid}",
                "product_type": pt,
                "country_of_origin": origin,
                "AUR": round(aur, 2),
                "base_cost": round(base_cost, 2),
                "weight_kg": round(max(0.1, float(np.random.lognormal(mean=0.0, sigma=0.5))), 3),
                "supplier_id": supplier_id,
            })
            pid += 1
    return pd.DataFrame(rows)

# ------------------
# 4) Cost & transit lanes
# ------------------
def generate_cost_transit(products: pd.DataFrame, suppliers: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, p in products.iterrows():
        origin = p.country_of_origin
        dests = np.random.choice(DEST_MARKETS, size=np.random.randint(1, 3), replace=False)
        srow = suppliers[suppliers.supplier_id == p.supplier_id]
        base_mult = 1.0
        freight_adj = 0.0
        lead_time_base = 28
        if not srow.empty:
            base_mult = float(srow.iloc[0].base_cost_multiplier)
            freight_adj = float(srow.iloc[0].freight_adj)
            lead_time_base = int(srow.iloc[0].lead_time_days)
        for dest in dests:
            lane = f"{origin}->{dest}"
            transit = int(max(10, np.random.normal(lead_time_base, 4)))
            cost_of_sourcing = max(1.0, p.base_cost * base_mult)
            freight_per_unit = round(max(0.2, float(np.random.normal(0.8 + freight_adj, 0.25))), 2)
            rows.append({
                "product_id": p.product_id,
                "origin_country": origin,
                "destination_market": dest,
                "lane": lane,
                "lead_time_days": transit,
                "transit_time_days": transit,
                "cost_of_sourcing": round(float(cost_of_sourcing), 2),
                "freight_per_unit": freight_per_unit,
                "incoterm": np.random.choice(["FOB", "CIF", "DDP"], p=[0.5, 0.3, 0.2]),
            })
    return pd.DataFrame(rows)

# ------------------
# 5) Sales (daily + weekly)
# ------------------
def generate_sales_daily(products: pd.DataFrame) -> pd.DataFrame:
    rows = []
    base_mu_map = {"Electronics": 8, "Apparel": 14, "Home": 10, "Toys": 9}
    for _, p in products.iterrows():
        base_mu = base_mu_map[p.product_type]
        for d in daterange(START_DATE, END_DATE):
            dow = d.weekday()
            week_bump = {5: 1.2, 6: 1.25}.get(dow, 1.0)
            month_trend = 1.0 + 0.02 * math.sin((d.dayofyear / 365) * 2 * math.pi)
            fcst = max(0, np.random.normal(base_mu * week_bump * month_trend, 2.0))
            actual = max(0, np.random.normal(fcst, 2.5))
            rows.append({
                "date": d.normalize(),
                "product_id": p.product_id,
                "prod_type": p.product_type,
                "sales_forecast": round(float(fcst), 2),
                "actual_sales": round(float(actual), 2),
            })
    return pd.DataFrame(rows)

def to_weekly(df_daily: pd.DataFrame) -> pd.DataFrame:
    df = df_daily.copy()
    df["year"] = df["date"].dt.isocalendar().year
    df["week"] = df["date"].dt.isocalendar().week
    grp = df.groupby(["year", "week", "product_id", "prod_type"], as_index=False).agg({
        "sales_forecast": "sum",
        "actual_sales": "sum",
    })
    grp["week_start"] = pd.to_datetime(grp["year"].astype(str) + grp["week"].astype(str) + "1", format="%G%V%u")
    return grp[["week_start", "year", "week", "product_id", "prod_type", "sales_forecast", "actual_sales"]]

# ------------------
# Build
# ------------------
tariffs = generate_tariffs()
suppliers = generate_suppliers()
markets = generate_markets()
products = generate_products(suppliers)
cost_transit = generate_cost_transit(products, suppliers)
sales_daily = generate_sales_daily(products)
sales_weekly = to_weekly(sales_daily)

# Ensure required columns/order
tariffs = tariffs[["country", "product_type", "current_tariff", "start_time"]]
products = products[["product_id", "product_name", "product_type", "country_of_origin", "AUR", "base_cost", "weight_kg", "supplier_id"]]
sales_daily = sales_daily[["date", "product_id", "prod_type", "sales_forecast", "actual_sales"]]
sales_weekly = sales_weekly[["week_start", "year", "week", "product_id", "prod_type", "sales_forecast", "actual_sales"]]
cost_transit = cost_transit[["product_id", "origin_country", "destination_market", "lane", "lead_time_days", "transit_time_days", "cost_of_sourcing", "freight_per_unit", "incoterm"]]

# Save
tariffs.to_csv(OUT_DIR / "tariffs.csv", index=False)
products.to_csv(OUT_DIR / "products.csv", index=False)
sales_daily.to_csv(OUT_DIR / "sales_daily.csv", index=False)
sales_weekly.to_csv(OUT_DIR / "sales_weekly.csv", index=False)
cost_transit.to_csv(OUT_DIR / "cost_transit.csv", index=False)
suppliers.to_csv(OUT_DIR / "suppliers.csv", index=False)
markets.to_csv(OUT_DIR / "markets.csv", index=False)

# Preview to user as small samples
print("\n=== TARIFFS (sample) ===")
print(tariffs.head(20))
print("\n=== PRODUCTS (sample) ===")
print(products.head(20))
print("\n=== SALES DAILY (sample) ===")
print(sales_daily.head(20))
print("\n=== SALES WEEKLY (sample) ===")
print(sales_weekly.head(20))
print("\n=== COST TRANSIT (sample) ===")
print(cost_transit.head(20))
print("\n=== SUPPLIERS (sample) ===")
print(suppliers.head(20))
print("\n=== MARKETS (sample) ===")
print(markets.head(20))

str(OUT_DIR)
