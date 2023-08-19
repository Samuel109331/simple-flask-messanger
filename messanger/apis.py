from flask_restful import Resource
from flask import request,session
import databases as db

class SendMessage(Resource):
    def post(self):
        data = request.get_json()
        sender = data['sender']
        reciever = data['reciever']
        message = data['message']
        db.sendMessages(sender,reciever,message)
        return {"status" : True,'sent' : message}

class SentMessages(Resource):
    def get(self,username):
        messages = db.sentMessages(username)
        return {"messages" : messages}

class InboxMessages(Resource):
    def get(self,username):
        messages = db.inboxMessages(username)
        return {"messages" : messages}

class ReportBug(Resource):
    def post(self):
        data = request.get_json()
        print(data)  # Add this line to check the received JSON data
        review = data['review']
        username = data['username']
        stars = data['stars']
        with db.pymysql.connect(host="sql.freedb.tech",user="freedb_sami9644",password="Hma8#vCBBUD&!Y8",database="freedb_messangerpro_db") as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO reviews(review,reviewedby,stars) VALUES (%s,%s,%s) ",(review,username,stars))
            conn.commit()
        return {"message" : "review sent successfully!"}
