from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase database
cred = credentials.Certificate('.backendw2023-firebase-adminsdk-vjhgp-0f8c1203ba.json')
firebaseapp = firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return {'message': 'Hello, World!'}

# @app.route("/sharereminders", methods=["POST"])
# def getreminders2():
#     data = request.get_json()
#     user_ref = db.collection(u'users').document(data["email"])
#     reminder_userID = user_ref.get().to_dict()["user_id"]
#     ### Get the user's email from handshake service ###
#     payload = {"r_user_id": reminder_userID}
#     r = requests.get("http://localhost:8002", json=payload)
# 
# 
#     ### Get the user's reminders from the database ###
#     reminders_ref = user_ref.collection(u'reminders')
#     reminders = []
#     for reminder in reminders_ref.stream():
#         reminders.append(reminder.to_dict())
#     return jsonify(reminders), 200

@app.route("/handshake", methods=["POST"])
def handshake():
    data = request.get_json()
    print(data)
    r = requests.post("http://localhost:8000/login", json=data)
    message = r.json()
    if r.status_code == 200:
        r_user_id_ref = db.collection(u'users').document(data["email"]).get()
        r_user_id = r_user_id_ref.to_dict()["user_id"]
        c_user_id = data['c_user_id']
        handshake_db = db.collection(u'handshake.db')
        handshake_db.add({"r_user_id": r_user_id, "c_user_id": c_user_id})
        return message, 201
    else:
        return message, 404


@app.route("/getreminders", methods=["GET"])
def getreminders():
    ### Convert the contacts user ID into internal user ID ###
    data = request.get_json()
    handshake_db = db.collection(u'handshake.db')
    c_user_id = data["c_user_id"]
    r_user_id_query = handshake_db.where(u'c_user_id', u'==', c_user_id).get()
    if not r_user_id_query:
        return jsonify({"message": "User not found, try syncing via handshake"}), 404
    r_user_id = r_user_id_query[0].to_dict()["r_user_id"]
    users_ref = db.collection(u'users')
    query_ref = users_ref.where(u'user_id', u'==', r_user_id)
    user = query_ref.get()
    if not user:
        return jsonify({"message": "User not found, try syncing via handshake"}), 404
    
    ### Get the user's reminders from the database ###
    user_reminders_ref = user[0].reference.collection(u'reminders')
    if not user_reminders_ref:
        return jsonify({[]}), 200
    reminders = []
    for reminder in user_reminders_ref.stream():
        r = reminder.to_dict()
        reminders.append(r)
    return jsonify(reminders), 200

if __name__ == '__main__':
    app.run(host="localhost", port=8001, debug=True)