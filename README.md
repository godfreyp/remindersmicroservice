# remindersmicroservice

Initialize venv and install both firebase-admin and flask. This will also require an firebase_admin SDK JSON from https://console.firebase.google.com/u/0/project/backendw2023/firestore/data/~2Fusers~2Ftest@gmail.com

This microservice runs independently from the reminders app backend.

The two supported paths are:

1. /handshake

Handshake takes a JSON with three paramters
{
  "email": STRING,
  "password": STRING,
  "c_user_id": INT
}

Returns a JSON containg the parameter message:

{
  "message": STRING
}


2. /getreminders

This takes a JSON with one reminder.

{
  "c_user_id": INT
}

If the user has no performed a handshake or there is an error, then a JSON with one parameter is returned

{
  "message": STRING
}

Otherwise, a JSON containing a list of reminders is returned
{
  [
    object1,
    object2,
    object3...
  ]
}
