from flask import *
import databases as db
import random,apis
from flask_restful import Api


def randomColor():
    hexchars = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    color = "#" + ("".join(random.choices(hexchars,k=6)))
    return color

app = Flask(__name__)

api = Api(app)

api.add_resource(apis.SentMessages,'/api/sents/<string:username>')
api.add_resource(apis.InboxMessages,'/api/inboxes/<string:username>')
api.add_resource(apis.SendMessage,'/api/send')
api.add_resource(apis.ReportBug,'/api/report')




app.secret_key = "SAMI@9644"

@app.before_request
def before():
    session.permanent = True

def loggedIn():
    return session.get("user-info")

@app.route("/mobileapp")
def mobileApp():
    return render_template("mobile.html")

@app.route("/")
def homePage():
    if loggedIn():
        return redirect(f"/profile/{session['user-info']['username']}")
    else:
        return render_template("home.html")



@app.route("/createacc")
def signUp():
    with open("static/text/countries.txt") as list:
        countries = list.read().split("\n")
    return render_template("signup.html",countries=countries)

@app.route("/register",methods=['POST'])
def regPage():
    fullname = request.form.get("full-name")
    username = request.form.get("user-name")
    birthdate = request.form.get("bd")
    gender = request.form.get("gender")
    countries = request.form.get("countries")
    password = request.form.get("password")
    confirm = request.form.get("confirm")
    try:
        if (password == confirm):
            db.createAccount(fullname,username,birthdate,gender,countries,password)
            return "<script>alert('Account created successfully!');window.location.href='/';</script>"
        else:
            flash("Password matching failed!")
            return render_template("signup.html",messages = get_flashed_messages)
    except db.sqlite3.IntegrityError:
        return "<script>alert('The username you used is chosen please choose another');window.location.href='/createacc';</script>"
    except Exception as e:
        return f"{e}"

@app.route("/signin",methods=["POST"])
def storeSession():
    try:
        username = request.form.get("user-name")
        password = request.form.get("password")
        userinfo = db.viewUserInfo(username)
        checkusername = userinfo[0][1]
        checkpassword = userinfo[0][5]
        if password == checkpassword:
            cookies = {
                "Full-name" : userinfo[0][0],
                "username" : userinfo[0][1],
                "birthdate" : userinfo[0][2],
                "gender" : userinfo[0][3],
                "country" : userinfo[0][4],
                "password" : userinfo[0][5]
            }
            session['user-info'] = cookies
            return redirect(f"/profile/{session['user-info']['username']}")
        else:
            return "<script>alert('Your password is in correct!Check your password and try again!');window.location.href='/';</script>"
    except:
        return "<script>alert('No account found assosciated with this username!');window.location.href='/createacc';</script>"

@app.route("/profile/<string:username>")
def profilePage(username):
    try:
        if username == session['user-info']['username']:
            return render_template("profile.html",username = username,userinfo = session['user-info'])
        else:
            userinfo = db.viewUserInfo(username)
            return render_template("user-profile.html",userinfo = userinfo[0])
    except KeyError:
        return "<script>alert('No saved sessions found!');window.location.href='/';</script>"
    
@app.route("/chat")
def chattingPage():
    if loggedIn():
        with db. pymysql.connect(host="sql.freedb.tech",user="freedb_sami9644",password="Hma8#vCBBUD&!Y8",database="freedb_messangerpro_db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username <> %s",(session['user-info']['username'],))
            users = cur.fetchall()
        return render_template("chatting.html",users = users,randcolor = randomColor(),username = session['user-info']['username'])
    else:
       return "<script>alert('No saved sessions found!');window.location.href='/';</script>"

@app.route("/chat/<string:username>")
def chatWith(username):
    if loggedIn():
        userinfo = db.viewUserInfo(username)
        currentsession = session['user-info']
        return render_template("messages.html",username=username,userinfo=userinfo,cookies=currentsession)
    else:
        return "<script>alert('No saved sessions found!');window.location.href='/';</script>"

