from flask import Flask, render_template, redirect, url_for,request
from flask import make_response, jsonify
from Detect import Test
import json

from flask_cors import CORS
app = Flask(__name__)
CORS(app)



@app.route("/",methods=['GET','POST'])
def home():
    datafromjs = request.form['mydata']
    response=Test.finalFunc(datafromjs)
    print(type(response))
    #response.headers.add('Access-Control-Allow-Origin', '*')
    #return '10'
    #print(datafromjs)
    return str(response)


if __name__ == "__main__":
    app.run(debug = True)
