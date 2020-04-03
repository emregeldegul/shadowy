from os import path, remove

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import pymysql.cursors

from app.oauth.cloud import drive
from app.oauth.mysql import db, coursor

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/images')
@api.route('/images/index')
def images_index():
    return 'ok'

@api.route('/images/create', methods = ['POST'])
def images_create():
    diagnose_id = request.form.get('diagnose_id')
    location = request.form.get('location')
    value = request.form.get('value')
    image = request.files['image']

    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'image is required'})

    if image.filename == '':
            return jsonify({'status': 'error', 'message': 'image is required'})

    image_name= secure_filename(image.filename)

    image_file_path = path.join('app', 'static', image_name)
    image.save(image_file_path)

    image_file = drive.CreateFile({'title': image_name})
    image_file.SetContentFile(image_file_path)
    image_file.Upload()

    drive_id = image_file['id']

    remove(image_file_path)


    insert = coursor.execute('INSERT INTO images (diagnose_id, drive_id, location, value) VALUES (%s, %s , %s, %s)', (diagnose_id, drive_id, location, value))
    db.commit()

    return jsonify({'status': 'success', 'drive_id': drive_id})

@api.route('/images/<string:drive_id>')
def images_show(drive_id):
    try:
        drive_file = drive.CreateFile({'id': drive_id})
        drive_file.GetContentFile('app/static/{}'.format(drive_file['title']))
        file_path = path.join('static', drive_file['title'])

        return send_file(file_path, mimetype = 'image/gif')
    except:
        return jsonify({'status': 'error', 'message': 'image not found'}), 404

@api.route('/images/detail/<string:drive_id>')
def images_detail(drive_id):
    coursor.execute('SELECT * FROM images WHERE drive_id = %s', (drive_id))
    images = coursor.fetchall()
    return jsonify(images)
