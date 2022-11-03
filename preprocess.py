import pandas as pd
import re

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'admin_message': message, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')
    df.rename(columns={'message_date': 'Date'}, inplace=True)
    users = []
    messages = []
    for message in df['admin_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])

        else:
            users.append('Notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['admin_message'], inplace=True)
    df['Year'] = df['Date'].dt.year
    df['month_num'] = df['Date'].dt.month
    df['Month'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day
    df['daily'] = df['Date'].dt.date
    df['Hour'] = df['Date'].dt.hour
    df['day_name'] = df['Date'].dt.day_name()
    df['Minute'] = df['Date'].dt.minute
    #for making heatmap and changing time duration between eg 9-10
    period = []
    for hour in df[['day_name', 'Hour']]['Hour']:
        if hour == 23:

            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))

        else:
            period.append(str(hour) + '-' + str(hour + 1))
    df['period'] = period

    return df