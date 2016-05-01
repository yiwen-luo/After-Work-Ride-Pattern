### storytelling
#### retrieve data from uber api and store surge price multiplier to dynamodb for six different companies in Manhattan every 5 seconds for further analysis


####
Some configuration files are not uploaded since they contains either api keys or AWS credentials

#### 
Makefile is for easier deploy of application. `make clean` could be used to clear uncorrelated files. I define `make` for different functionality, either `main.py` for testing of data retrieving, or `plot.py` for getting analyzed information necessary for further testing.

####
`main.py` is used to retrieve data from uber api to get uber surge multiplier information. Then the data are stored into DynamoDB in the format of `{name, time, surge_multiplier, lat, lon}`. `name` means company name. `lat` and `lon` represented latitude and longitude of the company's main entrance. These information are specified in the `location.json` file. `surge_multiplier` is the current surge multiplier around the location that we are interested. It has an infinite loop to retrieve uber api. One could just type `python main.py` or in AWS, type `nohup python main.py &`. AWS trigger could be used to detect exceptions.

####
I use a small nodejs tool to export the DynamoDB data into a csv file, rather than the original AWS export function pipeline. The command is: `node dynamoDBtoCSV.js -t [db name] > output.csv`.

####
`plot.py` read the csv data file and analyzed the averaged surge multiplier information for further use. It stored the favored surge information from noon to midnight to a local tsv file, for the use to plot Google charts. The stored data format could be checked by taking look at the `data.tsv` file. Usage is `python plot.py`.

####
`database.py` contains utility functions for accessing AWS DynamoDB.

####
`index.html` is used to plot the uber surge multiplier vs time range by using Google chart. One could just open the html file in Firefox. Chrome does not perform perfect since it assures one to deploy the web application on a server. It uses `d3js` to open the local tsv file and extracts the data as required json array.

####
`mapquest.py` does similar job to retrieve incident information. 