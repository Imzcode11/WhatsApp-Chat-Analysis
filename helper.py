from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    word = []
    for message in df['message']:
        word.extend(message.split())
    #to know about media which we shared in chats
    num_media_message = df[df['message'] == '<Media omitted>\n'].shape[0]
                     #df[df['message'] == '<Media omitted>\n'].shape[0]
    #to know about links which we shared in chats
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(word), num_media_message ,len(links)


def most_send_messages(df):
    x = df['user'].value_counts().head(2)
    df= round(df['user'].value_counts().head(2) / df.shape[0] * 100, 2).reset_index().rename(
        columns={'index': 'Name', 'user': 'Percent'})
    return x,df


def create_wordcloud(selected_user,df):
    f = open('hinglish.txt', 'r')
    stop_word = f.read()

    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    temp = df[df['user'] != 'Notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_word:
                y.append(word)

        return " ".join(y)


    wc = WordCloud(width=500,height=500,min_font_size=10, background_color='white')

    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc =wc.generate(temp['message'].str.cat(sep= " "))
    return df_wc


def most_common_word(selected_user, df):
    f = open('hinglish.txt','r')
    stop_word =f.read()

    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    temp = df[df['user'] != 'Notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_word:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    timeline = df.groupby(['Year', 'month_num', 'Month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + '-' + str(timeline['Year'][i]))

    timeline['time'] = time

    return timeline



def daily_timeline1(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    daily_timeline = df.groupby('daily').count()['message'].reset_index()

    return daily_timeline


def daily_chats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    daily = df['day_name'].value_counts()
    return daily


def month_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    return df['Month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user]

    heat_map=  df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return heat_map
