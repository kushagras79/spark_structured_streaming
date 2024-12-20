from pyspark.sql import SparkSession
from pyspark.sql import functions as f

spark = SparkSession.builder.appName('Streaming').getOrCreate()

# reading a dataframe from data stream from a socket source

words = spark.readStream.format('socket'). \
    option('host', 'localhost'). \
    option('port', '9983'). \
    load()

words.printSchema()

#as this is a streaming application so show will not work because unlike a batch processing where spark is able to collect few data and show it on the console in streaming spark will not be able collect data and show it.
# in streaming write stream works as displaying the result on the console.
# words.show()

#writing logic to count the word occurence.

words_df = words.withColumn('splitted_data', f.split(words.value, ' '))
words_df = words_df.withColumn('words', f.explode(words_df.splitted_data))
columns_to_be_dropped = ['value', 'splitted_data']
words_df = words_df.drop(*columns_to_be_dropped)

words_df = words_df.groupBy("words").agg(f.count("words").alias("word_count"))

query = words_df.writeStream. \
    format('console'). \
    outputMode('update'). \
    option('checkpointlocation', 'checkpointdir'). \
    start()

query.awaitTermination()
