from Model import Model
import flask, os, werkzeug, cv2, sys
import tensorflow as tf
from flask import request,Flask, render_template, redirect, url_for, send_from_directory, request
from flask import session
from io import BytesIO

#"python.linting.pylintArgs": ["--extension-pkg-whitelist=cv2"] in settings.json
app = flask.Flask('Object Detect App')
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def redirect_upload():
    """
    A viewer function that redirects the Web application from the root to a HTML page for uploading an image to get classified.
    The HTML page is located under the /templates directory of the application.
    :return: HTML page used for uploading an image. It is 'upload_image.html' in this exmaple.
    """
    return flask.render_template(template_name_or_list="upload_image.html")

app.add_url_rule(rule="/", endpoint="homepage", view_func=redirect_upload)

def upload_image():
    """
    Viewer function that is called in response to getting to the 'http://localhost:7777/upload' URL.
    It uploads the selected image to the server.
    :return: redirects the application to a new page for predicting the class of the image.
    """
    #Global variable to hold the name of the image file for reuse later in prediction by the 'CNN_predict' viewer functions.
    global secure_filename
    if flask.request.method == "POST":#Checking of the HTTP method initiating the request is POST.
        img_file = flask.request.files["image_file"]#Getting the file name to get uploaded.
        print(img_file)
        secure_filename = werkzeug.utils.secure_filename(img_file.filename)#Getting a secure file name. It is a good practice to use it.
        img_path = os.path.join(app.root_path, secure_filename)#Preparing the full path under which the image will get saved.
        img_file.save(img_path)#Saving the image in the specified path.
        print("Image uploaded successfully.")
        """
        After uploading the image file successfully, next is to predict the class label of it.
        The application will fetch the URL that is tied to the HTML page responsible for prediction and redirects the browser to it.
        The URL is fetched using the endpoint 'predict'.
        """
        return flask.redirect(flask.url_for(endpoint="predict"))
    return "Image upload failed."

"""
Creating a route between the URL (http://localhost:7777/upload) to a viewer function that is called after navigating to such URL. 
Endpoint 'upload' is used to make the route reusable without hard-coding it later.
The set of HTTP method the viewer function is to respond to is added using the 'methods' argument.
In this case, the function will just respond to requests of method of type POST.
"""
app.add_url_rule(rule="/upload", endpoint="upload", view_func=upload_image, methods=["POST"])

@app.route('/predict',methods=['GET', 'POST'])
def predict():
    print(request.method)
    global secure_filename
    input_img_path = os.path.join(app.root_path, secure_filename)
    output_img_path = 'output'+os.path.sep
 
    #Prediction using Keras Model
    with graph.as_default():
        weed_model.predict(input_img_path, output_img_path)

    return flask.render_template(template_name_or_list="display_predicted_image.html", thumbnail_name = secure_filename)

app.add_url_rule(rule="/predict/", endpoint = "predict", view_func=predict, methods=['GET', 'POST'])


@app.route('/output/<filename>', methods = ['GET', 'POST'])
def output(filename):
    print("Display: ", filename)
    return send_from_directory('./output', filename)


#initialize()
if __name__ == '__main__':
    #Initialization Code
    #Code to Fix flask debug setting and threading issue
    #https://github.com/keras-team/keras/issues/2397
    tf.keras.backend.clear_session()
    global graph
    graph = tf.get_default_graph()

    #Load a model
    weed_model = Model('config-weed.json')

    #Running an app
    app.run(port=7777, debug= True, threaded= True, use_reloader=False)
    #Working config
    #app.run(port=7777, debug= False, threaded= False)