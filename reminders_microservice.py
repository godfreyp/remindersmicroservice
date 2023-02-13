from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import argon2

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase database
cred = credentials.Certificate('.backendw2023-firebase-adminsdk-vjhgp-0f8c1203ba.json')
firebaseapp = firebase_admin.initialize_app(cred)
db = firestore.client()

# Initiliaze argon2 password hasher
hasher = argon2.PasswordHasher()

def hash_password(password):
    return hasher.hash(password)

def verify_password(hashed_password, password):
    try:
        return hasher.verify(hashed_password, password)
    except argon2.exceptions.VerifyMismatchError:
        return False

@app.route("/handshake", methods=["POST"])
def handshake():
    # Get the JSON data from the request
    data = request.get_json()
    
    # Check if the email exists
    collection = db.collection('users')
    doc_ref = collection.document(data['email'])
    doc = doc_ref.get()
    if doc.exists:
        db_dict = doc.to_dict()
        if verify_password(db_dict['password'], data['password']):
            response = jsonify({
                "message": "Login Successful",
            })
            response.status_code = 200
        else:
            response = jsonify({
                "message": "Wrong password",
            })
            response.status_code = 401
    else:
        response = jsonify({
            "message": "Email does not exist",
        })
        response.status_code = 401

    # If login is successful, proceed with handshake
    if response.status_code == 200:
        r_user_id_ref = db.collection(u'users').document(data["email"]).get()
        r_user_id = r_user_id_ref.to_dict()["user_id"]
        c_user_id = data['c_user_id']
        if not db.collection(u'handshake.db').where(u'r_user_id', u'==', r_user_id).where(u'c_user_id', u'==', c_user_id).get():
            handshake_db = db.collection(u'handshake.db')
            handshake_db.add({"r_user_id": r_user_id, "c_user_id": c_user_id})
            response.status = 201
        return response
    else:
        return response


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
        
        # Convert the "deadline" to two seperate fields, "date" and "time"
        date_time = r["deadline"].split(" ")
        r["date"], r["time"] = date_time[0], date_time[1]

        # Remove unecessary fields
        del r["deadline"]
        del r["email"]
        del r["description"]

        # Add the reminder to the list
        reminders.append(r)
    return jsonify(reminders), 200

if __name__ == '__main__':
    app.run(host="localhost", port=8001, debug=True)