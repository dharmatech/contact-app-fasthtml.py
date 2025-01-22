
import fasthtml

from contacts_model import Archiver

from template_archive_ui import template_archive_ui

ar = fasthtml.APIRouter()

# @app.route("/contacts/archive", methods=['DELETE'])
@ar.delete('/contacts/archive')
def reset_archive():
    archiver = Archiver.get()
    archiver.reset()
    return template_archive_ui(archiver)