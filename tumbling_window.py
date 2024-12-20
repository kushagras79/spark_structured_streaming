from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql.types import *

spark = SparkSession.builder.appName('tumbling window').getOrCreate()
# "order_id":57012,"order_date":"2020-03-02 11:05:00","order_customer_id":2765,"order_status":"PROCESSING", "amount": 200}
orders_schema = StructType([
    StructField('order_id', LongType()),
    StructField('order_date', StringType()),
    StructField('order_customer_id', IntegerType()),
    StructField('order_status', StringType()),
    StructField('amount', IntegerType())
])
df = spark.readStream.format('socket').option('host', 'localhost').option('port', '9988').load()

#converting string type value to json which will give a struct object
df = df.select(f.from_json("value",orders_schema).alias('orders_data'))
#extracting all the columns from the struc
df = df.select("orders_data.*")
df.printSchema()

df = df.groupBy(f.window("order_date","15 minutes")).agg(f.sum("amount").alias("total_amount"))

df.printSchema()

df = df.select("window.start","window.end","total_amount")

query = df.writeStream.format('console').outputMode('update').option('checkpointlocation',
                                                                     'chekpoint_directory').start()
query.awaitTermination()
