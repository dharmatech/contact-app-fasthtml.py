
import fasthtml

from contacts_model import Contact

ar = fasthtml.APIRouter()

# @app.route("/api/v1/contacts", methods=['GET'])
@ar.get('/api/v1/contacts')
def json_contacts():
    contacts_set = Contact.all()
    return {"contacts": [c.__dict__ for c in contacts_set]}
