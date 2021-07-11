#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import sqlite3


reqs = pd.read_csv(r'requests.csv', header = None)
reqsF = pd.DataFrame(reqs, columns = [0,1,2,3,4,5])
impressions = pd.read_csv(r'impressions.csv', header = None)
impressionsF = pd.DataFrame(impressions, columns = [0,1,2])
clicks = pd.read_csv(r'clicks.csv', header = None)
clicksF = pd.DataFrame(clicks, columns = [0,1,2])

connection = sqlite3.connect("DataEnginTable.db")

cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS requests')
cursor.execute('DROP TABLE IF EXISTS impressions')
cursor.execute('DROP TABLE IF EXISTS clicks')

cursor.execute('CREATE TABLE requests (timestamp TIMESTAMP, session_id varchar(50), partner varchar(50), user_id varchar(50), bid float, win BOOLEAN)')

for row in reqsF.itertuples():
    cursor.execute('''
                INSERT INTO requests ( timestamp, session_id, partner, user_id, bid, win)
                VALUES ( ?,?,?,?,?,?)
                ''',
                [row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6]]   
               )


cursor.execute('CREATE TABLE impressions (timestamp TIMESTAMP, session_id varchar(50), Duration INTEGER)')

for row in impressionsF.itertuples():
    cursor.execute('''
                INSERT INTO impressions ( timestamp, session_id, Duration)
                VALUES ( ?,?,?)
               ''',
               [row[1],
               row[2],
               row[3]]
                )
                
                
cursor.execute('CREATE TABLE clicks (timestamp TIMESTAMP, session_id varchar(50), Time INTEGER)')
                
for row in clicksF.itertuples():
    cursor.execute('''
                INSERT INTO clicks ( timestamp, session_id, Time)
                VALUES ( ?,?,?)
               ''',
               [row[1],
               row[2],
               row[3]]  
             )

cursor.execute('CREATE INDEX index1 ON requests(user_id)')
cursor.execute('CREATE INDEX index2 ON requests(session_id)')
cursor.execute('CREATE INDEX index3 ON impressions(session_id)')
cursor.execute('CREATE INDEX index4 ON clicks(session_id)')

    
    
connection.commit()


def userStats():
    print("Enter user_id:")
    user = input()
    for row in connection.execute('select count(*) from requests WHERE user_id = ?', [user]):
        print(row[0])
    for row in connection.execute('select count(*) from requests WHERE user_id = ? AND win = TRUE', [user]):
        print(row[0])
    for row in connection.execute('select count(*) from requests, clicks WHERE user_id = ? AND requests.session_id = clicks.session_id', [user]):
        print(row[0])
    for row in connection.execute('select AVG(bid) from requests WHERE user_id = ? AND win = TRUE', [user]):
        print(row[0])
    for row in connection.execute('SELECT AVG(Duration) FROM (SELECT Duration FROM requests, impressions WHERE user_id = ? AND requests.session_id = impressions.session_id ORDER BY Duration LIMIT 2 - (SELECT COUNT(*) FROM requests, impressions WHERE user_id = ? AND requests.session_id = impressions.session_id) % 2  OFFSET (SELECT (COUNT(*) - 1) / 2 FROM requests, impressions WHERE user_id = ? AND requests.session_id = impressions.session_id))', [user, user, user]):
        print(row[0])
    for row in connection.execute('select MAX(Time) from requests, clicks WHERE user_id = ? AND requests.session_id = clicks.session_id', [user]):
        print(row[0])


def sessionStats():
    print("Enter session_id:")
    session= input()
    for row in connection.execute('select timestamp from requests WHERE session_id = ?', [session]):
        print(row[0])
    for row in connection.execute('select MAX(timestamp) from requests WHERE session_id = ?', [session]):
        max_time = row[0]
    for row in connection.execute('select count(*), MAX(timestamp) from impressions WHERE session_id = ?', [session]):
        if row[0] > 0:
            max_time = max(max_time, row[1])
    for row in connection.execute('select count(*), MAX(timestamp) from clicks WHERE session_id = ?', [session]):
        if row[0] > 0:
            max_time = max(max_time, row[1])
    print(max_time)
    for row in connection.execute('select DISTINCT partner from requests WHERE session_id = ?', [session]):
        print(row[0])
        
        
while 1:
    print("Enter Command: ")
    command = input()
    if command == 'keepalive':
        print('Service is up and ready for query.')
    elif command == 'userStats':
        userStats()
    elif command == 'sessionId':
        sessionStats()
    elif command == 'Kill':
        print('Service shut down.')
        break
    else:
        print('Unkown command!')

    


# In[ ]:




