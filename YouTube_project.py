#!/usr/bin/env python
# coding: utf-8

# # Three youtube information crawl packages in total

# # youtube-search-python
# - without api
# - https://github.com/alexmercerind/youtube-search-python
# - limit (int, optional): Sets limit to the number of results. Defaults to 20.
# - language (str, optional): Sets the result language. Defaults to 'en'.
# - region (str, optional): Sets the result region. Defaults to 'US'.
# 
# ## Getting video information using video link or video ID
# - Getting information about video or its formats using video link or video ID.
# 
# - `Video.get` method will give both information & formats of the video
# - `Video.getInfo` method will give only information about the video.
# - `Video.getFormats` method will give only formats of the video.
# 
# - You may either pass link or ID, method will take care itself.

# # aiotube  
# - https://github.com/jnsougata/AioTube  -- to get the number of likes

# # youtube-comment-downloader
# - https://github.com/egbertbouman/youtube-comment-downloader

# In[1]:


import pandas as pd
from datetime import datetime
from tqdm import tqdm
import os

from youtubesearchpython import *
import aiotube  # https://github.com/jnsougata/AioTube  -- to get the number of likes
# get youtube comment
from youtube_comment_downloader.downloader import download_comments # https://github.com/egbertbouman/youtube-comment-downloader
import sys
import time