@app.route("/accountinfo")
def accountInfo():
    if loggedIn():
        userinfo = db.viewUserInfo(session['user-info']['username'])
        password = userinfo[0][5]
        hashtags = ""
        for i in range(len(password)):
            hashtags+="*"
        return render_template("info.html",userinfo=userinfo[0],password=hashtags)
    else:
        return "<script>alert('No saved sessions found!');window.location.href='/';</script>" 

@app.route("/accountsettings")
def settings():
    if loggedIn():
        userinfo = db.viewUserInfo(session['user-info']['username'])
        with open("static/text/countries.txt") as file:
            countries = file.read().split("\n")
        return render_template("setting.html",userinfo=userinfo[0],countries=countries)
    else:
        return "<script>alert('No saved sessions found!');window.location.href='/';</script>"

@app.route("/changepassword")
def changepassword():
    if loggedIn():
        return render_template("password.html")
    else:
       return "<script>alert('No saved sessions found!');window.location.href='/';</script>"

#save the new password
@app.route("/savenewpass",methods=["POST"])
def saveNewPass():
    old = session['user-info']['password']
    pwdold = request.form.get("old")
    pwdnew = request.form.get("new")
    pwdrep = request.form.get("repeat")
    if (old == pwdold) and (pwdnew == pwdrep):
        with db.pymysql.connect(host="sql.freedb.tech",user="freedb_sami9644",password="Hma8#vCBBUD&!Y8",database="freedb_messangerpro_db") as conn:
            cur = conn.cursor()
            cur.execute("UPDATE users SET password = %s",(pwdnew,))
            userinfo = db.viewUserInfo(session['user-info']['username'])
        cookies = {
                "Full-name": userinfo[0][0],
                "username": userinfo[0][1],
                "birthdate": userinfo[0][2],
                "gender": userinfo[0][3],
                "country": userinfo[0][4],
    
                "password": pwdnew
                }
        session['user-info'] = cookies
        return "<script>alert('Password changed successfully!');window.location.href='/';</script>"
    else:
        return "Something went wrong!"

@app.route("/report")
def reportBugs():
    if loggedIn():
        return render_template("report.html",username=session['user-info']['username'])
    else:
        return "<script>alert('No saved sessions found!');window.location.href='/';</script>"

@app.route("/savechanges",methods=["POST"])
def saveChanges():
    fullname = request.form.get("full-name")
    bd = request.form.get("birth-date")
    gender = request.form.get("gender")
    country = request.form.get("country")
    userinfo = db.viewUserInfo(session['user-info']['username'])
    with db. pymysql.connect(host="sql.freedb.tech",user="freedb_sami9644",password="Hma8#vCBBUD&!Y8",database="freedb_messangerpro_db") as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET fullname = %s, birthdate = %s, gender = %s, country = %s WHERE username = %s",
                    (fullname, bd, gender, country, session['user-info']['username']))
    cookies = {
        "Full-name": fullname,
        "username": userinfo[0][1],
        "birthdate": bd,
        "gender": gender,
        "country": country,
        "password": userinfo[0][5]
    }
    session['user-info'] = cookies
    return "<script>alert('Changes saved successfully!');window.location.href='/';</script>"

@app.route("/changedp")
def changeDp():
    return render_template("dp.html")

@app.route("/uploadnewdp",methods=['POST'])
def saveDp():
    avatar = request.files["profilepic"]
    username = session['user-info']['username']
    if (request.content_length <= (4 * 1024 * 1024)):
        avatar.save(f"static/avatars/{username}.png")
        avatarpath = f"static/avatars/{username}.png"
        return "<script>alert('Profile picture updated successfully!');window.location.href='/';</script>"
    else:
        return "<script>alert('Profile picture size must be 4MB or less!');window.location.href='/changedp';</script>"

@app.route("/logout")
def logOut():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run()
