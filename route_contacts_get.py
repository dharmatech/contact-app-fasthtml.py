
import fasthtml

from contacts_model import Contact

ar = fasthtml.APIRouter()

from template_index import template_index

@ar.get('/contacts')
def contacts(request, q: str = None, page: str = '1'):    
    
    search = q

    page = int(page)

    if search is not None:
        contacts_set = Contact.search(search)
        if request.headers.get('HX-Trigger') == 'search':
            return 'HX-Trigger'
    else:
        contacts_set = Contact.all()
    
    return template_index(q, contacts_set)