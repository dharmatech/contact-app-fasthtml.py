
import fasthtml

from contacts_model import Contact

ar = fasthtml.APIRouter()

# @app.route("/api/v1/contacts/{contact_id}", methods=['DELETE'])
@ar.delete('/api/v1/contacts/{contact_id}')
def json_contacts_delete(contact_id: int = 0):
    contact = Contact.find(contact_id)
    contact.delete()
    return {"success": True}
