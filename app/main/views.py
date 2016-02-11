import os
from flask import render_template, request, flash, redirect, url_for, jsonify
from flask.ext.login import current_user, login_required
from werkzeug.utils import secure_filename
from . import main
from manage import app
from .forms import PhotoForm
from ..models import Photo
from .. import db
import time






"""
    Upload photos
"""
@main.route('/upload', methods = ['GET', 'POST'])
@login_required
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        photo = Photo(filename=filename,
                        store_path = os.path.join(current_user.username,filename), 
                        user_id = current_user.id, 
                        description = form.description.data)
        db.session.add(photo)
        db.session.commit()
        
        if current_user.is_authenticated:
            userFolder = os.path.join(app.config['UPLOAD_FOLDER'], current_user.username)
            if not os.path.exists(userFolder):
                    os.mkdir(userFolder)
            form.photo.data.save(app.config['UPLOAD_FOLDER']+ '/' + current_user.username + '/' + filename)
            flash('Upload Success!')
            return redirect(url_for('main.upload'))
    else:
        filename = None
    return render_template('upload.html', form= form, filename = filename)



"""
    User's Gallery
    The main part is made by JS and CSS
"""
@main.route('/')
@main.route('/gallery', methods = ['GET'])
@login_required
def gallery():
    photos = db.session.query(Photo).filter_by(user_id = current_user.id).all()

    return render_template('gallery.html', photo_dicts = [i.to_json for i in photos])



"""
    shows all photos uploaded by user
"""
@main.route('/profile',methods = ['GET', 'POST'])
@login_required
def profile():
    photos = db.session.query(Photo).filter_by(user_id = current_user.id).all()
    photo_dicts = [i.to_json for i in photos]
    for photo in photo_dicts:
        photo['store_path'] = 'static/images/' + photo['store_path']
        print photo['filename']
    return render_template('profile.html', photo_dicts = photo_dicts)


"""
    Delete Photo
    Can only access through /profile
"""
@main.route('/delete/<path:filename>', methods = ['GET', 'POST'])
@login_required
def delete(filename):
    deleteItem = db.session.query(Photo).filter_by(filename=filename).first()
    file_path = current_user.username + '/' + filename
    if request.method == 'POST':
        if deleteItem != None:
            db.session.delete(deleteItem)
            db.session.commit()
            # the path only work by using path.join
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_path))
            # flash do not work for redirect function
            # flash('The photo has been removed! And broswer will be redirect to profile page in 1 seconds')
            # time.sleep(1)
            return redirect(url_for('main.profile'))
    return render_template('delete.html', filename= filename, file_path = os.path.join('/static/images', file_path))