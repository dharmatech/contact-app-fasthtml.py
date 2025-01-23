
import fasthtml

from contacts_model import Contact

ar = fasthtml.APIRouter()

from template_show import template_show

# @app.route('/contacts/{contact_id}')
@ar.get('/contacts/{contact_id}')
def contacts_view(contact_id: int = 0):
    contact = Contact.find(contact_id)
    return template_show(contact)
