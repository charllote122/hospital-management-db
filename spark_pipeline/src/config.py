import os
import sys

# =====================================================================
# CRITICAL WINDOWS FIX: SET ENVIRONMENT VARIABLES DIRECTLY IN PYTHON
# =====================================================================
# 1. Tell Spark where Hadoop is
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["hadoop.home.dir"] = r"C:\hadoop"

# 2. Add the Hadoop bin folder to the system PATH for this Python process
hadoop_bin = r"C:\hadoop\bin"
if hadoop_bin not in os.environ["PATH"]:
    os.environ["PATH"] = hadoop_bin + os.pathsep + os.environ["PATH"]

# 3. Force Spark to use the Python executable inside your virtual environment
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# =====================================================================
# PATHS
# =====================================================================
RAW_DATA_PATH = "python_scripts/data/raw/orders.csv"
BRONZE_PATH = "spark_pipeline/data/bronze/orders"
SILVER_PATH = "spark_pipeline/data/silver/orders"
GOLD_PATH = "spark_pipeline/data/gold/revenue_by_status"
