import os
import sys
from pyspark.sql import SparkSession

# -------------------------------------------------------------------
# CRITICAL FIX FOR WINDOWS:
# Force Spark to use the Python executable inside your virtual environment.
# Without this, Windows tries to open the Microsoft Store.
# -------------------------------------------------------------------
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# 1. Create the Spark Session
# local[*] tells Spark to use all CPU cores on your laptop
spark = (
    SparkSession.builder.appName("HospitalSparkTest").master("local[*]").getOrCreate()
)

# Set log level to reduce the massive amount of warning text
spark.sparkContext.setLogLevel("ERROR")

# 2. Create a simple DataFrame
data = [
    ("Mary Wanjiru", "Cardiology", 1500),
    ("John Doe", "Pediatrics", 2000),
    ("Samuel Kipchoge", "Cardiology", 1800),
]
columns = ["patient_name", "department", "bill_amount"]

df = spark.createDataFrame(data, columns)

# 3. Show the data
print("\n=== All Patients ===")
df.show()

# 4. Use Spark SQL to calculate total revenue per department
df.createOrReplaceTempView("billing")

print("=== Total Revenue by Department ===")
result = spark.sql("""
    SELECT department, SUM(bill_amount) as total_revenue
    FROM billing
    GROUP BY department
""")
result.show()

# 5. Stop the session
spark.stop()
