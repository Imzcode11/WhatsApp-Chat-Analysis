#!/usr/bin/env python
# coding: utf-8

# ## WhatsApp Chat Analysis

# #### 1.Import Regular Expression deal with text format 
# 

# In[1]:



import re
import pandas as pd


# In[2]:


f = open('WhatsApp Chat with Sahir Jio.txt','r',encoding ='utf-8')


# In[3]:


data = f.read()


# In[4]:


pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
#pattern for AM ANd PM format
#   '\d{1,2}\/\d{2,4}\/\d{2,4},\s\d{1,2}:\d{1,2}\s\w{1,2}\s-\s'


# In[5]:


message = re.split(pattern,data)[1:]


# In[6]:


dates = re.findall(pattern,data)


# In[7]:


df = pd.DataFrame({'admin_message':message, 'message_date':dates})  
df['message_date']= pd.to_datetime(df['message_date'],format= '%d/%m/%Y, %H:%M - ')
df.rename(columns = {'message_date': 'Date'}, inplace = True)
df.head(4)


# In[8]:


#separate user and message
users = []
messages = []
for message in df['admin_message']:
    entry = re.split('([\w\W]+?):\s', message)
    if entry[1:]: #user name
        users.append(entry[1])
        messages.append(entry[2])
        
    else:
        users.append('Notification')
        messages.append(entry[0])
        
df['user'] =users
df['message'] = messages


df.head(2)



# In[9]:



# Removing Extra Columnns
df.drop(columns=['admin_message'], inplace = True)


# In[10]:


df.head(3)


# In[11]:


#Changing Date columns to be more specific
df['Year']   =  df['Date'].dt.year
df['Month']  =  df['Date'].dt.month_name()
df['day'] =     df['Date'].dt.day
df['Hour'] =    df['Date'].dt.hour
df['Minute']=   df['Date'].dt.minute


# In[12]:


df.head(3)


# In[13]:


df[df['message']== '<Media omitted>\n'].shape[0]


# In[14]:


word = []
for message in df['message']:
    word.extend(message.split())


# In[15]:


len(word)


# In[16]:


new = df[df['message'] == '<Media omitted>\n'].shape[0]
new


# In[17]:


with open('WhatsApp Chat with Sahir Jio.txt') as file:
    for line in file:
        urls = re.findall('https?://(?:[-\w]|(?:%[\da-fA-F]{2}))+',line)
        print(urls)


# In[18]:


from urlextract import URLExtract 
extract = URLExtract()


# In[19]:


links = []
for message in df["message"]:
    links.extend(extract.find_urls(message))
    
  
   


# In[20]:


len(links)


# In[21]:


x = df['user'].value_counts().head(2)


# In[22]:


import matplotlib.pyplot as plt
name = x.index
count = x.values


# In[23]:


plt.bar(name,count,color= 'green')


# In[24]:


# percentages of msg send
Percent =round(df['user'].value_counts().head(2)/df.shape[0]*100,2)
Percent


# In[26]:


chats_percentage= round(df['user'].value_counts().head(2)/df.shape[0]*100,2).reset_index().rename(columns={'index':'Name','user':'Percent'})
chats_percentage


# In[33]:


exp= [0.1,0]
plt.pie(chats_percentage['Percent'], labels= chats_percentage['Name'] ,explode= exp);


# In[34]:


from wordcloud import WordCloud
wc = WordCloud(width=800,height=800,min_font_size=10, background_color='white')
df_wc =wc.generate(df['message'].str.cat(sep= " "))
df_wc


# In[35]:


plt.figure(figsize=(10,10))
plt.imshow(df_wc)
plt.axis('off');


# In[36]:


words = []
for message in df['message']:
    words.extend(message.split())


# In[37]:


words


# In[38]:


from collections import Counter


# In[39]:


Counter(words)


# In[40]:


counts =Counter(words).most_common(20)
counts


# In[41]:


#convert into data frame
pd.DataFrame(counts)


# ### Removing  notification , media omitted

# In[43]:


temp = df['user'] != 'Notification'
temp


# In[44]:


temp = df[df['user'] != 'Notification']
temp= temp[temp['message'] != '<Media omitted>\n']


# In[45]:


f = open('hinglish.txt','r')
stop_word = f.read()


# In[46]:


print(stop_word)


# In[47]:


words = []
for message in temp['message']:
    for word in message.lower().split():
        if word not in stop_word:
            words.append(word)
  


# In[48]:


print(words)


# In[49]:


pd.DataFrame(Counter(words).most_common(20))


# In[50]:


df['month_num'] = df['Date'].dt.month


# In[51]:


df.groupby(['Year','month_num']).count()


# In[52]:


Time_line =df.groupby(['Year','month_num','Month']).count()['message'].reset_index()
Time_line


# In[53]:


#mearing year and months columns
time= []
for i in range(Time_line.shape[0]):
    time.append(Time_line['Month'][i]+ '-'+str(Time_line['Year'][i]))


# In[54]:


time


# In[55]:


Time_line['time'] =time


# In[56]:


Time_line


# In[57]:


plt.plot(Time_line['time'],Time_line['message'])
plt.xticks(rotation = 90)
plt.show()


#  ### Chats frequency per day

# In[58]:


df['daily'] =df['Date'].dt.date


# In[59]:


daily_timeline =df.groupby ('daily').count()['message'].reset_index()
daily_timeline


# In[61]:


plt.figure(figsize= (18,10))
plt.plot(daily_timeline['daily'],daily_timeline['message']);


# In[62]:


df['day_name'] = df['Date'].dt.day_name()


# In[63]:


df['day_name'].value_counts()


# In[64]:


yeah =df.groupby ('day_name').count()['message'].reset_index()
yeah


# In[65]:


# chatting krne ka waqt

period = []
for hour in df[['day_name','Hour']]['Hour']:
    if hour == 23:
        
        period.append(str(hour)+ "-"+str('00'))
    elif hour == 0:
        period.append(str('00')+ "-"+str(hour+1))                                 
                                         
    else: 
        period.append(str(hour)+ '-'+str(hour+1))
                                         
                                         
                                         


# In[66]:


df['period'] = period


# In[67]:


df.head(3)


# In[68]:


import seaborn as sns
plt.figure(figsize=(16,8))
sns.heatmap(df.pivot_table(index= 'day_name',columns = 'period', values= 'message',aggfunc ='count').fillna(0))
plt.yticks(rotation ='horizontal')
plt.show()


# In[ ]:




