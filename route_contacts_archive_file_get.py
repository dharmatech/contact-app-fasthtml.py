
import fasthtml

import starlette

from contacts_model import Archiver

ar = fasthtml.APIRouter()

# @app.route("/contacts/archive/file", methods=['GET'])
@ar.get('/contacts/archive/file')
def archive_content():
    print('archive_content')
    archiver = Archiver.get()
        
    return starlette.responses.FileResponse(
        path=archiver.archive_file(),
        filename='archive.json',
        content_disposition_type='attachment'
    )