## OPTIMAL TENANT MIX ANALYTICS

The success of online stores can be attributed to the plethora of data which they collect on customer behavior. With an increase in the number of such stores, it is imperative for the retailers to step up their game and use a combination of statistical analytics and social WiFi capability, that helps the retailers to

1. Engage new customers 
2. Influence customer purchasing decisions 
3. Increase the basket size of existing customers

Each and every store plays a very important role in garnering profits for a mall. Increasing the profit of low-performance stores will highly contribute to the success of a mall. Objectives: The location of a retailer store in the layout plays a major role in attracting customers. The exposure of stores located in dead zones can be increased by identifying strategic locations through the mall at which marketing can be done for each store in a dead zone.

In order to identify the dead zones, we find the frequent paths travelled by most customers. The idea to determine the frequent paths follows the same analogy of determination of frequent itemsets baskets by malls such as Ralphs, Costco, Wallmart etc. Our project employs PCY, Multihash and Toivonen's Algorithm to find the frequent paths from which we derive the frequent stores, non frequent stores, dead zones and optimal location of the stores.

## Getting Started

1. To use this project download the project zip named 'INF560_Final_Project.zip' from USC Blackboard under INF560 section.
2. Go to 'Download' folder and unzip the contents
3. Copy and paste the folder 'INF560_Final_Project' to your desired location.

## Prerequisites:

1. Download the python from the link 'https://www.python.org/downloads/'. 
2. The link 'https://wiki.python.org/moin/BeginnersGuide/Download' has instructions to set up in one's operating system be it windows, linux or Mac.
3. PIL package should be installed additionally in order to draw the points on the maps. You can download PIL from 'http://www.pythonware.com/products/pil/'. 
4. You can install the PIL library by following the instructions on the link 'http://www.pythonware.com/products/pil/'.

## Running the enviornment and Results that follow:

1. Open the terminal in your operating system and go to the desired folder by typing the following command:
    'cd YourFolderName/INF560_Final_Project/PagesAndScripts'
2.  a. In order to run the PCY Algorithm type
        'python project_pcy.py input1.txt 7 20' 
        where "project_pcy.py" is the file name, "input1.txt" is the datafile name containing comma seperated values, "7" is the support count and "20" is the bucket size.
    b. The results are stored in the file 'pcy_log_yearmonthdate-hoursminutesecond.txt'
    c. The images 'freq_store_map.png', 'dead_zone_store_map.png', 'non_freq_store_map.png' and 'optimal_location_store_map.png' are generated in the same folder as 'PagesAndScripts'
    d. The csv files 'freq_stats.csv', 'nonfreq_stats.csv', 'frequent_paths.csv' and 'store_stats.csv' are saved in the same folder as 'PagesAndScripts'.
3.  a. In order to run the Multihash Algorithm type
        'python project_multihash.py input1.txt 7 20' 
        where "project_multihash.py" is the file name, "input1.txt" is the datafile name containing comma seperated values, "7" is the support count and "20" is the bucket size.
    b. The results are stored in the file 'multihash_log_yearmonthdate-hoursminutesecond.txt'
    c. The images 'freq_store_map.png', 'dead_zone_store_map.png', 'non_freq_store_map.png' and 'optimal_location_store_map.png' are generated in the same folder as 'PagesAndScripts'
    d. he csv files 'freq_stats.csv', 'nonfreq_stats.csv', 'frequent_paths.csv' and 'store_stats.csv' are saved in the same folder as 'PagesAndScripts'.
4. In order to run the Toivonen Algorithm type
    'python project_toivonen.py input1.txt 15' 
    where "project_multihash.py" is the file name, "input1.txt" is the datafile name containing comma seperated values, "15" is the support count and "20".
5. Open another terminal and follow the same steps as mentioned in step 1.
6. Type the command 'python -m SimpleHTTPServer' and copy the port number appearing in the command prompt or teminal..
7. Open the web browser and type 'localhost:8000/BarChart.html .
8. The results of the project are displayed in the dashboard.

## Note:

1. The results of Toivonen Algorithm are displayed in the console itself.
2. If you want to rerun the algorithms make sure that you delete 'freq_store_map.png', 'dead_zone_store_map.png', 'non_freq_store_map.png' and 'optimal_location_store_map.png' in the folder named as 'PagesAndScripts'

## Authors:

This project is authored by Mounik Muralidhara from University Of Southern California
