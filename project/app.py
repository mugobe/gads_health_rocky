from flask import Flask, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
import xmltodict

import json, xmljson
from lxml.etree import fromstring, tostring

import requests

 



app = Flask(__name__)
CORS(app) ## To allow direct AJAX calls


# home page route and view
@app.route('/')
def Index():

    category = [
             {
                'id':1,
                'title': 'Coronavirus',
                'description': "Find answers to questions about novel coronavirus, including disease basics, prevention, travel, and 2019-nCoV and animals information."
            },

              {
                'id':2,
                'title': 'Infectious Diseases',
                'description': "Find answers to questions about novel coronavirus, including disease basics, prevention, travel, and 2019-nCoV and animals information."
            },

              {
                'id':3,
                'title': 'Nutrition',
                'description': "Find answers to questions about novel coronavirus, including disease basics, prevention, travel, and 2019-nCoV and animals information."
            },

            {
                'id':4,
                'title': 'Hospitals',
                'description': "Find answers to questions about novel coronavirus, including disease basics, prevention, travel, and 2019-nCoV and animals information."
            }


    ]

    return render_template('home.html', news_categories=category)

# news list route and view
# @app.route('/healthnews')
# def News():
#     return render_template('news.html')

# # @app.route('/articles')
# # def articles():
# #     return render_template('articles.html', articles=Articles)




            

@app.route('/healthguidelines', methods=['GET'])
def home():
    r = requests.get('http://dummy.restapiexample.com/api/v1/employees')
    
    response = r

    return render_template('hg.html', response = response )  


@app.route('/worldhealthnews', methods=['GET'])
def world_health_news():
    r = requests.get('http://newsapi.org/v2/top-headlines?country=us&category=health&apiKey=db0dbc6d89ae4a8583fb8c71a49deb8b').json()
    
    data = r.get('articles')

    return render_template('news.html', data = data )  


@app.route('/who')
def who():
    data = requests.get('https://www.who.int/rss-feeds/news-english.xml').json()

    

    
    data = data.get(link)
    json.dumps(xmljson.badgerfish.data(data))

    # data = xmltodict.parse(data)

    return render_template('who.html', data = data)





@app.route('/covidstats', methods=['GET'])
def covid_stats():
    r = requests.get('https://api.covid19api.com/stats').json()
    
    data = r

    return render_template('covidstats.html', data = data )  

if __name__ == '__main__':
    app.run(debug=True)
