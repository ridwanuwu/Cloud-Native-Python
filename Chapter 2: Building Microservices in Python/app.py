from flask import Flask
from flask import jsonify
from flask import request
import datetime
import json
import sqlite3

app = Flask(__name__)

def upd_user(user):
 conn = sqlite3.connect('mydb.db')
 print ("Opened database successfully");
 cursor=conn.cursor()
 cursor.execute("SELECT * from users where id=? ", (user['id'],))
 data = cursor.fetchall()
 print (data)
 if len(data) == 0:
  return "Failed"
 else:
  key_list=user.keys()
  for i in key_list:
   if i != "id":
    print (user, i)
    # cursor.execute("UPDATE users set {0}=? where id=? ", (i, user[i], user['id']))
    cursor.execute("""UPDATE users SET {0} = ? WHERE id = ?""".format(i), (user[i], user['id']))
    conn.commit()
    return  "Success"

def list_users():
 conn = sqlite3.connect('mydb.db')
 print ("Opened database successfully");
 api_list=[]
 cursor = conn.execute("SELECT username, full_name, emailid, password, id from users")
 for row in cursor:
  a_dict = {}
  a_dict['username'] = row[0]
  a_dict['name'] = row[1]
  a_dict['email'] = row[2]
  a_dict['password'] = row[3]
  a_dict['id'] = row[4]
  api_list.append(a_dict)
 conn.close()
 return jsonify({'user_list': api_list})

def list_user(user_id):
 conn = sqlite3.connect('mydb.db')
 print ("Opened database successfully");
 api_list=[]
 cursor=conn.cursor()
 cursor.execute("SELECT * from users where id=?", (user_id,))
 data = cursor.fetchall()
 if len(data) == 1:
  user = {}
  user['username'] = data[0][0]
  user['email'] = data[0][1]
  user['password'] = data[0][2]
  user['name'] = data[0][3]
  user['id'] = data[0][4]
 else:
  user = {}
  user['error'] = "Resource not found!"
 conn.close()
 return jsonify(user)

def add_user(new_user):
 conn = sqlite3.connect('mydb.db')
 print ("Opened database successfully");
 api_list=[]
 cursor=conn.cursor()
 cursor.execute("SELECT * from users where username=? or emailid=?",(new_user['username'],new_user['email']))
 data = cursor.fetchall()
 if len(data) != 0:
  return "Failed"
 else:
  cursor.execute("insert into users (username, emailid, password, full_name) values(?,?,?,?)",(new_user['username'], new_user['email'], new_user['password'], new_user['name']))
  conn.commit()
  return "Success"
 conn.close()
 return jsonify(a_dict)

def del_user(del_user):
 conn = sqlite3.connect('mydb.db')
 print ("Opened database successfully");
 cursor=conn.cursor()
 cursor.execute("SELECT * from users where username=?",(del_user,))
 data = cursor.fetchall()
 print ("Data",data)
 if len(data) == 0:
  return "Failed"
 else:
  cursor.execute("delete from users where username=?",(del_user,))
  conn.commit()
  return "Success"

def list_tweets():
 conn = sqlite3.connect('mydb.db')
 print ("Opened database successfully");
 api_list=[]
 cursor = conn.execute("SELECT username, body, tweet_time, id from tweets")
 data = cursor.fetchall()
 if len(data) != 0:
  for row in data:
   tweets = {}
   tweets['Tweet By'] = row[0]
   tweets['Body'] = row[1]
   tweets['Timestamp'] = row[2]
   tweets['id'] = row[3]
   api_list.append(tweets)
  conn.close()
  return jsonify({'tweets_list': api_list})
 else:
  return api_list

def add_tweet(new_tweets):
 conn = sqlite3.connect('mydb.db')
 print ("Opened database successfully");
 cursor=conn.cursor()
 cursor.execute("SELECT * from users where username=? ", (new_tweets['username'],))
 data = cursor.fetchall()
 if len(data) == 0:
  return "Failed"
 else:
  cursor.execute("INSERT into tweets (username, body, tweet_time) values (?,?,?)",(new_tweets['username'],new_tweets['body'],new_tweets['created_at']))
  conn.commit()
  return "Success"

def list_tweet(user_id):
 print (user_id)
 conn = sqlite3.connect('mydb.db')
 print ("Opened database successfully");
 api_list=[]
 cursor=conn.cursor()
 cursor.execute("SELECT * from tweets where id=?",(user_id,))
 data = cursor.fetchall()
 print (data)
 if len(data) == 0:
  return jsonify({'status':"404 Not Found"})
 else:
  user = {}
  user['id'] = data[0][0]
  user['username'] = data[0][1]
  user['body'] = data[0][2]
  user['tweet_time'] = data[0][3]
 conn.close()
 return jsonify({"data":user})

@app.route("/api/v1/info")
def home_index():
 conn = sqlite3.connect('mydb.db')
 print ("Opened database successfully");
 api_list=[]
 cursor = conn.execute("SELECT buildtime, version, methods, links from apirelease")
 for row in cursor:
  a_dict = {}
  a_dict['version'] = row[1]
  a_dict['buildtime'] = row[0]
  a_dict['methods'] = row[2]
  a_dict['links'] = row[3]
  api_list.append(a_dict)
 conn.close()
 return jsonify({'version_list': api_list}), 200

@app.route("/api/v1/users", methods=['GET'])
def get_users():
 return list_users()

@app.route("/api/v1/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
 return list_user(user_id)

@app.route('/api/v1/users', methods=['POST'])
def create_user():
 if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
  return jsonify({'status': "Failed"})
 else:
  user = {
   'username': request.json['username'],
   'email': request.json['email'],
   'name': request.json.get('name',""),
   'password': request.json['password']
  }
  return jsonify({'status': add_user(user)}), 201

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
 if not request.json or not 'username' in request.json:
  return jsonify({'status': "Failed"})
 else:
  user=request.json['username']
  return jsonify({'status': del_user(user)}), 200

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
 user = {}
 if not request.json:
  return jsonify({'status': "Failed"})
 user['id']=user_id
 key_list = request.json.keys()
 for i in key_list:
  user[i] = request.json[i]
 print (user)
 return jsonify({'status': upd_user(user)}), 200

@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
 return list_tweets()

@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():
 user_tweet = {}
 if not request.json or not 'username' in request.json or not 'body' in request.json:
  return jsonify({'status': "Failed"})
 d=datetime.datetime.now()
 user_tweet['username'] = request.json['username']
 user_tweet['body'] = request.json['body']
 user_tweet['created_at']=d.strftime("%Y-%m-%d %H:%M:%S")
 print (user_tweet)
 return jsonify({'status': add_tweet(user_tweet)}), 200

@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
 return list_tweet(id)

if __name__ == "__main__":
 app.run(host='0.0.0.0', port=5000, debug=True)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False