
import fasthtml

from fasthtml.common import Request, RedirectResponse

from contacts_model import Contact

from template_new import template_new

ar = fasthtml.APIRouter()

# @app.route('/contacts/new', methods=['POST'])
@ar.post('/contacts/new')
async def contacts_new(request: Request):

    form_data = await request.form()
    
    c = Contact(
        id_=None,

        first=form_data.get('first_name'),
        last =form_data.get('last_name'),
        phone=form_data.get('phone'),
        email=form_data.get('email')
    )

    if c.save():
        print('Created New Contact!')
        # flash('Created New Contact!')
        return RedirectResponse(url='/contacts', status_code=303)
    else:
        return template_new(c)