import flask
from flask import request,Flask, render_template, redirect, url_for, send_from_directory, request
import os
import werkzeug
import werkzeug.utils
import cv2

from io import BytesIO
import base64
#"python.linting.pylintArgs": ["--extension-pkg-whitelist=cv2"] in settings.json
app = flask.Flask('Object Detect App')

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
    #Reading the image file from the path it was saved in previously.
    img = cv2.imread(os.path.join(app.root_path, secure_filename))
    img_filename = os.path.join(app.root_path, secure_filename)
    print(img_filename)
    #print(str(img.shape))

    target = 'output'+os.path.sep
    exec_str = "python predict.py -c config-weed.json -i {} -o {} ".format(img_filename, target)
    print(exec_str)
    os.system(exec_str)
    #return ("Image Shape: {}".format(str(img.shape)))
    destination = os.path.join(target, secure_filename)
    print("destination :", os.path.join(app.root_path, destination))
    src = secure_filename
    return flask.render_template(template_name_or_list="display_predicted_image.html", thumbnail_name = secure_filename)



@app.route('/output/<filename>', methods = ['GET', 'POST'])
def output(filename):
    print("Display: ", filename)
    return send_from_directory('./output', filename)


#initialize()
if __name__ == '__main__':
    
    app.run(port=7777, debug= True)