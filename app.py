from flask import Flask, jsonify, request, render_template, redirect, url_for,send_file 
from flask_api import FlaskAPI, status, exceptions
from PIL import Image
from werkzeug.utils import secure_filename
# from flaskext.mysql import MySQL
import os, json 
import requests 
import csv
import Model
import Model2
import threading
app = Flask(__name__)

@app.route('/') 
def index(): 
	return "Flask server" 

@app.route('/loggedInRec', methods = ['POST']) 
def recommenLoggedIn():
    req_data = request.get_json()
    result=Model.runCollab(req_data["user"],req_data["url"])
    print(result)    
    result=json.dumps(result)
    return jsonify({'msg': 'success','data_result':result})

@app.route('/contentRec', methods = ['POST']) 
def recommen():
    result=Model2.recommenFetch()
    
    result=json.dumps(result)
    print(result)    
    return jsonify({'msg': 'success','data_result':result})


def callToCSV():
    # requests.get('http://localhost:3000/tocsv')
    requests.get('https://cyber-store.herokuapp.com/tocsv')
    print("Happening")
    threading.Timer(20.0, callToCSV).start()

# threading.Timer(20.0, callToCSV).start()




if __name__ == "__main__": 
	app.run(threaded=True, port = int(os.environ.get('PORT', 5000)))
