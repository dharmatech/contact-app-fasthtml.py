
import fasthtml

from contacts_model import Contact

ar = fasthtml.APIRouter()

# @app.route("/api/v1/contacts/{contact_id}", methods=['GET'])
@ar.get('/api/v1/contacts/{contact_id}')
def json_contacts_view(contact_id: int = 0):
    contact = Contact.find(contact_id)
    return contact.__dict__
