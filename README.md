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

## Changes to prevent possible crawling failure.
1. 326 shorlisted companies (500 S&P 500 companies originally) Selection critiera: * Whether there is YouTube channel; * Whether the number of subscribers of the corresponding company is bigger than 1k. (The file name is called new company youtube link.csv)
2. Automatically divide the all 326 companies into 7 groups (Indicating one group for one day, so the crawling frequency is per week). 50 companies for first 6 days and the remaining 26 companies on Sunday.
3. The program will wait for one minute (You can choose your own preference) after crawling one company and will wait for additional 5 minutes after crawling 10 companies.
4. Do not crawl the video comment at this stage. (While you can still choose to crawl the video comment in the initial pop-up settings.)

## Update
- I have update the test.py file and YouTube_project.py file according to the changes above.

## Attention
The test.py file, the YouTube_project.py file and the company youtube link.csv file should be in the same folder.

The program will automatically create the folder for different companies and the issue folder if there's any issue when crawling.
