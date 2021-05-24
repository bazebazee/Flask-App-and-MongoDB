from flask import Flask, render_template, request, redirect,session,jsonify
from functools import wraps
from pymongo import MongoClient
import json
from bson import json_util
from bson.objectid import ObjectId
from forms import User, SearchForm, Form
import pandas as pd


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.user_db
collection = db.user_data

def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap


@app.route('/', methods=['GET', 'POST'])
def home():
  return render_template('home.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
          print(request.form)
          
          return User().signup(request)
  #return (request.form['name'])

@app.route('/signout')
def signout():
  return User().signout()

@app.route('/home', methods=['GET','POST'])
def login():
        if request.method == 'POST':
          print(request.form)
          
          return User().login(request)
        return render_template('index1.html')


@app.route('/new_data', methods=['POST'])
def new_data(add):
    _json = request.json
    _name = _json['name']
    _surname = _json['surname']
    _street = _json['street']  
    _city = _json['city']
    _country = _json['country']
    
    if _name and _surname and _street and _city and _country == ['POST']:
                
        add = db.user_data.insert({'name':_name,'surname':_surname,'street':_street,'city':_city, 'country':_country})
        resp = jsonify("Data added successfully")
        
        resp.status_code = 200
        
    else:
            return not_found()
        
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message':'Not Found'
        
        }
    resp = jsonify(message)
    
    resp.status_code = 200
    
    return resp

@app.route('/index1')
def index():
  search= SearchForm(request.form)
  if request.method=='POST':
    return index2(search)
  return render_template('index1.html', form=search)



@app.route('/results', methods=['GET', 'POST'])
def index2():
  columns = request.args.get('search')  
  language = request.args.get('select')
  
  table_data1 = get_english_data_set()
  table_data2 = get_italian_data_set()

  if  language['select'] == 'English' :
    get_english_data_set(columns)
    
  elif language['select'] == 'Italian' :
    get_italian_data_set(columns)
    if language is None:
        return not_found()
    #return render_template('results.html',form= search, table=table)

    tables = pd.read_html('results.html')

    table_df = pd.DataFrame('table_data1')
    table_data1 = pd.Dataframe(tables[0], columns = ['Name','Surname','Street', 'City','Country'])
    
    table1_df = pd.DataFrame('table_data2')
    table_data2 = pd.Dataframe(tables[0], columns = ['Nome','Cognome','Strada', 'Citta','Paese'])
 
    columns_list = columns.split(" ")


def get_english_data_set(columns):

        
  for items in columns.order_by('Name'):
      name = request.args.get('Name')
      surname = request.args.get('Surname')
      street = request.args.get('Street')
      city = request.args.get('City')
      country = request.args.get('Country')
      if items is None:
          return not_found()
          
    
      #return render_template('results.html', form=search)

def get_italian_data_set(columns): 
    
   for items in data_set2.order_by('Name'): 
       name = request.args.get('Nome')
       surname = request.args.get('Cognome')
       street = request.args.get('Strada')
       city = request.args.get('Citta')
       country = request.args.get('Paese')
       if items is None:
          return not_found()
       #return render_template('results.html', form=search)
      


if __name__ == "__main__":
    app.run(debug=True)