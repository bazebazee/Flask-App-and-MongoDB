from flask import Flask, jsonify, request, session, redirect
from wtforms import Form, StringField, SelectField
from passlib.hash import pbkdf2_sha256
import uuid
import pymongo
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.user_db
collection = db.user_data

class User:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  def signup(self, request):
    print(request.form)
    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password')
    }

    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    if db.user_data.find_one({ "email": user['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400

    if db.user_data.insert_one(user):
      return self.start_session(user)

    return jsonify({ "error": "Signup failed" }), 400

  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self, request):
    print(request.form)

    user = db.user_data.find_one({
      "email": request.form.get('email')
    })

    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
      return self.start_session(user)
    
    return jsonify({ "error": "Invalid login credentials" }), 401



class Form(Form):
    choices = [('English', 'English'),
               ('Italian', 'Italian'),]
    select = SelectField('Choose Language:', choices=choices)
    search = StringField('Insert Columns:')

class SearchForm(Form):

    name = StringField('Name')
    surname = StringField('Surname')
    street = StringField('Street')
    city = StringField('City')
    country = StringField('Country')
  