# YouTube-Crawling

## Goal
To crawl the YouTube data without using API.

## Set up
You need to install the following packages for the crawling process:
- youtube-search-python: https://github.com/alexmercerind/youtube-search-python
- aiotube: https://github.com/jnsougata/AioTube
- youtube-comment-downloader: https://github.com/egbertbouman/youtube-comment-downloader
- tqdm: https://github.com/tqdm/tqdm#installation
- pandas
- numpy
- datetime
- time

## test.py
Run the test.py file in your terminal.

## Choose your own preference for crawling settings at the beginning:
1. `Please input the file path, input 1 for the default settings:`: You can input your preferred file path for new company youtube link.csv.
2. `Please input you preference for crawling:(Input 1 for default crawling, 2 for crwaling failure solution -- discard video comment at this stage.)`: You can input 2 if you do not want to crawl video comment information at this stage.
3. `Do you want to split the companies into 7 batches? (Input 1 for yes, 0 for no.)`: If you want to crawl different batches of companies on different day in on week, you can input 1.
4. `Please input the file path, input 1 for the default settings:`: This is the file path where you want to save your data.
5. `Please specify if you are testing the program or not. (0 for testing, 1 for crawling)`: If you just want to test the program, input 0 and the program will only crawl top two videos in one YouTube channel.
6. `Please specify the stop time after each crawling for one company.(In seconds, suggested setting is 60 --> stop for 1 min.)`: For the sake of preventing crawling failure, it is highly suggested to wait for 60 seconds after crawling one company.

## Changes to prevent possible crawling failure.
1. 326 shorlisted companies (500 S&P 500 companies originally) Selection critiera: * Whether there is YouTube channel; * Whether the number of subscribers of the corresponding company is bigger than 1k. (The file name is called new company youtube link.csv)
2. Automatically divide the all 326 companies into 7 groups (Indicating one group for one day, so the crawling frequency is per week). 50 companies for first 6 days and the remaining 26 companies on Sunday.
3. The program will wait for one minute (You can choose your own preference) after crawling one company and will wait for additional 5 minutes after crawling 10 companies.
4. Do not crawl the video comment at this stage. (While you can still choose to crawl the video comment in the initial pop-up settings.)

## Update
- I have update the test.py file and YouTube_project.py file according to the changes above.
- New update on Feb 8 2022: The program is more robust. 1. The program will raise the alert if one crawling step fails but still continue to crawl. 2. There will be a file stating the information for failed crawling.

## Attention
The test.py file, the YouTube_project.py file and the (new) company youtube link.csv file should be in the same folder.

The program will automatically create the folder for different companies and the issue folder if there's any issue when crawling.
