from flask import Flask, render_template, request, redirect, Response,jsonify,send_file
import random, json
import pandas as pd 
import cv2
import matplotlib.pyplot as plt

app = Flask(__name__)

df = pd.DataFrame()


@app.route('/api/a')
def image():
    return send_file('./Primavera.jpg',  mimetype='image/png')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.get_json()
    global df
    df = pd.DataFrame.from_dict(jsdata['cord'])
    print(df)
    
    return jsdata

@app.route('/df')
def get_df():
    
    detect(df)
    return {}






def detect(data):
    img = cv2.imread('./Primavera.jpg',cv2.IMREAD_GRAYSCALE)
    print(img.shape)

    img = cv2.resize(img,(911,700))

    print(img.shape)

    import pytesseract

    texts= {}
    df = data
    for i in range(df.shape[0]):
        label,y1,y2,x1,x2 = df['keys'][i],df['starty'][i],int(df['starty'][i]+df['h'][i]),df['startx'][i],int(df['startx'][i]+df['w'][i])
        roi = img[y1:y2,x1:x2]
        print(y1,y2,x1,x2)
        cv2.imwrite('new.jpg',roi)
        # text = pytesseract.image_to_string(roi)
        # texts[label] = text

    


    # print(texts)

app.run(debug=True)







