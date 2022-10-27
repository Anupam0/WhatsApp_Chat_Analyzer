from urlextract import URLExtract
import pandas as pd
from wordcloud import WordCloud,STOPWORDS
from collections import Counter
import emoji
import seaborn as sns


def number_of_messages(user_type,DataFrame):

    if user_type=='Group Analysis':
        return DataFrame.shape[0]
    else:
        #masking the user
        mask=DataFrame['user']==user_type
        return DataFrame[mask].shape[0]

        # return DataFrame[DataFrame['user'] == user_type].shape[0]

#total numeber of words written
def number_of_words(user_type,DataFrame):
    words = []
    if user_type=='Group Analysis':
        for items in DataFrame['message']:
            words.extend(items.split())


    else:
        mask=DataFrame['user']==user_type
        new_DataFrame=DataFrame[mask]
        for items in new_DataFrame['message']:
            words.extend(items.split())

    return len(words)

def media_shared(user_type,DataFrame):
    mask1 = DataFrame['message'] == '<Media omitted>\n'
    mask2 = DataFrame['user'] == user_type

    if user_type=='Group Analysis':
        new_DataFrame1=DataFrame[mask1]
        return new_DataFrame1.shape[0]
    else:
        new_DataFrame2 = DataFrame[mask1 & mask2]
        return new_DataFrame2.shape[0]

def url_extract(user_type,DataFrame):

    mask=DataFrame['user']==user_type
    new_DataFrame=DataFrame[mask]

    links = []
    extractor = URLExtract()

    if user_type=='Group Analysis':

        for messages in DataFrame['message']:
            links.extend(extractor.find_urls(messages))
    else:

        for messages in new_DataFrame['message']:
            links.extend(extractor.find_urls(messages))

    return len(links)

def most_active_users1(DataFrame):

    ndf1 = DataFrame[DataFrame['user']!='group_notification']
    ndf2=ndf1['user'].value_counts()
    return ndf2

def most_active_users2(DataFrame):
    ndf1 = DataFrame[DataFrame['user'] != 'group_notification']
    ndf2 = ndf1['user'].value_counts()
    # x = DataFrame[DataFrame['user']!='group_notification'].value_counts()
    d = {'Users': ndf2.index, 'Percentage of Messages': (ndf2.values / ndf1.shape[0]) * 100}
    new_df = round(pd.DataFrame(d),2)
    return new_df

    # a = x.index
    # b = x.values
    # for i in range(len(b)):
    #     plt.text(i, b[i], b[i], ha='center', va='bottom', fontsize='xx-small')
    #
    # plt.bar(a, b, color='#063970')
    # plt.xticks(rotation=90)
    # plt.xlabel('Users')
    # plt.ylabel('Number of Messages')
    # plt.show()

#creating the wordcloud

def wordcloud(user_type,DataFrame):
    if user_type=='Group Analysis':
        new_df=DataFrame
    else:
        mask=DataFrame['user']==user_type
        new_df=DataFrame[mask]
    additional=["<Media omitted>\n","<media omitted>\n","<omitted media>\n","<omitted Media>\n","Group notification"]
    stopwords=STOPWORDS.update(additional)
    wc = WordCloud(
        width=1000,
        height=1000,
        min_font_size=10,
        max_font_size=100,
        background_color='white',
        stopwords=stopwords)
    #generating the wordcloud,sep argument breaksthe words and puts them in an image
    DataFrame.wc = wc.generate(new_df['message'].str.cat(sep=' '))
    return DataFrame.wc
    #the df.wc will return an image which neds to be displayed by the matplotlib

def most_common_words(user_type, DataFrame):
    if user_type=='Group Analysis':
        new_df=DataFrame
    else:
        mask=DataFrame['user']==user_type
        new_df=DataFrame[mask]

    f = open('Hinglish stopwords.txt','r',encoding='utf-8')
    extra_stopwords = f.read()

    s1 = list(extra_stopwords.split('\n'))
    s2 = list(STOPWORDS)

    for items in s2:
        s1.append(items)

    s3 = ['<Media', 'omitted>']

    s1.extend(s3)

    temp = new_df[new_df['user'] != 'group_notification']
    ntemp = temp[temp['message'] != '<Media omitted>\n']


    new_word_list = []
    for items in ntemp['message']:
        for words in items.lower().split():
            if words not in s1:
                new_word_list.append(words)

    all_words = []
    for items in new_word_list:
        all_words.extend(items.split())

    my_counter = Counter(all_words)
    common_words1 = pd.DataFrame(my_counter.most_common(20))
    d = {'Words': common_words1[0], 'Number of times appeared': common_words1[1]}
    common_words2 = pd.DataFrame(d)
    return common_words2

