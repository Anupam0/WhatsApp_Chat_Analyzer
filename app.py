"""#to run this file, go to local terminal and run the command streamlit run app.py"""
import streamlit as st
import pandas as pd
import preprocessor
import helper
import matplotlib.pyplot as plt
import plotly.express as px
import emoji
from urlextract import URLExtract
import seaborn as sns


st.sidebar.title('Whatsapp Chat Analyzer')

#uploading a file
#https://docs.streamlit.io/library/api-referen  ce/widgets/st.file_uploader
uploaded_file = st.sidebar.file_uploader("Choose a whatsapp imported chat file (The file will be in .text format")
if uploaded_file is not None:
# To read file as bytes:
    bytes_data = uploaded_file.getvalue()
#https://www.geeksforgeeks.org/python-strings-decode-method/
#the file now is in stream data,and we have to convert it into strings of data,
#but it has to be converted into strings data, so we have to use the .decode() function
    data = bytes_data.decode('utf-8')
#the preprocessor functions is linked from here
    df= preprocessor.preprocess(data)
#to display the data frame
    #st.dataframe(df)
#fetch unique users
#https://pandas.pydata.org/docs/reference/api/pandas.Series.unique.html
#https://www.javatpoint.com/numpy-array-tolist#:~:text=tolist()%2C%20used%20to%20convert,elements%20as%20a%20Python%20list.
    user_list=df['user'].unique().tolist()
#We now have to sort the list and remove the 'group_notification' message from the list
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Group Analysis')
#https://docs.streamlit.io/library/api-reference/widgets/st.selectbox
    selected_user=st.sidebar.selectbox("Analysis with respect to the user:",user_list)
#now importing functions from the helper file
    num_messages=helper.number_of_messages(selected_user,df)
    num_words=helper.number_of_words(selected_user,df)
    media=helper.media_shared(selected_user,df)
    url=helper.url_extract(selected_user,df)
    wordcloud=helper.wordcloud(selected_user,df)
    most_common_words_df=helper.most_common_words(selected_user,df)
    most_common_emojis=helper.most_used_emoji(selected_user,df)
    monthly_timeline=helper.monthly_timeline_of_chats(selected_user,df)
    daily_timeline=helper.daily_timeline_of_chats(selected_user,df)
    day_wise_messages=helper.day_wise_statistics(selected_user,df)
    month_wise_messages=helper.Month_wise_statistics(selected_user,df)
    message_timeline=helper.activity_heatmap(selected_user,df)
#showing the stats of the group
    if st.sidebar.button('Show Analysis'):
        st.title('Chat Statistics')
