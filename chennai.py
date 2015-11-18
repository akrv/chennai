from flask import Flask,request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import os
import image

app = Flask(__name__)
app.config.from_object('config')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # TODO upload image or click facebook button to load profile pic
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
    # TODO write facebook upload logic
    return send_from_directory(app.config['CONVERTED_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.debug=True
    app.run()
