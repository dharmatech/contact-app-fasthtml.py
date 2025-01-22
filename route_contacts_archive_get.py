
import fasthtml

from contacts_model import Archiver

from template_archive_ui import template_archive_ui

ar = fasthtml.APIRouter()

# @app.route("/contacts/archive", methods=['GET'])
@ar.get('/contacts/archive')
def archive_status():

    archiver = Archiver.get()
    return template_archive_ui(archiver)