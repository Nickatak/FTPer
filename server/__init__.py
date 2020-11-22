"""Main server file."""

from pathlib import Path
from typing import Union
from uuid import UUID

from flask import Flask, redirect, render_template, request, send_file, url_for

from conf import BASE_DIR, TEMPLATE_DIR, UPLOAD_DIR
from server.converters import UUIDConverter
from server.models import DBManager, File, User
from server.types import FileStorage, Response


app: Flask = Flask(__name__, template_folder=str(TEMPLATE_DIR))
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.url_map.converters['uuid'] = UUIDConverter
db: DBManager = DBManager()

@app.route('/<uuid:file_uuid>', methods=['GET', 'POST'])
def file_view(file_uuid: UUID) -> Union[str, Response]:
    """View for uploading files.
            :file_uuid: UUID of the file that we're uploading.
    """

    file: Union[File, None] = db.session.query(File).get(file_uuid) 
    if file is None:
        return render_template('404.html')
    elif file.completed:
        return redirect(url_for('serve_file', file_uuid=file_uuid))


    if request.method == 'POST':
        flask_file: FileStorage = request.files['file_upload']
        ext: str = Path(flask_file.filename or '').suffix

        flask_file.save(str(UPLOAD_DIR.joinpath('{}{}'.format(file_uuid.hex, ext))))
        file.ext = ext
        file.completed = True
        db.session.commit()

        # Let's make this a template for now.
        return render_template('file_upload_complete.html', file=file)
    else:
        return render_template('file_upload.html', file=file)

@app.route('/download/<uuid:file_uuid>')
def serve_file(file_uuid) -> Union[str, Response]:
    """View for downloading files.
            :file_uuid: UUID of the file that we're downloading.
    """

    file: Union[File, None] = db.session.query(File).get(file_uuid) 
    if file is None:
        return render_template('404.html')
    elif not file.completed:
        return redirect(url_for('file_view', file_uuid=file_uuid))

    file_path: Path = BASE_DIR.joinpath('downloads', '{}{}'.format(file_uuid.hex, file.ext))
    return send_file(file_path)

