from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StructField, StringType
import os

# Import UDFs from preprocess.py
import re

# Function to process HTML and extract text
@udf(returnType=StringType())
def process_html(content):
    cleaned_text = re.sub(r"<.*?>", "", content)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
    return cleaned_text

# Function to convert views, num_answer, votes to numeric values
@udf(returnType=StringType())
def convert_to_numeric(value):
    try:
        if value.endswith("k"):
            return str(int(float(value[:-1]) * 1000))
        elif value.endswith("m"):
            return str(int(float(value[:-1]) * 1000000))
        elif value.endswith("b"):
            return str(int(float(value[:-1]) * 1000000000))
        else:
            return str(int(value))
    except ValueError:
        return "0"


# Kafka settings
kafka_topic_name = os.environ.get("KAFKA_TOPIC_NAME", "stack_exchange")
kafka_bootstrap_servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "k8s://http://example.com/kafka")

# AWS S3 settings
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
s3_bucket = os.environ.get("S3_BUCKET", "btl-bigdata")
s3_folder_name = os.environ.get("S3_FOLDER_NAME", "test")  # Thư mục trong bucket
s3_output_path = "s3a://{}/{}".format(s3_bucket, s3_folder_name)


# Initialize Spark Session with package configurations
spark = (
    SparkSession.builder.appName("KafkaConsumer")
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id)
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key)
    .config(
        "spark.hadoop.fs.s3a.aws.credentials.provider",
        "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
    )
    .getOrCreate()
)

# Define schema for the data
schema = StructType(
    [
        StructField("title", StringType(), True),
        StructField("content", StringType(), True),
        StructField("time", StringType(), True),
        StructField("category", StringType(), True),
        StructField("views", StringType(), True),
        StructField("num_answer", StringType(), True),
        StructField("votes", StringType(), True),
        StructField("solved", StringType(), True),
    ]
)

# Read data from Kafka
df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers)
    .option("subscribe", kafka_topic_name)
    .option("startingOffsets", "latest")
    # .option("startingOffsets", "earliest")
    .load()
)

# Convert JSON data from Kafka to DataFrame and apply preprocessing
df_json = (
    df.selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
    .withColumn("content", preprocess.process_html("content"))
    .withColumn("views", preprocess.convert_to_numeric("views"))
    .withColumn("num_answer", preprocess.convert_to_numeric("num_answer"))
    .withColumn("votes", preprocess.convert_to_numeric("votes"))
)

# Write data to Amazon S3
# query = (
#     df_json.repartition(1)
#     .writeStream.outputMode("append")
#     .format("json")
#     .option("checkpointLocation", "{}/checkpoint".format(s3_output_path))
#     .option("path", "{}/data".format(s3_output_path))
#     .start()
# )

# Write data to local JSON file
query = (
    df_json.writeStream.outputMode("append")
    .format("json")
    .option("checkpointLocation", "./output/checkpoint")
    .option("path", "./output/data")
    .start()
)

# Wait for the query to finish
query.awaitTermination()
