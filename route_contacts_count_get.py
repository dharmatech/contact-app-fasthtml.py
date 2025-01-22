import fasthtml

from contacts_model import Contact

ar = fasthtml.APIRouter()

# @app.route("/contacts/count", methods=['GET'])
@ar.get('/contacts/count')
def contacts_count():
    count = Contact.count()
    return "(" + str(count) + " total Contacts)"