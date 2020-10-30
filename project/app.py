from flask import Flask, render_template, request, redirect, url_for, flash, session, logging
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import json, xmljson

import requests

 
# initialise db



app = Flask(__name__)
CORS(app) ## To allow direct AJAX calls

# db configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'health_rocky'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)



# home page route and view, containing a dictionary thats rendered in the updates section
@app.route('/')
def Index():

    category = [
             {
                'id':1,
                'title': 'Covid-19 Updates',
                'description': "A centralised hub of all the latest covid-19 updates and statics from around the world and a selected few african states"
             
            
            },

              {
                'id':2,
                'title': 'World Health News',
                'description': "All the latest world health news aggregated in one central hub for you to freely access and stay informed on whats happening in the health world"
            },

              {
                'id':3,
                'title': 'Nigeria Health News',
                'description': "Catch up to speed with the latest nigerian health news, collected from trusted publishers in nigeria, bringimg you both local and international ."
            },

            {
                'id':4,
                'title': 'South Africa Health News',
                'description': "Catch up to speed with the latest South Africa health news, collected from trusted publishers in nigeria, bringimg you both local and international"
            }


    ]

    return render_template('home.html', news_categories=category)


# api call to news api for world nes, its only a get request 
@app.route('/worldhealthnews', methods=['GET'])
def world_health_news():
    r = requests.get('http://newsapi.org/v2/top-headlines?country=us&category=health&apiKey=db0dbc6d89ae4a8583fb8c71a49deb8b').json()
    
    data = r.get('articles')

    return render_template('news.html', data = data )  



# api call for nigeria news
@app.route('/nigeria_news')
def nigeria_news():
    data = requests.get('http://newsapi.org/v2/top-headlines?country=ng&category=health&apiKey=db0dbc6d89ae4a8583fb8c71a49deb8b').json()

    data = data.get('articles')

    return render_template('nigeria_news.html', data = data )  


# api call for outh africa health news all still via news api   
@app.route('/sa_news')
def sa_news():
    data = requests.get('http://newsapi.org/v2/top-headlines?country=za&category=health&apiKey=db0dbc6d89ae4a8583fb8c71a49deb8b').json()
    
    data = data.get('articles')

    return render_template('sa_news.html', data = data )  


# api call to covid19api.com , it feteches alll sumaeries of the pandemic , the same funtion calls covid19 updates from uganda , south africa nd nigeria

@app.route('/covidstats', methods=['GET'])
def covid_stats():
    r = requests.get('https://api.covid19api.com/summary').json()
    south_live = requests.get('https://api.covid19api.com/total/country/south-africa').json()
    uganda_live = requests.get('https://api.covid19api.com/total/country/uganda').json()
    nigeria_live = requests.get('https://api.covid19api.com/total/country/nigeria').json()
                                
    data = r
    south_data = south_live
    uganda_data = uganda_live
    nigeria_data = nigeria_live

    return render_template('covidstats.html', data = data, south_data = south_data, uganda_data = uganda_live, nigeria_data =nigeria_live )  


# creating user admin for the first time,
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('email', [validators.Length(min=1, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords doesnt match')])
    confirm = PasswordField('confirm Password')

    

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))


        # create cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(name, email, password) VALUES(%s, %s, %s)", (name, email, password))

        # commit to  db
        mysql.connection.commit()


        cur.close()

        flash('You are now registered and can NOW  login', 'success')

        redirect(url_for('Index'))

    return render_template('register.html', form=form)


#using the mailgun api, a user subcribes for email listing
def subscribe_user(email, user_group_email, api_key):
    r = requests.post(f"https://api.mailgun.net/v3/lists/{user_group_email}/members",
                auth=("api", api_key),
                  data={"subscribed": True,
                        "address": email}
    )


    print(r.status_code)
    return r


@app.route('/subscribe', methods=["GET", "POST"])
def subcribe():

    if request.method =="POST":
        email =  request.form.get('email')
        subscribe_user(email = email, 
                        user_group_email="healthrocy@sandbox30d1b9d9f64c4c35832b400b6bd46e66.mailgun.org",
                        api_key="0d12038e0871eb4f63aabc33f5d970f1-9b1bf5d3-0baad249"  )
        

    return render_template('subcribe.html')

if __name__ == '__main__':

    app.secret_key="secret123"
    app.run(debug=True)
