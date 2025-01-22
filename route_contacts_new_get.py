
import fasthtml

from contacts_model import Contact

from template_new import template_new

ar = fasthtml.APIRouter()

# @app.route("/contacts/new", methods=['GET'])
@ar.get('/contacts/new')
def contacts_new_get():

    # print('/contacts/new GET')

    return template_new(contact=Contact())