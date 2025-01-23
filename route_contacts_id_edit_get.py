
import fasthtml

from contacts_model import Contact

ar = fasthtml.APIRouter()

from template_edit import template_edit

# @app.route('/contacts/{contact_id}/edit', methods=['GET'])
@ar.get('/contacts/{contact_id}/edit')
def contacts_edit_get(contact_id: int = 0):
    contact = Contact.find(contact_id)
    return template_edit(contact)
