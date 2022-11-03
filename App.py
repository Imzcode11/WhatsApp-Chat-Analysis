import streamlit as st
import pandas as pd
import preprocess
import helper
import seaborn as sns

import matplotlib.pyplot as plt



st.sidebar.title('WhatsApp chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose your file')
if uploaded_file is  not None:
    bytes_data = uploaded_file.getvalue()
    data =bytes_data.decode('utf-8')
    df = preprocess.preprocess(data)

    #st.dataframe(df)   ,hiding the actual chats
    # fatch unique user
    user_list = df['user'].unique().tolist()

    #user_list.remove('Notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox('Show Analysis wrt',user_list)

    if st.sidebar.button('Show Analysis'):
        #stats here
        num_messages, word , num_media_message,links = helper.fetch_stats(selected_user,df)
        st.title('WhatsApp Chats Statistics')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(word)

        with col3:
            st.header('Media Shared')
            st.title(num_media_message)

        with col4:
            st.header('Links Shared')
            st.title(links)

        # monthly timeline
        st.title('Chats Frequency per Months')
        timeline =helper.monthly_timeline(selected_user,df)
        fig ,ax= plt.subplots()
        plt.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # daily timeline
        st.title('Daily chats')
        daily_timeline = helper.daily_timeline1(selected_user,df)
        fig, ax = plt.subplots()
        plt.plot(daily_timeline['daily'], daily_timeline['message'],color = 'red')
        st.pyplot(fig)
        #din k hisab se chats
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        with col1:
            st.header('Most busy day')
            busy_day =helper.daily_chats(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values, color = 'purple')
            plt.xticks(rotation=60)

            st.pyplot(fig)

        with col2:
            st.header('Most busy Month')
            months = helper.month_activity(selected_user,df)
            fig,ax =plt.subplots()
            ax.bar(months.index, months.values ,color ='black')
            plt.xticks(rotation=90)
            st.pyplot(fig)
        st.title('Weekly Activity Heat Map')
        heatmap = helper.activity_heatmap(selected_user,df)
        fig ,ax =plt.subplots()
        ax = sns.heatmap(heatmap)
        st.pyplot(fig)


        # Which one send more messages
        if selected_user == 'Overall':

            st.title('Send Most Messages')
            x ,new_df = helper.most_send_messages(df)
            fig, ax =plt.subplots()


            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color = 'green')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #word cloud
        st.title('Word Cloud')
        df_wc =helper.create_wordcloud(selected_user,df)
        fig, ax =plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #  Most Common Word
        most_common_df = helper.most_common_word(selected_user, df)
        fig ,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1], color = 'orange')
        plt.xticks(rotation = 'vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

