def preprocess(data):
        import re
        import pandas as pd
        regex_string = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
        messages=re.split(regex_string,data)[1:]
        dates = re.findall(regex_string,data)
        d = {'user_messages': messages, 'dates': dates}
        df = pd.DataFrame(data=d)
        df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%y, %H:%M - ')
        df['year'] = df['dates'].dt.year
        df['month'] = df['dates'].dt.month_name()
        df['month_num'] = df['dates'].dt.month
        df['day'] = df['dates'].dt.day
        df['hour'] = df['dates'].dt.hour
        df['minute'] = df['dates'].dt.minute
        df['Day name'] = df['dates'].dt.day_name()
        period = []
        for i in df['hour']:
            if i == 23:
                period.append(str(i) + '-' + str('00'))
            elif i == 0:
                period.append(str(i) + "-" + str('1'))
            else:
                period.append(str(i) + "-" + str(i + 1))
        df['Period'] = period

        # df.drop(columns=['dates'], inplace=True)
        users = []
        messages = []

        for items in df['user_messages']:
            entry = re.split('([\w\W]+?):\s', items)
            if entry[1:]:
                new_entry = ' '.join(entry[2:])
                users.append(entry[1])
                messages.append(new_entry)
            else:
                users.append('group_notification')
                messages.append(entry[0])

        df['user'] = users
        df['message'] = messages
        df.drop(columns=['user_messages'], inplace=True)
        return df