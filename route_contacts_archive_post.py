
import fasthtml

from contacts_model import Archiver

from template_archive_ui import template_archive_ui

ar = fasthtml.APIRouter()

# @app.route("/contacts/archive", methods=['POST'])
@ar.post('/contacts/archive')
def start_archive():

    archiver = Archiver.get()
    archiver.run()
    return template_archive_ui(archiver)