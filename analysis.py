import pandas as pd
from urlextract import URLExtract
import emoji
from collections import Counter


def dataframe(selected_user, df):
    if selected_user!= "Overall":
        df = df[df["user"]==selected_user]
    return df

def fetch_kpi(selected_user, df):
    if selected_user!= "Overall":
        df = df[df["user"]==selected_user]
    
    num_messages = df.shape[0]


    words = []
    links = []
    for message in df["message"]:
        words.extend(message.split())
        extract = URLExtract()
        links.extend(extract.find_urls(message))

    num_media = df[df["message"]=="<media omitted>\n"].shape[0]

    return num_messages, len(words), num_media, len(links)

def most_busy_user(df): 
    x = df['user'].value_count().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index': 'name', 'user':'percent'})

def most_common_words(selected_user, df):
    if selected_user!= "Overall":
        df = df[df["user"]==selected_user]

    #c1= df['user']!='group_notification'
    #c2 = df['message']!= '<Media omitted>\n'
    #c3 = df['message']!= 'This message was deleted'
    #df1 = df[c1]
    #df2 = df1[c2]
    #df3 = df2[c3]
    #temp= df[df['user']!='group_notification']
    #temp= temp[temp['message']!= '<Media omitted>\n']
    words = []
    #for message in df["message"]:
     #   for word in message.lower().split():
      #      words.append(word) 
    #words_df = pd.DataFrame(Counter(words).most_common(10))
    
    for message in df['message']:
        for word in message.lower().split():
            words.append(word) 
    words_df = pd.DataFrame(Counter(words).most_common(10))
    return words_df



def monthly_timeline(selected_user, df):
    if selected_user!= "Overall":
        df = df[df["user"]==selected_user]
# groupby creates a df, 
    timeline_df = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index() 
     # reset_index =  arranges the index in order

    time=[]
    for i in range(timeline_df.shape[0]):
        time.append(timeline_df['month'][i]+"-"+ str(timeline_df['year'][i]))
    
    timeline_df['time']=time

    return timeline_df
 #   return

#def(user, data):
#    return

def daily_timeline(selected_user, df):
    if selected_user!= "Overall":
        df = df[df["user"]==selected_user]   

    daily_timeline_df = df.groupby(['date']).count()['message'].reset_index()
    
    return daily_timeline_df  


def weekly_timeline(selected_user, df):
    if selected_user!= "Overall":
        df = df[df["user"]==selected_user]
    
    return df["day_name"].value_counts()

def monthly_activity(selected_user, df):
    if selected_user!= "Overall":
        df = df[df["user"]==selected_user]
           
    return df["month"].value_counts()  


def emojis(selected_user, df):
    if selected_user!= "Overall":
        df = df[df["user"]==selected_user]
    
    emojis = []
    for message in df["message"]:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(10))
    return emoji_df