def most_used_emoji(user_type,DataFrame):
    if user_type=='Group Analysis':
        new_df=DataFrame
    else:
        mask=DataFrame['user']==user_type
        new_df=DataFrame[mask]


    # the goal is to create a string to be put in the function emoji.emoji_list('funtion')
    words = []
    for messages in new_df['message']:
        words.extend(messages.split())
    # now we have a list which contains all the words in df['message'] of dataframe
    # now the goal is to convert it into a string
    my_str = ""
    for word in words:
        my_str = my_str + " " + word
    # now we have to put this string into the emoji function
    myemoji = emoji.emoji_list(my_str)

    pre_final_emoji_list = []
    for i in range(len(myemoji)):
        pre_final_emoji_list.extend(myemoji[i]['emoji'])
    # now we have another list which contains all the emojis but it also contains some extra emojis which need to be removed
    # we create two new list, one where removal characters are present and another one where final emojis are

    emojis_to_be_removed = ['️', '🏻']

    final_emoji_list = []
    for items in pre_final_emoji_list:
        if items not in emojis_to_be_removed:
            final_emoji_list.append(items)

    emoji_counter = Counter(final_emoji_list).most_common()
    emoji_counter_dataframe1 = pd.DataFrame(emoji_counter)
    emoji_counter_dataframe2 = pd.DataFrame({'Emoji': emoji_counter_dataframe1[0], 'Number of times used': emoji_counter_dataframe1[1]})

    return emoji_counter_dataframe2


def monthly_timeline_of_chats(user_type,DataFrame):
    if user_type=='Group Analysis':
        new_df=DataFrame
    else:
        mask=DataFrame['user']==user_type
        new_df=DataFrame[mask]

    timeline=new_df.groupby(['year','month','user']).count()['message'].reset_index()
    Time=[]
    for i in range(len(timeline)):
        Time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
    timeline['Time']=Time
    return timeline

def daily_timeline_of_chats(user_type,DataFrame):
    if user_type=='Group Analysis':
        new_df=DataFrame
    else:
        mask=DataFrame['user']==user_type
        new_df=DataFrame[mask]

    new_df['dateonly'] = new_df['dates'].dt.date
    date_dataframe = new_df.groupby('dateonly').count()['message'].reset_index()
    date_dataframe.rename(columns={'dateonly': 'date'}, inplace=True)
    return date_dataframe

def day_wise_statistics(user_type,DataFrame):
    if user_type=='Group Analysis':
        new_df=DataFrame
    else:
        mask=DataFrame['user']==user_type
        new_df=DataFrame[mask]

    dayname = new_df['Day name'].value_counts().reset_index()
    dayname1 = dayname.sort_values('index')
    dayname2 = dayname1.rename(columns={'index': 'Day', 'Day name': 'Number of messages'})
    return dayname2


def Month_wise_statistics(user_type,DataFrame):
    if user_type=='Group Analysis':
        new_df=DataFrame
    else:
        mask=DataFrame['user']==user_type
        new_df=DataFrame[mask]

    Monthname = new_df['month'].value_counts().reset_index()
    Monthname1 = Monthname.sort_values('index')
    Monthname2 = Monthname1.rename(columns={'index': 'Month', 'month': 'Number of messages'})
    return Monthname2


def activity_heatmap(user_type,DataFrame):
    if user_type=='Group Analysis':
        new_df=DataFrame
    else:
        mask=DataFrame['user']==user_type
        new_df=DataFrame[mask]

    new_df.rename(columns={'Day name': 'Day'}, inplace=True)
    final_pivot_table = new_df.pivot_table(index='Day', columns='Period', values='message', aggfunc='count').fillna(0)
    return final_pivot_table



