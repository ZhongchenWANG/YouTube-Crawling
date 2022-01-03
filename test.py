#!/usr/bin/env python
# coding: utf-8

# In[1]:


from YouTube_project import YouTube
from datetime import datetime
import pandas as pd


# In[2]:


print('\n\033[1m'+'\033[94m' + 'Today is '+datetime.now().strftime('%Y-%m-%d')+" and let's start crwaling!" + '\033[0m\n')
#company_list = ['Tesla','Apple']
#print('\n\033[1m'+'Company list:'+'\033[0m', company_list)


# In[3]:


print('\n\033[1mDefault file path:\033[0m', '/Users/evaking/desktop/research assistant/social media/codes/Youtube/data/')
dirs = input('Please input the file path, input 1 for the default settings: \n')
if dirs == str(1):
    dirs = '/Users/evaking/desktop/research assistant/social media/codes/Youtube/data/'


# In[4]:


link_list = pd.read_csv('./company youtube link.csv')
total = len(link_list)


# In[5]:


start_company = input('Please input the No. of the start company:(1 is the beginning No.)\n')


# In[6]:


lk = link_list.link
st = link_list.search_term
spno = link_list.sp500no
test = input('Please specify if you are testing the program or not. (0 for testing, 1 for crawling)\n')


# In[7]:


if test == '0':
    test = True
else:
    test = False


# In[ ]:


for i in range(int(start_company)-1,total):
    
    if pd.isna(lk)[i]:
        print('\033[1m'+'\033[30m\nThere is no youtube link for the company.\n\033[0m')
        continue
        
    com_link = lk[i]
    com_name = st[i]
    sp500no = spno[i]
    print('\033[1m'+'\033[5m'+'\033[32m\nCrawling Process: [',i+1,'/',total,'].\033[0m')
    print('\033[1m'+'\033[35m\nStart crwaling information of company:',com_name+'\n\n\033[0m')
    company = YouTube(com_name,com_link, sp500no, test = test, dirs = dirs)
    company.run_once()
    
print('\n\033[1m'+'\033[94m' + 'Today is '+datetime.now().strftime('%Y-%m-%d')+" and the crawling process is finished!" + '\033[0m\n')

