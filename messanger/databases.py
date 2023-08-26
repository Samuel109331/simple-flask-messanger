import pymysql 
from datetime import datetime

def createUsers():
    with pymysql.connect(host="sql.freedb.tech",user="freedb_sami9644",password="Hma8#vCBBUD&!Y8",database="freedb_messangerpro_db") as conn:
        cur = conn.cursor()
        # cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("CREATE TABLE users(\
                    fullname VARCHAR(255),\
                    username VARCHAR(255) PRIMARY KEY,\
                    birthdate DATE,\
                    gender VARCHAR(255),\
                    country VARCHAR(255),\
                    password VARCHAR(255),\
                    session VARCHAR(255),\
                    createdon DATE)")


def messages():
    with pymysql.connect(host="sql.freedb.tech",user="freedb_sami9644",password="Hma8#vCBBUD&!Y8",database="freedb_messangerpro_db") as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE messages(\
                    message VARCHAR(255),\
                    senton VARCHAR(255),\
                    sentby VARCHAR(255),\
                    sentto VARCHAR(255))")


        
def sendMessages(sender,reciever,message):
    with pymysql.connect(host="sql.freedb.tech",user="freedb_sami9644",password="Hma8#vCBBUD&!Y8",database="freedb_messangerpro_db") as conn:
        cur = conn.cursor()
        senton = f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}"
        cur.execute("INSERT INTO messages(message,senton,sentby,sentto) VALUES (%s,%s,%s,%s)",
                     (message,senton,sender,reciever,))
        conn.commit()

def inboxMessages(username):
    with pymysql.connect(host="sql.freedb.tech",user="freedb_sami9644",password="Hma8#vCBBUD&!Y8",database="freedb_messangerpro_db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT message FROM messages WHERE sentto = %s ORDER BY senton",(username,))
        messages = cur.fetchall()
    if len(messages) == 0:
        return messages
    else:
        return [i[0] for i in messages]

def sentMessages(username):
    with pymysql.connect(host="sql.freedb.tech",user="freedb_sami9644",password="Hma8#vCBBUD&!Y8",database="freedb_messangerpro_db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT message FROM messages WHERE sentby = %s",(username,))
        messages = cur.fetchall()
    if len(messages) == 0:
        return messages
    else:
        return [i[0] for i in messages]



def reviews():
    with pymysql.connect(host="sql.freedb.tech",user="freedb_sami9644",password="Hma8#vCBBUD&!Y8",database="freedb_messangerpro_db") as conn:
        cur = conn.cursor()
        # cur.execute("DROP TABLE IF EXISTS reviews")
        cur.execute("CREATE TABLE reviews(\
                    review VARCHAR(255),\
                    reviewedby VARCHAR(255),\
                    stars INT)")


def createAccount(fullname,username,birthdate,gender,country,password):
    with pymysql.connect(host="sql.freedb.tech",user="freedb_sami9644",password="Hma8#vCBBUD&!Y8",database="freedb_messangerpro_db") as conn:
        cur = conn.cursor()
        time = datetime.now()
        time1 = str(time).split(" ")[0]
        time2 =str(time).split(" ")[1].split(".")[0]
        ultimatetime = time1+" "+time2
        cur.execute("INSERT INTO users(fullname,username,birthdate,gender,country,password,session,createdon)\
                    VALUES(%s,%s,%s,%s,%s,%s,false,%s)",(fullname,username,birthdate,gender,country,password,ultimatetime))
        conn.commit()

def viewUserInfo(username):
    with pymysql.connect(host="sql.freedb.tech",user="freedb_sami9644",password="Hma8#vCBBUD&!Y8",database="freedb_messangerpro_db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s",(username,))
        return cur.fetchall()
    
