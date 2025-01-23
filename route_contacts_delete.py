
import fasthtml

import starlette

from fasthtml.common import Request

from contacts_model import Contact

from template_index import template_index

ar = fasthtml.APIRouter()
    
# @app.route('/contacts', methods=['DELETE'])
@ar.delete('/contacts')
async def contacts_delete_all(request: Request):
        
    form_data: starlette.datastructures.FormData = await request.form()

    contact_ids = form_data.getlist('selected_contact_ids')

    contact_ids = list(map(int, contact_ids))

    for id in contact_ids:
        contact = Contact.find(id)
        contact.delete()

    # flash("Deleted Contacts!")

    print('Deleted Contacts!')

    contacts_set = Contact.all(page=1)

    return template_index(None, contacts_set)