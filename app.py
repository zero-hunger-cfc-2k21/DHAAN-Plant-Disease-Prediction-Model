# Flask utils
import os
from tensorflow.keras.preprocessing import image
from flask import Flask, redirect, url_for, request, render_template
import numpy as np
from werkzeug.utils import secure_filename
#from flask_ngrok import run_with_ngrok
#from gevent import WSGIServer
from keras.models import load_model

model = load_model('dhaani.h5',compile=False)
print('Model loaded')
 
# Define a flask app
app = Flask(__name__)
#run_with_ngrok(app) 

def model_predict(img_path, model):
    img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    show_img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = np.array(x, 'float32')
    x /= 255
    preds = model.predict(x)
    print(preds)
    return preds


@app.route('/')
def index():
    # Main page
    print('index root')
    return render_template('index.html')


@app.route('/predict', methods=['GET','POST'])
def upload():
    
    if request.method == 'POST':
       
        # Get the file from post request
        f = request.files['file']
        
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        print(preds[0])

        # x = x.reshape([64, 64]);
        disease_class = ['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy', 'Potato___Early_blight',
                         'Potato___Late_blight', 'Potato___healthy', 'Tomato_Bacterial_spot', 'Tomato_Early_blight',
                         'Tomato_Late_blight', 'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
                         'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
                         'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus', 'Tomato_healthy']
        a = preds[0]
        ind=np.argmax(a)
        print('Prediction:', disease_class[ind])

        '''if(disease_class == "Tomato__Tomato_mosaic_virus"):
            print("""Cultural control :\n\nUse certified disease-free seed or treat your own seed.\n
                Soak seeds in a 10% solution of trisodium phosphate (Na3PO4) for at least 15 minutes.\n
                Or heat dry seeds to 158 °F and hold them at that temperature for two to four days.\n
                Purchase transplants only from reputable sources. Ask about the sanitation procedures they use to prevent disease.\n
                Inspect transplants prior to purchase. Choose only transplants showing no clear symptoms.\n
                Avoid planting in fields where tomato root debris is present, as the virus can survive long-term in roots.\n
                Wash hands with soap and water before and during the handling of plants to reduce potential spread between plants.\n
                Disinfect tools regularly — ideally between each plant, as plants can be infected before showing obvious symptoms.\n
                Soaking tools for 1 minute in a 1:9 dilution of germicidal bleach is highly effective.\n
                Or a 1-minute soak in a 20% weight/volume solution of nonfat dry milk and water is also very effective.\n
                When pruning plants, have two pruners and alternate between them to allow proper soaking time between plants.\n
                Avoid using tobacco products around tomato plants, and wash hands after using tobacco products and before working with the plants.\n
                Tobacco in cigarettes and other tobacco products may be infected with either ToMV or TMV, both of which could spread to the tomato plants.\n
                Scout plants regularly. If plants displaying symptoms of ToMV or TMV are found, remove the entire plant (including roots), bag the plant, and send it to the University of Minnesota Plant Diagnostic Clinic for diagnosis.\n
                If ToMV or TMV is confirmed, employ stringent sanitation procedures to reduce spread to other plants, fields, tunnels and greenhouses.\n
                Completely pull up and burn infected plants. Do not compost infected plant material.\n
                After working with diseased plants, thoroughly disinfect all tools and hands as outlined above.\n
                For added security against spread, keep separate tools for working in the diseased area and avoid working with healthy plants after working in an area with diseased plants.\n
                At the end of the season, burn all plants from diseased areas, even healthy-appearing ones, or bury them away from vegetable production areas.\n
                Disinfect stakes, ties, wires or any other equipment between growing seasons using the methods noted above.\n
                Chemical control\n
                There are currently no chemical options that are effective against either virus.\n""")
        else:
            print("Control strategy would be provided for all the diseases in future")
        '''
        
        result=disease_class[ind]
        print (result)
        return result
    return 'Please try with an image of a crop / plant'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8080')





