from flask import Flask, jsonify
import json
import sqlite3
from flask import abort
from time import gmtime, strftime
from flask import request
from flask import make_response
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULER'] = False
@app.route("/api/v1/info")

def home_index():
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor = conn.execute("SELECT buildtime, version, methods, links from apirelease")
    for row in cursor:
        api = {}
        api['version'] = row[1]
        api['buildtime'] = row[0]
        api['methods'] = row[2]
        api['links'] = row[3]
        api_list.append(api)
    conn.close()
    return jsonify({'api_version': api_list}), 200

@app.route('/api/v1/users', methods=['GET'])
def get_users():
   return list_users()

def list_users():
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor = conn.execute("SELECT username, full_name,  emailid, password, id from users")
    for row in cursor:
        a_dict = {}
        a_dict['username'] = row[0]
        a_dict['fullname'] = row[1]
        a_dict['emailid'] = row[2]
        a_dict['password'] = row[3]
        a_dict['id'] = row[4]
        api_list.append(a_dict)

    conn.close()
    return jsonify({'user_list': api_list})


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return list_user(user_id)

def list_user(user_id):
    conn = sqlite3.connect('mydb.db')
    print ("Opened database Successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users where id=?",(user_id,))
    data = cursor.fetchall()
    if len(data) != 0:
       user = {}
       user['username'] = data[0][0]
       user['fullname'] = data[0][3]
       user['emailid'] = data[0][1]
       user['password'] = data[0][2]
       user['id'] = data[0][4]
    conn.close()
    return jsonify(user)

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'emailid' in request.json or not 'full_name' in request.json or not 'password' in request.json:
        abord(400)
    user = {
        'username': request.json['username'],
        'emailid': request.json['emailid'],
        'full_name': request.json.get('full_name',""),
        'password': request.json['password']
    }
    return jsonify({'status': add_user(user)}), 201

def add_user(new_user):
    conn = sqlite3.connect('mydb.db')
    print ("Opened database Successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users where username=? or emailid=?", (new_user['username'], new_user['emailid']))
    data = cursor.fetchall()
    if len (data) != 0:
       abort(409)
    else:
       cursor.execute("INSERT INTO users (username,emailid,password,full_name) values(?,?,?,?)", (new_user['username'],new_user['emailid'],new_user['password'],new_user['full_name']))
       conn.commit()
       return "Success"
    conn.close()
    return jsonify(a_dict)

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json:
       abort(400)
    user=request.json['username']
    return jsonify({'status': del_user(user)}), 200

def del_user(del_user):
    conn = sqlite3.connect('mydb.db')
    print ("Openend database successfully");
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users where username=?", (del_user,))
    data = cursor.fetchall()
    print ("Data", data)
    if len (data) == 0:
       abord(404)
    else:
       cursor.execute("DELETE FROm users WHERE username==?", (del_user,))
    conn.commit()
    return "Success"

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    if not request.json:
       abort(400)
    user['id'] = user_id
    key_list = request.json.keys()
    for i in key_list:
       user[i] = request.json[i]
    print (user)
    return jsonify({'status': upd_user(user)}), 200

def upd_user(user):
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=? ", (user['id'],))
    data = cursor.fetchall()
    if len (data) == 0:
       abort(404)
    else:
       key_list=user.keys()
       for i in key_list:
           if i != "id":
              print (user, i)
              # cursor.execute("UPDATE users set {0}=? where id=? ", (i, user[i], user['id'])
              cursor.execute("""UPDATE users SET {0} = ? WHERE id = ?""".format(i), (user[i], user['id']))
              conn.commit()
    return "Success"

@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()

def list_tweets():
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT username, body, tweet_time, id from tweets")
    data = cursor.fetchall()
    print (data)
    print (len(data))
    if len(data) == 0:
        return api_list
    else:
        for row in data:
            tweets = {}

            tweets['tweetedby'] = row[0]
            tweets['body'] = row[1]
            tweets['timestamp'] = row[2]
            tweets['id'] = row[3]

            print (tweets)
            api_list.append(tweets)

    conn.close()
    print (api_list)
    return jsonify({'tweets_list': api_list})

@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():
    user_tweet = {}
    if not request.json or not 'username' in request.json or not 'body' in request.json:
        abort(400)
    user_tweet['username'] = request.json['username']
    user_tweet['body'] = request.json['body']
    user_tweet['created_at']=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    print (user_tweet)
    return jsonify({'status': add_tweet(user_tweet)}), 200

def add_tweet(new_tweets):
    conn = sqlite3.connect('mydb.db')
    print ("Opened database Successfully");
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users where username=? ", (new_tweets['username'],))
    data = cursor.fetchall()
    if len (data) == 0:
       abort(404)
    else:
       cursor.execute("INSERT INTO tweets (username, body, tweet_time) values(?,?,?)",(new_tweets['username'],new_tweets['body'], new_tweets['created_at']))
    conn.commit()
    return "Success"

@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
    return list_tweet(id)

def list_tweet(user_id):
    print (user_id)
    conn = sqlite3.connect('mydb.db')
    print ("Opened database Successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM tweets where id=? ", (user_id,))
    data = cursor.fetchall()
    print (data)
    if len(data) == 0:
       abort(404)
    else:
       user={}
       user['id'] = data[0][0]
       user['username']= data[0][1]
       user['body'] = data[0][2]
       user['tweet_time']= data[0][3]
    conn.close()
    return jsonify(user) 

@app.errorhandler(400)
def invalid_request(error):
     return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error':'Resource not found!'}), 404)

@app.errorhandler(409)
def user_found(error):
    return make_response(jsonify({'error': 'Conflict! Record exist'}), 409)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)