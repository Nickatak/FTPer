from flask import Flask, redirect, render_template, request, send_file, url_for
from server.models import DBManager, File, User
from conf import BASE_DIR, TEMPLATE_DIR, UPLOAD_DIR
from server.converters import UUIDConverter

import pathlib

app = Flask(__name__, template_folder=str(TEMPLATE_DIR))
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.url_map.converters['uuid'] = UUIDConverter
db = DBManager()

# OOOOOF I really wanted to avoid this str-byte conversion.  Let's get it working for now, and then I'll replace it later. I can do something fancy and add my own converter (from werkzeug.routing.BaseConverter), but, the problem with that is I still have to keep converting from a str to a UUID regardless.  I guess there's no real way to avoid this, IF I want to use it as a slug.
@app.route('/<uuid:file_uuid>', methods=['GET', 'POST'])
def file_view(file_uuid):
    # One of two things is going to happen in this route:
        # 1. Get a form to upload a file.
        # 2. POST comes here, and we upload said file.


    file = db.session.query(File).get(file_uuid) 
    if not file:
        return render_template('404.html')
    elif file.completed:
        return redirect(url_for('serve_file', file_uuid=file_uuid))


    if request.method == 'POST':
        # I want this to handle an AJAX post.
        # We'll add error handling later.
        flask_file = request.files['file_upload']
        ext = pathlib.Path(flask_file.filename).suffix

        flask_file.save(UPLOAD_DIR.joinpath('{}{}'.format(file_uuid.hex, ext)))
        file.ext = ext
        file.completed = True
        db.session.commit()

        # Let's make this a template for now.
        return render_template('file_upload_complete.html', file=file)
    else:
        return render_template('file_upload.html', file=file)

# Okay, yeah, if I do this, I definitely want to use a custom converter so I can validate the URL without activating the route for security reasons.  I'm still going to leave it as a STR right now, but this is decided that I'll do it later.
@app.route('/download/<uuid:file_uuid>')
def serve_file(file_uuid):
    file = db.session.query(File).get(file_uuid) 
    if not file:
        return render_template('404.html')
    elif not file.completed:
        return redirect(url_for('file_view', file_uuid=file_uuid))

    file_path = BASE_DIR.joinpath('downloads', '{}{}'.format(file_uuid.hex, file.ext))
    return send_file(file_path)

