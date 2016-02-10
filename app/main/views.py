import os
from flask import render_template, request, redirect, url_for, jsonify
from flask.ext.login import current_user, login_required
from werkzeug.utils import secure_filename
from . import main
from manage import app
from .forms import PhotoForm
from ..models import Photo
from .. import db

# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])




@main.route('/')
def index():
    return render_template('index.html')

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# @main.route('/test', methods = ['GET', 'POST'])
# def test():
#     form = PhotoForm()
#     print app.config['UPLOAD_FOLDER']
#     print str(current_user.username)
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             if current_user.is_authenticated:
#                 userFolder = os.path.join(app.config['UPLOAD_FOLDER'], current_user.username)
#                 if not os.path.exists(userFolder):
#                     os.mkdir(userFolder)
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], current_user.username,filename))
#                 return redirect(url_for('main.test'))
#     return render_template('test.html', form = form)



@main.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        photo = Photo(store_path = os.path.join(current_user.username,filename), 
                        user_id = current_user.id, 
                        description = form.description.data)
        db.session.add(photo)
        db.session.commit()
        
        if current_user.is_authenticated:
            userFolder = os.path.join(app.config['UPLOAD_FOLDER'], current_user.username)
            if not os.path.exists(userFolder):
                    os.mkdir(userFolder)
            form.photo.data.save(app.config['UPLOAD_FOLDER']+ '/' + current_user.username + '/' + filename)
            return redirect(url_for('main.upload'))
    else:
        filename = None
    return render_template('upload.html', form= form, filename = filename)



# @main.route('/upload', methods = ['GET', 'POST'])
# @login_required
# def upload():
#     form = PhotoForm()
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             # store data to the database
#             photo = Photo(store_path = os.path.join(current_user.username,filename), 
#                         user_id = current_user.id, 
#                         description = form.description.data)
#             db.session.add(photo)
#             db.session.commit()
            
#             if current_user.is_authenticated:
#                 userFolder = os.path.join(app.config['UPLOAD_FOLDER'], current_user.username)
#                 if not os.path.exists(userFolder):
#                     os.mkdir(userFolder)
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], current_user.username,filename))
#                 return redirect(url_for('main.upload'))
#     return render_template('upload.html', form = form)



@main.route('/gallery', methods = ['GET'])
@login_required
def gallery():
    photos = db.session.query(Photo).filter_by(user_id = current_user.id).all()
    #temp = db.session.query(Photo).filter_by(user_id = current_user.id).first()
    #return render_template('gallery.html', photo_items = jsonify(PhotoItems=[i.to_json for i in photos]))
    #return jsonify(PhotoItems=[i.to_json for i in photos])
    return render_template('gallery.html', photo_dicts = [i.to_json for i in photos])


@main.route('/profile',methods = ['GET', 'POST'])
@login_required
def profile():
    photos = db.session.query(Photo).filter_by(user_id = current_user.id).all()
    photo_dicts = [i.to_json for i in photos]
    for photo in photo_dicts:
        photo['store_path'] = 'static/images/' + photo['store_path']
    return render_template('profile.html', photo_dicts = photo_dicts)

@main.route('/delete/<path:file_path>', methods = ['GET', 'POST'])
@login_required
def delete(file_path):
    #print file_path
    #return 'delete ' + file_path
    print ' ' + file_path
    deleteItem = db.session.query(Photo).filter_by(store_path=file_path).first()
    print deleteItem
    if request.method == 'POST':
        if deleteItem != None:
            db.session.delete(deleteItem)
            db.session.commit()
            flash('The photo has been removed!')
            return redirect(url_for('main.profile'))
    return render_template('delete.html', filepath=file_path)