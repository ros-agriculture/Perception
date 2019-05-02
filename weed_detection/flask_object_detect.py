import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def hello():
    return "This Machine Learning App detects objects in an image"

@app.route('/predict', methods = ['POST', 'GET'])
def predict():
    print(request.method)
    if request.method == 'POST':
        try:
            recv_data = request.get_json()
            data = recv_data['data']
            
        
        except ValueError:
            return jsonify("Please enter a number")
        #print('In post method')
        #return jsonify("I made it")
        return jsonify('Got Input : '+str(data))
    
    if request.method != 'POST':
        error = 'You have requested {} method, only POST method is allowed'.format(request.method)
        print(error)
        return error


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)



