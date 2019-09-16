from flask import Flask, render_template, request
from database_handlers import mongo_handler
import json

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def dashboard():
    return render_template('index.html')

@app.route('/network-visual', methods = ['GET'])
def return_visual():
    return render_template('network.html')

@app.route('/import-assets', methods = ['GET'])
def import_assets():
    current_data = mongo_handler.get_data()
    return render_template('import-assets.html', data=current_data)

@app.route('/configuration', methods = ['GET'])
def configuration():
    return render_template('config.html')

@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == 'POST':
        raw_data = request.files['raw_data'].read().decode("utf-8")
        try:
            data_list = raw_data.split('\n')
            for obj in data_list:
                obj = obj.replace('\n', '')
            mongo_handler.add_data(data_list)
            current_data = mongo_handler.get_data()
            return render_template('import-assets.html', data=current_data)
        except Exception as e:
            print (e)
            return render_template('failed-upload.html')

@app.route('/upload-json', methods = ['POST'])
def upload_json():
    if request.method == 'POST':
        raw_data = request.files['data'].read().decode("utf-8")
        try:
            data_list = raw_data.split('\n')
            for obj in data_list:
                obj = obj.replace('\n', '')
            mongo_handler.add_data(data_list)
            current_data = mongo_handler.get_data()
            return render_template('import-assets.html', data=current_data)
        except Exception as e:
            print (e)
            return render_template('failed-upload.html')