# remindersmicroservice

## Intro

This is a microservice designed for Group 23 of Oregon State University's CS361 - 400 class as of W2023.

## Dependencies

Because the app is currently hosted locally, you will need the following.

Download reminders_microservice.py and install:

> firebase-admin

> flask

> argon2-cffi

Additionally, you will also need an firebase_admin SDK JSON from https://console.firebase.google.com/u/0/project/backendw2023/

This microservice runs independently from the reminders app backend.

## Communications Contract

The microservice utilizes communicates using JSON through APIs.

The host is set to http://localhost/8001 and there are two paths available.

### 1. /handshake

**METHOD: POST**

**JSON BODY**

{
  "email": STRING,
  "password": STRING,
  "c_user_id": INT
}

**RESPONSE**

It returns a JSON containg the parameter message:

{
  "message": STRING
}

This message, along with its accompanying status code, will inform you whether your handshake was successful or not.


### 2. /getreminders

**METHOD: GET**

**JSON BODY**

{
  "c_user_id": INT
}

**SUCCESSFUL RESPONSE**

Otherwise, a JSON containing a list of reminders is returned with a status code of 200

{
  [
    object1,
    object2,
    object3...
  ]
}

**FAILED RESPONSE**

If the user has no performed a handshake or there is an error, then a JSON with one parameter is returned along with a non-200 status code.

{
  "message": STRING
}
