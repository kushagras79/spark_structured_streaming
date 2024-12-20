from pyspark.sql import SparkSession
from pyspark.sql import functions as f

spark = SparkSession.builder.appName('various triggers'). \
    getOrCreate()

#reading from socket

df = spark.readStream.format('socket'). \
    option('host','localhost'). \
    option('port','9982'). \
    load()

df = df.select(f.explode(f.split("value",' ')).alias('words')).groupBy('words').agg(f.count('words').alias('word_count'))

query = df.writeStream.format('console'). \
    trigger(availableNow=True). \
    outputMode('complete'). \
    option('checkpointlocation','trigger_checkpoint_dir'). \
    start()

query.awaitTermination()







