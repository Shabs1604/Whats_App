import streamlit as st
import matplotlib.pyplot as plt
#import seaborn as sns
import pandas as pd
import preprocessor as pre
import analysis as ana

st.sidebar.title("WhatsApp Chat Analyser")

user_file = st.sidebar.file_uploader("Choose a text file containing the raw WhatsApp Data", type=["txt"], accept_multiple_files=False)

if user_file is not None:
    byte_data = user_file.getvalue()   # Gets the data byte wise
    data = byte_data.decode('utf-8')   # utf as it containg special characters
    
    df = pre.preprocess(data)
    v1 = st.title("Whatsapp chat")
    v2 = st.dataframe(df)

    df = df[df['user']!='group_notification']
    df = df[df['message']!= '<Media omitted>\n']
    df = df[df['message']!= 'This message was deleted\n']

    # Fetch the unique data

    user_file = df['user'].unique().tolist()  # converting it to list to add it into the selection box
    user_file.sort()
    user_file.remove('group notification')
    user_file.insert(0, 'Overall')

    v3 = st.header("Total Members")
    v4 = st.title(len(user_file))

    selected_user = st.sidebar.selectbox("Show analysis", user_file)

    if st.sidebar.button("Show Analysis"):

        v1.empty()
        v2.empty()
        v3.empty()
        v4.empty()

        
        user_df = ana.dataframe(selected_user,df)
        a1 = st.title("Selected user's chats")
        a2 = st.dataframe(user_df)
        a3 = st.title("Selected user's statistics")
        num_messages,num_words,num_media,num_links = ana.fetch_kpi(selected_user,df)
        
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            b1 = st.header("Total Messages")
            b2 = st.title(num_messages)
        with col2:
            b3 = st.header("Total Words")
            b4 = st.title(num_words)
        with col3:
            b5 = st.header("Total Media")
            b6 = st.title(num_media)
        with col4:
            b7 = st.header("Total Links")
            b8 = st.title(num_links)
        

        # Timeline of Activity 
        if user_df.empty:
            st.header("Non active user")
        else:
            if user_df.shape[0]>=5:
                st.title("Monthly Activity")
                timeline_df = ana.monthly_timeline(selected_user, df)
                fig,ax = plt.subplots()
                plt.bar(timeline_df['time'],timeline_df['message'], width=0.3)
                plt.xlabel('Month')
                plt.ylabel("Frequency of messages")        
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)       
        
                st.title("Daily Activity")
                daily_timeline_df  = ana.daily_timeline(selected_user, df)
                fig,ax = plt.subplots()
                plt.scatter(daily_timeline_df['date'],daily_timeline_df['message'], color ='red')
                plt.xlabel('Day')
                plt.ylabel("Frequency of messages")        
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig) 

                st.title("Activity map") 
                cl1, cl2 = st.columns(2)

                with cl1:
                    st.header("most active days")
                    busy_day = ana.weekly_timeline(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_day.index, busy_day.values, color = "orange", width=0.3)
                    plt.xlabel('date')
                    plt.ylabel("Frequency of messages")        
                    plt.xticks(rotation = 'vertical')
                    st.pyplot(fig)

                with cl2:
                    st.header("most active months")
                    busy_month = ana.monthly_activity(selected_user, df)
                    fig, ax = plt.subplots()
                    ax.bar(busy_month.index, busy_month.values, color = "green", width=0.3)
                    plt.xlabel('Month')
                    plt.ylabel("Frequency of messages")        
                    plt.xticks(rotation = 'vertical')
                    st.pyplot(fig) 
            
      
        #time(month_name)


    #  timeline of daily activity/weekly as well 
    # no of msgs done per day by the user
    
    # Activity map of the user 
    #  Most busy days wtr the user selected /overall(in separate plots)
    #  Most busy month wrt the user (in a separate plot )
    

                if selected_user=="Overall":
                    st.title("Most busy Users")

                    busy_user,new_df = ana.most_busy_user(df)
                    fig,ax = plt.subplots

                    cl1,cl2 = st.clumns(2)

                    with cl1:
                        fig, ax = plt.subplots()
                        ax.bar(busy_user.index, busy_user.values, color = "green", width=0.3)
                        plt.xlabel('User')
                        plt.ylabel("Frequency of messages")        
                        plt.xticks(rotation = 45)
                        st.pyplot(fig)

                    with cl2:
                        st.dataframe(new_df)
                                    # Most common WORDS
                
                st.title("Most common words")
                words_df = ana.most_common_words(selected_user, df)
                cl1,cl2 = st.columns(2)
                #if words_df.shape[0]>10:
                with cl1:
                    fig, ax = plt.subplots()
                    ax.bar(words_df[0], words_df[1], color = "yellow", width =0.3)
                    plt.xlabel('Common words')
                    plt.ylabel("Frequency of messages")  
                    plt.xticks(rotation = 45)      
                    st.pyplot(fig)


                with cl2:
                    st.dataframe(words_df)
                #else:
                   # st.write("Not enough data found")



                st.title("Most common emoji's used")
                emoji_df = ana.emojis(selected_user, df)

                if emoji_df.empty:
                    st.write("No emojis found")
                else:
                    cl1,cl2 = st.columns(2)

                    with cl2:
                        fig, ax = plt.subplots()
                        ax.pie(emoji_df[1], labels= emoji_df[0])
                        plt.legend(emoji_df[0], loc = "best")      
                        st.pyplot(fig)

            else:
                col1.empty()
                col2.empty()
                col3.empty()
                col4.empty() 
                #a1.empty()
                #a2.empty() 
                a3.empty()
                b1.empty()
                b2.empty()
                b3.empty()
                b4.empty()
                b5.empty()
                b6.empty()
                b7.empty()
                b8.empty()
                st.title("Not enough data is found for this user to display the statistics")
                

            





