from database import get_db
import lib
from flask import *
from werkzeug.utils import secure_filename
import json
import os
from PIL import Image


def compressMe(file):

    # Get the path of the file
    filepath = os.path.join(os.getcwd(),file)

    # open the image
    picture = Image.open(filepath).convert('RGB')

    # Save the picture with desired quality
    # To change the quality of image,
    # set the quality variable at
    # your desired level, The more
    # the value of quality variable
    # and lesser the compression
    picture.save(file,"JPEG",optimize=True, quality=30)
    return
# enctype="multipart/form-data" in html


def post():
    if 'file' not in request.files:
        flash('No file part')
        return "Error"
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return "Error"
    if file:
        db = get_db('database')
        lab_code = request.form['lab_code']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], lab_code+".png"))
        compressMe(os.path.join(app.config['UPLOAD_FOLDER'], lab_code+".png"))
        # print('upload_image filename: ' + filename)
        db.execute('UPDATE patient_out SET CBC=? , Timestamp = ?, Date = ?  WHERE Lab_Code=?',
                   (0, lib.time(), lib.date(), lab_code,))
        flash('Image successfully uploaded and displayed below')
        return "Done"
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return "Error"
