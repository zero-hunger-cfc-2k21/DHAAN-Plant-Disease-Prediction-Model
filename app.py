#Plant Disease Prediction Model

# Flask utils
import os
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from keras.models import load_model

model = load_model('model/dhaani.h5',compile=False)

print('Model loaded')

# Define a flask app
app = Flask(__name__, template_folder='Dhaan/')

def model_predict(img_path, model):
    img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    show_img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = np.array(x, 'float32')
    x /= 255
    preds = model.predict(x)
    return preds


@app.route('/')
def index():
    # Main page
    print('index root')
    
    return (
            """<form action="http://cc13a3317ef2.ngrok.io/predict" id="upload-file" method="post" enctype="multipart/form-data">
                  <input type="file" name="file" class="btn btn-success" id="imageUpload" accept=".png, .jpg, .jpeg">
              </form>


              <div class="image-section">
                <img id="imagePreview"  class="img-responsive" src="#" style="width:300px;height:300px;display:none"/><br><br>
                <div>
                  <button type="button" class="btn btn-info btn-lg " id="btn-predict">Predict!</button>
                </div>
            </div>"""
    )


@app.route('/predict', methods=['GET','POST'])
def upload():
    print('hello going inside')
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        print('smile')
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads/', secure_filename(f.filename))
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
        result=disease_class[ind]
        return result
    return None


if __name__ == '__main__':
 
    app.run()