#https: // docs.streamlit.io / library / api - reference / layout / st.columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.title('Messages')
            st.header(num_messages)

        with col2:
            st.title('Words')
            st.header(num_words)

        with col3:
            st.title('Media')
            st.header(media)

        with col4:
            st.title('Links')
            st.header(url)

        st.title('Daily Timeline')
        plot = px.line(daily_timeline, x='date', y='message')
        plot.update_yaxes(tickfont=dict(size=12))
        plot.update_xaxes(tickfont=dict(size=12))
        plot.update_layout(xaxis=dict(showgrid=False),
                           yaxis=dict(showgrid=False))

        plot.update_layout(width=1100)
        st.plotly_chart(plot)

        st.title('Monthly Timeline')
        plot = px.line(monthly_timeline, x='Time', y='message')
        plot.update_yaxes(tickfont=dict(size=12))
        plot.update_xaxes(tickfont=dict(size=12))
        plot.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

        plot.update_layout(width=1100)

        st.plotly_chart(plot)


        # col1,col2,col3 = st.columns(3)
        col1, col2 = st.columns(2)

        with col1:
            st.title('Most Busy Day')
            plot = px.bar(day_wise_messages, x='Day', y='Number of messages', color='Number of messages',color_continuous_scale='Sunsetdark')
            plot.update_layout(width=500)
            st.plotly_chart(plot)

        with col2:
            st.title('Most Busy Month')
            plot = px.bar(month_wise_messages, x='Month', y='Number of messages', color='Number of messages',color_continuous_scale='Sunsetdark')
            plot.update_layout(width=600)
            st.plotly_chart(plot)


        st.title('Day X Time Activity Heatmap')
        plt.figure(figsize=(20, 8))
        sns.heatmap(message_timeline, annot=True)
        plt.yticks(rotation='horizontal')
        plt.xticks(rotation='vertical')
        st.pyplot(plt)


            # st.dataframe(day_wise_messages)

        # st.title('Most Busy Month')

        # col1, col2, col3 = st.columns(3)
        #
        # with col1:
        #     plot = px.bar(month_wise_messages, x='Month', y='Number of messages', color='Number of messages')
        #     st.plotly_chart(plot)
        #
        # with col3:
        #     st.dataframe(month_wise_messages)




        if selected_user=='Group Analysis':
            st.title('Most Active Users')


            col1, col2, col3 = st.columns(3)
            with col1:
                st.header('Graph')
                x = helper.most_active_users1(df)
                a = x.index
                b = x.values
                d = {'Users': a, 'Number of Messages': b}
                new_df = pd.DataFrame(d)
                plot = px.bar(new_df, x='Users', y='Number of Messages', color='Number of Messages',color_continuous_scale='Sunsetdark')
                st.plotly_chart(plot)

            with col3:
                st.header('Table')
                y = helper.most_active_users2(df)
                st.dataframe(y)

            # fig, ax = plt.subplots(1, 1)
            # for i in range(len(b)):
            #     plt.text(i, b[i], b[i], ha='center', va='bottom', fontsize='xx-small')
            # plt.xticks(rotation=90)
            # ax.bar(a, b, color='#33BEFF')
            # ax.set_xlabel('Users')
            # ax.set_ylabel('Number of Messages')
            # st.pyplot(fig)

                # if st.sidebar.button('Interactive Graph'):
                #     st.header('Interactive Graph')
                #     d = {'Users': a, 'Number of Messages': b}
                #     new_df = pd.DataFrame(d)
                #     plot = px.bar(new_df, x=new_df['Users'], y=new_df['Number of Messages'])
                #     st.plotly_chart(plot)
                #
                # else:
                #     st.header('Normal Graph')
                #     fig, ax = plt.subplots(1, 1)
                #     for i in range(len(b)):
                #         plt.text(i, b[i], b[i], ha='center', va='bottom', fontsize='xx-small')
                #     plt.xticks(rotation=90)
                #     ax.bar(a, b, color='#33BEFF')
                #     ax.set_xlabel('Users')
                #     ax.set_ylabel('Number of Messages')
                #     st.pyplot(fig)



        #Building the wordcloud
        st.header('WordCloud')
        image=wordcloud
        fig, ax = plt.subplots()
        ax.imshow(image)
        st.pyplot(fig)

        st.title('Most Common Chat Words')
        col1, col2,col3 = st.columns(3)


        with col1:
            plot=px.bar(most_common_words_df, y='Number of times appeared', x='Words', color='Number of times appeared',color_continuous_scale='Sunsetdark')
            st.plotly_chart(plot)
            # fig,ax=plt.subplots()
            # a=most_common_words_df[0]
            # b=most_common_words_df[1]
            # ax.bar(a,b)
            # st.pyplot(fig)

        with col3:
            # building a matplotib and plotly chart to show most used words
            st.dataframe(most_common_words_df)

        st.title('Most Common Emojis')
        col1, col2, col3 = st.columns(3)
        most_common_emojis = helper.most_used_emoji(selected_user, df)

        with col1:
            plot = px.pie(most_common_emojis, values='Number of times used', names='Emoji', color='Number of times used', title='Emojis')
            plot1=plot.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(plot)
            # fig,ax=plt.subplots()
            # a=most_common_words_df[0]
            # b=most_common_words_df[1]
            # ax.bar(a,b)
            # st.pyplot(fig)

        with col3:
            # building a matplotib and plotly chart to show most used words
            st.dataframe(most_common_emojis)








