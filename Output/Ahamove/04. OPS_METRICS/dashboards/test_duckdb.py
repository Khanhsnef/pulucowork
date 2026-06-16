import duckdb
import os
import glob

BASE_DIR = "/Users/ts-1148/Desktop/Pulu-workspace"
RAW_DATA_DIR = os.path.join(BASE_DIR, "output", "Ahamove", "04. OPS_METRICS", "raw-data")

def find_file(pattern):
    search_pattern = os.path.join(RAW_DATA_DIR, pattern)
    matches = glob.glob(search_pattern)
    if matches:
        return matches[0]
    direct_path = os.path.join(RAW_DATA_DIR, pattern.replace("*", ""))
    if os.path.exists(direct_path):
        return direct_path
    return None

ACTIVE_FILE = find_file("*active.csv")
DISPATCH_FILE = find_file("*dispatch.csv")
if not DISPATCH_FILE:
    DISPATCH_FILE = find_file("*dispatch 2.csv")

print("Active File:", ACTIVE_FILE)
print("Dispatch File:", DISPATCH_FILE)

if not ACTIVE_FILE or not DISPATCH_FILE:
    print("❌ Error: Missing files!")
    exit(1)

db = duckdb.connect(database=':memory:')

# Test loading raw files
print("Loading data into DuckDB...")
db.execute(f"""
    CREATE OR REPLACE TEMP VIEW raw_dispatch AS 
    SELECT 
        service,
        order_date,
        CAST(REPLACE(requested_order, ',', '') AS INTEGER) as requested_order,
        CAST(REPLACE(recommended_order, ',', '') AS INTEGER) as recommended_order,
        CAST(REPLACE(rec_rate, '%', '') AS DOUBLE) / 100.0 as rec_rate,
        province,
        hour
    FROM read_csv_auto('{DISPATCH_FILE}', header=True)
""")

db.execute(f"""
    CREATE OR REPLACE TEMP VIEW raw_active AS 
    SELECT 
        city_id,
        order_date,
        tag,
        CAST(REPLACE(total_active, ',', '') AS INTEGER) as total_active,
        service,
        hour,
        MONTH,
        WEEK
    FROM read_csv_auto('{ACTIVE_FILE}', header=True, types={{'total_active': 'VARCHAR'}})
""")

print("Successfully loaded CSV views.")
print("Verifying demand metrics...")
demand_res = db.execute("SELECT COUNT(*), SUM(requested_order) FROM raw_dispatch").fetchone()
print("Dispatch rows count & sum:", demand_res)

print("Verifying active driver metrics...")
active_res = db.execute("SELECT COUNT(*), SUM(total_active) FROM raw_active").fetchone()
print("Active driver rows count & sum:", active_res)

print("Verifying hourly join query...")
query = """
    WITH hourly_demand AS (
        SELECT 
            hour,
            SUM(requested_order) as total_demand,
            SUM(recommended_order) as total_recommended
        FROM raw_dispatch
        WHERE province = 'SGN'
        GROUP BY hour
    ),
    hourly_capacity AS (
        SELECT 
            hour,
            SUM(total_active) as active_capacity
        FROM raw_active
        WHERE city_id = 'SGN' 
          AND LOWER(tag) IN ('ft', 'pt', 'nim')
        GROUP BY hour
    )
    SELECT 
        d.hour,
        d.total_demand,
        d.total_recommended,
        c.active_capacity
    FROM hourly_demand d
    LEFT JOIN hourly_capacity c ON d.hour = c.hour
    ORDER BY d.hour
"""
res = db.execute(query).fetchall()
print("Hourly results sample (first 3):", res[:3])
print("✅ DuckDB POC validation succeeded!")
