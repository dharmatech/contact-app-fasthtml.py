
import fasthtml

from fasthtml.common import Request, RedirectResponse

from contacts_model import Contact

ar = fasthtml.APIRouter()

# @app.route('/contacts/{contact_id}', methods=['DELETE'])
@ar.delete('/contacts/{contact_id}')
def contacts_delete(request: Request, contact_id: int = 0):
    contact = Contact.find(contact_id)
    contact.delete()
    if request.headers.get('HX-Trigger') == 'delete-btn':
        # flash("Deleted Contact!")
        print('Deleted Contact!')
        return RedirectResponse(url='/contacts', status_code=303)
    else:
        return ''