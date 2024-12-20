from pyspark.sql import SparkSession
from pyspark.sql import functions as f


#Note :- By creating the function and calling this function from write stream it will not create a state store hence we would need to add a extra logic to get the data from the preivious table/batch and add it to the current batch as state store is not there we would have to do it manually

# In this example we are not doing that

# function to calculate the word count


spark = SparkSession.builder.appName('word_count_by_avoiding_state_store').enableHiveSupport().getOrCreate()

df = spark.readStream.format('socket'). \
    option('host', 'localhost'). \
    option('port', '9988'). \
    load()


def word_count(batch_df,batch_id):
    df = batch_df.select(f.explode(f.split("value"," ")).alias('words'))
    df = df.groupBy("words").agg(f.count("words").alias("word_count"))
    df.show()

query = df.writeStream.format('console').outputMode('update').option('checkpointlocation','dir1').foreachBatch(word_count).start()

query.awaitTermination()

