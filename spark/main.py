# %%
from pyspark.sql import SparkSession

# Tạo SparkSession
spark = SparkSession.builder.appName("SimpleSparkApp").getOrCreate()

# %%
# Đường dẫn đến tệp JSON
json_file_path = "./cardano.json"

# Đọc tệp JSON vào DataFrame
df = spark.read.json(json_file_path)

# Hiển thị DataFrame
df.show()

# Đóng SparkSession
spark.stop()
