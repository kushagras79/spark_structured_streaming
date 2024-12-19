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

