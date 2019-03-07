
from flask import Flask, render_template, request, redirect, url_for,session
import requests
import json
import subprocess

#initialize the App
app = Flask(__name__)


## Ecash function is a view (request handler). use decorator to route URLS to view

@app.route('/home')
def home_page():
	# render a static template
    return render_template('home.html')

@app.route('/')
def index():
	# redirect to home
	return redirect(url_for('home_page'))




@app.route('/classify', methods=['GET'])
def classify_page():
    try:
        #postedData = request.get_json()
        #url = request.form['homepage']
        url = request.args.get('homepage')
        #print(url)
    except Exception as e:
        retJson= app.logger.info('Invalid image URL')
        return render_template('classify.html', error='Invalid URL', retJson=str(e)),301
    #get image
    r = requests.get(url)
    retJson = {}
    with open('temp.jpg', 'wb') as f:
        f.write(r.content)
        proc =  subprocess.Popen('python classify_image.py --model_dir=. --image_file=./temp.jpg', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        ret = proc.communicate()[0]
        proc.wait()
        with open('text.txt') as g:
            retJson = json.load(g)
        return render_template('classify.html', retJson=retJson)
    return render_template('classify.html', error='Invalid URL', retJson='No Request' )

            

if __name__ =='__main__':
    app.run(host ='0.0.0.0',debug=True)