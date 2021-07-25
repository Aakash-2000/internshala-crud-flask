import re
from bson.objectid import ObjectId
from flask import Flask,request,render_template,session,redirect,url_for
from flask import jsonify
from flask.signals import request_started
from flask_pymongo import PyMongo
from flask_session import Session
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config["MONGO_URI"] = "mongodb+srv://user_1:Aakash4224@cluster0.fjw1u.mongodb.net/db?retryWrites=true&w=majority"
mongoDB = PyMongo(app)
@app.route('/',methods=["GET"])
def index():
    
    if not session.get('uid'):
        return render_template('Signup.html')
    else:
        data = []
            
        x = mongoDB.db[str(session['uid'])].find({})
        for j in x:
            data.append(j)
        print(data)
        return render_template('Home.html',data = data)
@app.route('/view/<id>',methods=['GET'])
def view(id):
    
    x = mongoDB.db[str(session['uid'])].find({'_id':ObjectId(id)})
    for i in x:
        data = i
    return render_template('View.html',data = data,id=id)
@app.route('/editCard',methods=["POST"])
def editCard():
    print(request.get_json())
    x = mongoDB.db[str(session['uid'])].find_one({'_id':ObjectId(request.get_json()['item'][2])})
    
    d = x['data']
    Updatedlist = []

    for j in d:
        print('j',j)
        if(j['item'] ==request.get_json()['item'][0] and j['qty'] ==request.get_json()['item'][1]):
            k = {'item':request.get_json()['new'][0],'qty':request.get_json()['new'][1]}
            Updatedlist.append(k)
        else:
            Updatedlist.append(j)
    print(Updatedlist)
    query = { '_id':ObjectId(request.get_json()['item'][2]) }
    newdata = { "$set": { "data": Updatedlist } }
    mongoDB.db[str(session['uid'])].update_one(query,newdata)
    
    url = "/view/"+str(request.get_json()['item'][2])
    return redirect(url)
    

    
    
    
    
    
    return 'Hello'
@app.route('/create',methods=['GET'])
def create():
    return render_template('Create.html')
@app.route('/createcart',methods=['GET','POST'])
def createcart():
    
    mongoDB.db[str(session['uid'])].insert_one(request.get_json())
    return redirect(url_for('index'))
    
@app.route('/login',methods=["POST",'GET'])
def login():
    if request.method == 'GET':
        return render_template('Login.html')
    else:

        try:
            result = mongoDB.db.users.find({'name':request.form['uname'],'password':request.form['pwd']})
            print(result)
            for i in result:
            
                session['uid']  = i['_id']
                return redirect(url_for('index'))
            else:
                return {'error':'No such user found'}
        except:
            return { 'error' : 'Error Occured'}
@app.route('/delCard',methods=["POST"])
def delCard():
    
    mongoDB.db[str(session['uid'])].delete_one({"_id":ObjectId(request.get_json()['id'])})
    
    return redirect(url_for('index'))
    
@app.route('/Signup',methods=["POST","GET"])
def Signup():
    if request.method == 'GET':
        return render_template('Signup.html')
    else:
        try:
            result = mongoDB.db.users.insert_one({'name':request.form['uname'],'password':request.form['pwd'],'email':request.form['gmail']})
            session['uid'] = result.inserted_id
            
            return redirect(url_for('index'))
        except:
            return { 'error' : 'Error Occured'}
if __name__ == '__main__':
    app.run(debug=True)
