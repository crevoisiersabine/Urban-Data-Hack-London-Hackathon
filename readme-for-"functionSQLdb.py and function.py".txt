Estimating the number of parking spaces occupied at each time
The python script function.py reads in the file:
“ParkingCashlessTransactionsThisFinYear_head_minimal.csv” and creates a dictionary of dictionaries.

The first dictionary contains keys for each bay.

The nested dictionary then contains a key for each one hour parking period that exists in that bay. For example if the bay has a parking event from 12h15 to 18h17, there will be 7 keys entered:
[12 - 13]
[13 - 14]
[14 - 15]
[15 - 16]
[16 - 17]
[17 - 18]
[18 - 19]
To avoid checking unnecessary time periods (where no events exist), a variable windowDur is created that checks for that particular bay event what the parking duration was and only looks at that timeframe for that particular bay event.

Iterating through each cashless transaction, a value is added per bay and per hourly time corresponding to whether a payment was made during that time.
For example if there is a cashless transaction for 12-13 in bay 344, then the dictionary entry will be:
{344 {12 - 13 [1]}}
If another cashless transaction is found for 12.15-12.30, the dictionary entry will be updated as such:
{344 {12 - 13 [1.25]}}

This would be possible in bay 344 if there was at least 2 spaces available. The only instance where you might get occupancy values that are greater than spaces available within the bay is because the minimum payment period is 30mins and therefore you may get instances of someone leaving before their time has ended and someone arriving within that timeframe and hence getting overlap of payment without physical overlap of car spaces.

The code then writes this dictionary onto a csv file called ‘output.csv’ where the first column corresponds to the bay number, the second column to the time stamp and the third column to the numerical value of occupied spaces within that bay within that time stamp hour.

The same code figures in ‘function_SQLdb.py’ but instead of writing to a csv file, it writes to the SQL database. Before it writes to the database it also checks that there is an existing entry for the bay key (in the table which gives the longitude and latitude coordinates) and if there is not, it does not write that line - this is to avoid having information about bays that we could not locate on the map because we were not given geo-coordinates for them.
