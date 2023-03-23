# Processes the text file based on different category, name/number, msg, date time, emojis 
# re  - regular expression, for string manipulation and pattern matchig of the strings.
import re     # standard library  re = regex
import datetime
import numpy as np
import pandas as pd  # for dataframe
import streamlit as st


# define function 
def preprocess(data):
    pattern =  "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[\w][\w]\s-" # describe date   \d for extracting integer from string
  
    dates = re.findall(pattern, data)  # data  -  user uploaded file
    message = re.split(pattern, data)[1:]  # slicing for extracting only the messages


    df = pd.DataFrame({"date_time": dates, "user_message": message})  

    # removing the , : in the dataframe 

    df["date_time"] = pd.to_datetime(df["date_time"], format="%d/%m/%Y, %I:%M %p -") # %d for % I for 12hur format, %h for 24 hour

    user = []
    messages = []
    # for spliting the name and message
    for i in df["user_message"]:
        entry = re.split("([\w\W]+?):\s", i)  
        if entry[1:]:  # considering msg hence entry[1:]  |entry[0:] -  user name
            user.append(entry[1]) #name or phone number
            messages.append(entry[2]) # messages
        else:
            for k in entry:
                entry2 = re.split("([\w\W]+?)\sj", k)  # j is of the joined
                if entry2[1:]:
                    user.append(entry2[1]) # to ascces all the  notification msgs like "joined the group"
                    messages.append("Joined using this link")
                else:
                    for i in entry2:
                        entry3= re.split('([\w\W]+?)\sadded',i)
                        if entry3[1:]:
                            user.append(entry3[2])
                            messages.append("added to group")
                        else: 
                            #for i in entry:
                                #entry4 = re.split("([\w\W]+?)and", i)
                                #if entry4[1:]:
                                 #   user.append(entry4[1])
                                  #  user.append(entry4[2])
                                #else:   
                                #    for i in entry:
                                 #       entry5 = re.split("([\w\W]+?),([\w\W]+?),([\w\W]+?)and", i)
                                  #      if entry5[1:]:
                                   #         user.append(entry5[1])
                                    #        #user.append(entry5[2]) 
                                     #   else:
                            user.append('group notification')
                            messages.append(entry2[0])
                                        
              

    df["user"] = user
    df["message"] = messages
    df.drop(columns=["user_message"], inplace = True)
    df['year'] = df['date_time'].dt.year
    df['month_num'] = df['date_time'].dt.month
    df['month'] = df['date_time'].dt.month_name()
    df['day'] = df['date_time'].dt.day
    df['day_name']= df['date_time'].dt.day_name()
    df['hour'] = df['date_time'].dt.hour
    df['minute'] = df['date_time'].dt.minute
    df['date'] = df['date_time'].dt.date
    df.drop(columns=["date_time"], inplace = True)
    
    #df = df[df['user']!='group_notification']
    #df = df[df['message']!= '<Media omitted>\n']
    #df = df[df['message']!= 'This message was deleted']
    
    
    return df


    #inactive_users=[]
    #for i in df["messages"]:
      #  n = re.split("([\w][\W]+?):\s", i) 
       # if n[1:]:
        #    inactive_users.append(n[0])
         #   user.append(n[0])
    #return df







        


