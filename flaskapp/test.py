from flask import Flask, render_template, request, redirect, Response,jsonify,send_file, flash, url_for,session,make_response
from werkzeug.utils import secure_filename
from flask_session import Session

import random, json
import pandas as pd 
import cv2
import matplotlib.pyplot as plt
import os

#initiates flask app
app = Flask(__name__)

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




#Create empty dataframe to fill with cordinates later
df = pd.DataFrame()


#url to send image file to javascript intenrally
@app.route('/api/a')
def image():
    print(image)
    resp = make_response(send_file('./static/image/'+ image,  mimetype='image/png'))
    resp.set_cookie('sessionID', '', expires=0)
    return resp

#home page
@app.route('/')
def index():
    resp = make_response(render_template('index.html'))
    resp.set_cookie('sessionID', '', expires=0)
    return resp




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/draw', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'img-file' not in request.files:
            flash('No img file')
            return redirect(request.url)
        # if 'pdf-file' not in request.files:
        #     flash('No pdf file')
        #     return redirect(request.url)
        img_file = request.files['img-file']
        print("Inhere")
        # pdf_file = request.files['pdf-file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if img_file.filename == '':
            flash('No image file selected')
            return redirect(request.url)
        # if pdf_file.filename == '':
        #     flash('No pdf file selected')
        #     return redirect(request.url)
        if img_file and allowed_file(img_file.filename):
            print("In image fuct************************************")
            global image
            image = img_file.filename
            
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join( "./static" + "/image", filename))
        
        return redirect(url_for('upload_file'))
    resp = make_response(render_template('draw.html'))
    resp.set_cookie('sessionID', '', expires=0)
    return resp



#onclick submit button ajax query posts cord json object contaning all cordinates to this url
@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    
    #loads json data in jsdata 
    jsdata = request.get_json()
    
    #makes df global variable so it can be accessed throughout this file
    global df
    
    #populates df dataframe with the recieved cordinates in jsdata 
    df = pd.DataFrame.from_dict(jsdata['cord'])
    print(df)
    
    #just a return statement 
    #no change needed in here
    return jsdata



#url htttp://127.0.0.1/5000/df
#access this url after clicking submit in the form to call the detect function defined in here
@app.route('/df')
def get_df():
    
    detect(df)
    return {}





#detect function to load the image here in server in img variable

def detect(data):
    
    #reads the img 
    img = cv2.imread('./Primavera.jpg',cv2.IMREAD_GRAYSCALE)
    print(img.shape)

    #as default width for canvas in html is 700
    width =700
    
    #calculate height for new rescaled image as per width of canvas and maintaining image aspect ratio
    height = width * (img.shape[0]/img.shape[1])
    
    #resize img with new dimensions
    img = cv2.resize(img,(height,width))

    print(img.shape)

    import pytesseract

    #creates a empty dictionary to store keys and extracted text values from pytesseraact
    texts= {}
    df = data
    
    #looping over each row in dataframe
    #each row contains Key and cordinates of the region
    for i in range(df.shape[0]):
        
        #pull values from dataframe by [column_name] and [index] to respective variable 
        label,y1,y2,x1,x2 = df['keys'][i],df['starty'][i],int(df['starty'][i]+df['h'][i]),df['startx'][i],int(df['startx'][i]+df['w'][i])
        
        #crop the image with given the above cordinates
        roi = img[y1:y2,x1:x2]
        
        #print cordinates
        print(y1,y2,x1,x2)
        
        #Write the crop image to disk and check if it is the correct region 
        cv2.imwrite('new.jpg',roi)
        
        
        #below is tesseract code which takes croped regoin of image as input and outputs texts in the image
        #uncomment when achieved extracting correct region
        ## text = pytesseract.image_to_string(roi)
        ## texts[label] = text

    

    #prints the texts dictionary containing Keys and extreacted texts
    # print(texts)

    
#Run the app
app.run(debug=True)