class YouTube(object):
    def __init__(self, search_term,url,nosp500,comment = False, test = False,dirs = '/Users/evaking/desktop/research assistant/social media/codes/Youtube/data/'): 
        self.search_term = search_term
        self.dirs = dirs
        self.url = url
        self.nosp500 = nosp500
        self.comment = comment
        self.test = test
        self.video_error = []
        self.video_error_flag = 0
        self.video_comment_error = []
        self.video_comment_error_flag = 0
    
    # Search for channel's information

    def channel_show(self,url,nosp500):
        search_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        channel = aiotube.Channel(url)
        lt = [nosp500]
        info = channel.info
        lt.append(channel.name)
        lt.append(info['id'])
        lt.append(info['subscribers'])
        lt.append(channel.video_count)
        lt.append(info['views'])
        lt.append(info['url'])
        lt.append(channel.description)
        df = pd.DataFrame(lt).T
        df.columns = ['No.SP500','name','id','subscribers','videoCount','views','url','description']
        df['search_date'] = search_date
        
        if pd.isna(df['videoCount'])[0]:
            link = 'https://www.youtube.com/playlist?list=UU'+df.id[0][2:]
            df['videoCount'] = aiotube.Playlist(link).video_count
        
        return df
    
    ## save channel info
    def channel_info_save(self):
        
        print('\033[1mStart to crawl Channel Information of '+self.search_term+'.\033[0m')
        #channelsSearch = ChannelsSearch(self.search_term, limit = 2, region = 'US')
        #channel_result = channelsSearch.result()['result']
        #channel = self.channels_show(channel_result)
        
        channel = self.channel_show(self.url,self.nosp500)
        self.channel_id = channel.id[0]
        
        # save file for channel information
        dirs = self.dirs+'Data Crawling/'+self.search_term+'/channel information'
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        channel.to_csv(dirs+'/'+self.search_term+' channel information at '+
                  datetime.now().strftime('%Y-%m-%d')+'.csv',index = False,header = True)
        print('\033[1mChannel information saved for',self.search_term+'.\n\033[0m')
        
    # get videos in a specific channel
    def video_df(self,result):
        big_df = pd.DataFrame()
        for i in range(len(result)):
            res = result[i]
            df = pd.DataFrame([res])
            df['channel_name'] = res['channel']['name']

            big_df = pd.concat([big_df,df],axis = 0)
        big_df = big_df.drop(columns = ['thumbnails','accessibility','channel']) #pics

        big_df.reset_index(drop = True, inplace = True)
        big_df = big_df.rename(columns={'id':'video_id'})
        return big_df
    
    def video_get(self):
        link = 'https://www.youtube.com/playlist?list=UU'+self.channel_id[2:]
        playlist = Playlist(link)
        #print(f'Videos Retrieved: {len(playlist.videos)}')

        while playlist.hasMoreVideos:
            #print('Getting more videos...\n')
            playlist.getNextVideos()
            #print(f'Videos Retrieved: {len(playlist.videos)}')
        #print('Found all the videos for '+self.search_term+'.')
        return playlist
    
    def videoinfo_show(self,res):
        df = pd.DataFrame([res])
        df['view Count'] = res['viewCount']['text']
        df['channel_name'] = res['channel']['name']
        df['channel_id'] = res['channel']['id']
        df['channel_link'] = res['channel']['link']
        return df
    
    def all_video_info(self,video_id):
        df = pd.DataFrame()
        for i in tqdm(range(len(video_id))):
            try:
                vv = Video.getInfo(video_id[i])
                info = self.videoinfo_show(vv)
                info['# likes'] = aiotube.Video(video_id[i]).likes
                info['search_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                df = pd.concat([df,info],axis = 0)
            except:
                print('Fail to get video information for video:',video_id[i])
                self.video_error.append(video_id[i])
                self.video_error_flag = 1
                continue
        try:
            df = df.drop(columns = ['viewCount','thumbnails','channel']) #pics
            df = df.reset_index(drop = True)
            df = df.rename(columns={'id':'video_id'})
        except:
            df = pd.DataFrame()
        
        return df
    
    ## save video info
    def video_info_save(self):
        print('\033[1m\nStart to crawl Video Information of '+self.search_term+'.\033[0m')
        playlist = self.video_get()
        all_video = self.video_df(playlist.videos)
        self.video_id = all_video.video_id.tolist()
        self.video_count = len(self.video_id)
        if self.test:
            video_info = self.all_video_info(self.video_id[:2])
        else:
            video_info = self.all_video_info(self.video_id)
        
        try:
            video_info_simple = video_info.drop(columns = ['duration','link','channel_name','allowRatings','averageRating','isLiveNow'])
            df_videoinfo = pd.merge(all_video,video_info_simple,on=['video_id','title'])
        except:
            df_videoinfo = all_video
        
        # save file for video information
        dirs = self.dirs+'Data Crawling/'+self.search_term+'/video information'
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        df_videoinfo.to_csv(dirs+'/'+self.search_term+' video information at '+
                  datetime.now().strftime('%Y-%m-%d')+'.csv',index = False,header = True)
        print('\033[1mVideo information saved for',self.search_term+'.\n\033[0m')
    
    # get comment
    def comment_extract(self,youtube_id, sort = 1, language = None):
        # parm: limit = 50,
        # for sort: 'Whether to download popular (0) or recent comments (1). Defaults to 1'
        # language: Language for Youtube generated text
        # votes: the number of likes of comment
        # photo: avatar of comment user

        print('Extracting Youtube comments for video:', youtube_id)
        count = 0
        start_time = time.time()
        #sys.stdout.write('Downloaded %d comment(s)\r' % count)
        sys.stdout.flush()

        comment_list = []
        for comment in download_comments(youtube_id,sort,language):
            comment['search_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            comment_list.append(comment)
            count += 1
            sys.stdout.write('Extracting %d comment(s)\r' % count)
            sys.stdout.flush()
            #if limit and count >= limit:
                #break
        print('\n[{:.2f} seconds] Done!\n'.format(time.time() - start_time))
        return pd.DataFrame(comment_list)
    
    ## save comment info
    def comment_info_save(self):
        print('\033[1m\nStart to crawl Video Comment of '+self.search_term+'.\n\033[0m')
        if self.test:
            ct = 2
        else:
            ct = self.video_count
        
        for i in range(ct):
            try:
                idd = self.video_id[i]
                comment = self.comment_extract(youtube_id = idd,language = 'en')

                # save file for video information
                dirs = self.dirs+'Data Crawling/'+self.search_term+'/comment information/'+self.video_id[i]
                if not os.path.exists(dirs):
                    os.makedirs(dirs)
                comment.to_csv(dirs+'/'+self.search_term+' comment information for '+self.video_id[i]+ 'at '+
                          datetime.now().strftime('%Y-%m-%d')+'.csv',index = False,header = True)
            except:
                print('Fail to get comment information for video',idd)
                self.video_comment_error.append(idd)
                self.video_comment_error_flag = 1
                continue
            
        print('\033[1mComment information saved for',self.search_term+'.\n\033[0m')
    
    def issue_raise(self,types,error_df):
        print('\033[1m'+'\033[37m'+'\033[41m\nSomething wrong with the '+types+ ' information collection part.\n\n\033[0m')
        dirs = self.dirs+'Data crawling issue/'+types+' issue/'+datetime.now().strftime('%Y-%m-%d')+'/'
        if not os.path.exists(dirs):
                os.makedirs(dirs)
        
        if types == 'video' or types == 'video comment':
            df = error_df
        else:
            df = pd.DataFrame([self.search_term,self.url,datetime.now().strftime('%Y-%m-%d')]).T
            df.columns = ['Company_Name','Link','Search_date']
            
        df.to_csv(dirs+self.search_term+ ' at '+ datetime.now().strftime('%Y-%m-%d')+'.csv',
                  index = False,header = True)
    
    def error_df_func(self,lt,name,issue):
        error_df = pd.DataFrame(lt)
        error_df.columns = [name]
        error_df['lin'] = ['https://www.youtube.com/watch?v=' for i in range(len(error_df))]
        error_df['link'] = error_df['lin']+error_df[name]
        error_df = error_df.drop(['lin'],1)
        error_df['Company name'] = [self.search_term for i in range(len(error_df))]
        self.issue_raise(issue,error_df)
    
    # final run
    def run_once(self):
        print('Start crawling time:' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'\n')
       
        # channel information
        try:
            self.channel_info_save()
        except:
            self.issue_raise('channel',pd.DataFrame())    
       
        # video information
        self.video_info_save()
        
        if self.video_error_flag:
            self.error_df_func(self.video_error,'Error video ID','video')
            
        # comment information
        if self.comment:
            self.comment_info_save()
            if self.video_comment_error_flag:
                self.error_df_func(self.video_comment_error,'Video ID for video comment crawling error','video comment')
                
        print('End crawling time:' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print('\033[1m'+'\033[36mData crawling completed.\n\n\n\033[0m')
