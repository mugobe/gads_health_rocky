from flask import Flask, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
import requests
 



app = Flask(__name__)
CORS(app) ## To allow direct AJAX calls



headers = {
    'x-rapidapi-host': "getguidelines.p.rapidapi.com",
    'x-rapidapi-key': "4530cb2b74msh6b53c3be454b827p188292jsn9e5ec4781425"
    }



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

# #news categories
# @app.route('/heath_news_categoris')
# def Categories():
#     category = [
#             {
#                 'id':1,
#                 'title': 'Coronavirus'
#                 'description': "Find answers to questions about novel coronavirus (2019-nCoV), including disease basics, prevention, travel, and 2019-nCoV and animals information."
#             }

#     ]

# news list route and view
@app.route('/healthnews')
def News():
    return render_template('news.html')


#Health guidelines 

#get all guidelines
# @app.route('/healthguidelines')
# def HealthGuidelines():
#     url = "https://rapidapi.p.rapidapi.comhttps//getguidelines.com/all"

#     response = requests.request("GET", url, headers=headers)

#     return render_template('hg.html', response )              

@app.route('/healthguidelines', methods=['GET'])
def home():
    r = requests.get('http://dummy.restapiexample.com/api/v1/employees')
    
    response = r.json()

    return render_template('hg.html', response = response )  


@app.route('/cdc', methods=['GET'])
def cdc():
    r = requests.get('http://data.cdc.gov/')
    
    response = r

    return render_template('cdc.html', response = response )  

if __name__ == '__main__':
    app.run(debug=True)
