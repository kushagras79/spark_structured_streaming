from pyspark.sql import SparkSession
from pyspark.sql import functions as f


spark = SparkSession.builder.appName('Word_count_using_file_location').getOrCreate()
#reading a file pointing to a file source
#important point to note is that the path will not point to single file instead it will point to a folder where stream data would be comming.
data = spark.readStream. \
    format('csv'). \
    schema('value string'). \
    option('header','true'). \
    option('inferSchema','false'). \
    option('path',"/Users/kushagra/Documents/spark_structured_streaming/spark_structured_streaming/data/input/"). \
    load()


data.printSchema()
data = data.withColumn('splitted_value',f.split("value"," "))
data = data.withColumn('words',f.explode("splitted_value"))
data = data.groupBy("words").agg(f.count("words").alias('word_count')).drop('splitted_value')

query = data.writeStream. \
    format('console'). \
    outputMode('complete'). \
    option('checkpointlocation', 'checkpointdir'). \
    start()

query.awaitTermination()
