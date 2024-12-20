# spark_structured_streaming
This repo will contain the practical for spark streaming

In order to use socket as source open your terminal and type `nc -lk <port_number>`
Then in the same terminal we can manually type the data.

for word_count_using_file_source put the file inside `data/input/` our application will pick the file and do a word count.

Different output mode:-
* complete
* update
* append


Complete:- This mode will output the full aggregation after every batch. i.e it will combine result of previous batches with latest batch and display the full result

Update:- This mode will output only the new/updated data. It will not show the data of previous batches if the data is not present in the current micro batch.

Append:- This mode will output only the new record added in the micro batch. It does not update the existing records because of which it doesnot work with streaming aggregation.


Triggers defines the timing of streaming data processing.

Different trigger mode:- 
* Unspecified
* fixed interval
* available now

1. Unspecified :- When in write stream no other triggers are specified. It is set by default.
2. fixedInterval:- In this our streaming application will wait for specified time duration and then re run the application. In the scenario were one of the batch is running for the long time then next batch will only run after previous run is over.
3. available now;- In this type of trigger spark application stops after a batch is completed.It does not wait for next set of records to come.


Aggregation in spark streaming is of 2 types:- 
1. Continuous aggregation i.e there is no time limit on the aggregation. all the aggregation will happened from start to end.
2. Time bound aggregation i.e. there is a fixed time limit on the aggregation for the data.

there is 2 type of time bound(window) aggregation 
1. Tumbling window :- Fixed width non overlapping window of time frame
 eg 11:00 => 11:15
    11:15 => 11:20
2. Sliding window:- Fixed width overlapping window of time frame
eg 11:00 => 11:15
    11:05 => 11:20
    11:10 => 11:25