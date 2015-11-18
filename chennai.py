from flask import Flask,request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import os
import image

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
CONVERTED_FOLDER = 'converted/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print "loading"
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image.watermark_image(filename,'uploads/'+filename)
            return redirect(url_for('converted_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/converted/<filename>')
def converted_file(filename):
    return send_from_directory(app.config['CONVERTED_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.debug=True
    app.run()
