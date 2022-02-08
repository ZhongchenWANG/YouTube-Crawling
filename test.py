#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from YouTube_project import YouTube
from datetime import datetime
import pandas as pd
import time


# In[ ]:


print('\n\033[1m'+'\033[94m' + 'Today is '+datetime.now().strftime('%Y-%m-%d')+" and let's start crwaling!" + '\033[0m\n')


# In[ ]:


print('\n\033[1mDefault file path for youtube link:\033[0m', '/Users/evaking/desktop/research assistant/social media/codes/Youtube/new company youtube link.csv')
link_path = input('Please input the file path, input 1 for the default settings: \n')
if link_path == str(1):
    link_path = '/Users/evaking/desktop/research assistant/social media/codes/Youtube/new company youtube link.csv'


# In[ ]:


link_list = pd.read_csv(link_path)
total = len(link_list)


# In[ ]:


print('\n\033[1mDefault crawling:\033[0m', 'Crawl all the data including channel information, video information and video comment.')
craw_block = input('Please input you preference for crawling:(Input 1 for default crawling, 2 for crwaling failure solution -- discard video comment at this stage.) \n')


# In[ ]:


batches = input('\n\033[1mDo you want to split the companies into 7 batches? (Input 1 for yes, 0 for no.\033[0m) \n')


# In[ ]:


weekday = datetime.now().weekday()
if weekday == 0:
    weekday_name = 'Monday'
    dat = 'First 50 companies.'
    beg = 0
    end = 50
elif weekday == 1:
    weekday_name = 'Tuesday'
    dat = 'Companies 51 - 100.'
    beg = 50
    end = 100
elif weekday == 2:
    weekday_name = 'Wednesday'
    dat = 'Companies 101 - 150.'
    beg = 100
    end = 150
elif weekday == 3:
    weekday_name = 'Thursday'
    dat = 'Companies 151 - 200.'
    beg = 150
    end = 200
elif weekday == 4:
    weekday_name = 'Friday'
    dat = 'Companies 201 - 250.'
    beg = 200
    end = 250
elif weekday == 5:
    weekday_name = 'Saturday'
    dat = 'Companies 251 - 300.'
    beg = 250
    end = 300
else:
    weekday_name = 'Sunday'
    dat = 'Companies 301 - 326.'
    beg = 300
    end = 326


# In[ ]:


print('\n\033[1mThe new file have',total,'companies in total.\033[0m')
if batches == str(1):
    print('\n\033[1m'+'\033[94m' 
          + 'Since you want to split the companies, Today is '+weekday_name+" so today we will crawl the "+ dat + '\033[0m\n')
    short_link_list = link_list.iloc[beg:end,:].reset_index(drop = True)
else:
    print('\n\033[1m'+'\033[94m' 
          + "Since you don't want to split the companies, we will crawl all ", total, " companies in the file.\033[0m\n")
    short_link_list = link_list


# In[ ]:


print('\n\033[1mDefault file path:\033[0m', '/Users/evaking/desktop/research assistant/social media/codes/Youtube/data/')
dirs = input('Please input the file path, input 1 for the default settings: \n')
if dirs == str(1):
    dirs = '/Users/evaking/desktop/research assistant/social media/codes/Youtube/data/'


# In[ ]:


#start_company = input('\nPlease input the No. of the start company:(1 is the beginning No.)\n')


# In[ ]:


lk = short_link_list.link
st = short_link_list.search_term
spno = short_link_list.sp500no
test = input('\n\033[1mPlease specify if you are testing the program or not.\033[0m (0 for testing, 1 for crawling)\n')


# In[ ]:


if test == '0':
    test = True
else:
    test = False


# In[ ]:


tim = input('\n\033[1mPlease specify the stop time after each crawling for one company.\033[0m(In seconds, suggested setting is 60 --> stop for 1 min.)\n')


# In[ ]:


print('\n\033[1mKindly remind that there will be 5 minutes stop time after crawling 10 companies.\033[0m\n')


# In[ ]:


#for i in range(int(start_company)-1,total):
for i in range(len(short_link_list)):

    if pd.isna(lk)[i]:
        print('\033[1m'+'\033[30m\nThere is no youtube link for the company.\n\033[0m')
        continue

    com_link = lk[i]
    com_name = st[i]
    sp500no = spno[i]
    print('\033[1m'+'\033[5m'+'\033[32m\nCrawling Process: [',i+1,'/',len(short_link_list),'].\033[0m')
    print('\033[1m'+'\033[35m\nStart crwaling information of company:',com_name+'\n\n\033[0m')
    if craw_block == str(1):
        company = YouTube(com_name,com_link, sp500no, comment = True,test = test, dirs = dirs)
    else: 
        company = YouTube(com_name,com_link, sp500no, comment = False,test = test, dirs = dirs)
    company.run_once()
    print('\nStop crawling for',tim,'seconds.\n\n')
    time.sleep( int(tim))
    
    if not (i+1)%10:
        print('\n\033[1mHave crawled',i+1,'companies already, stop crawling for 5 minutes for fear of crawling failure.\033[0m')
        time.sleep( 300 )

print('\n\033[1m'+'\033[94m' + 'Today is '+datetime.now().strftime('%Y-%m-%d')+" and the crawling process is finished!" + '\033[0m\n')
