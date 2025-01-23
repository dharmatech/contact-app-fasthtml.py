
import fasthtml

from fasthtml.common import Request, RedirectResponse

from contacts_model import Contact

ar = fasthtml.APIRouter()

from template_edit import template_edit

# @app.route('/contacts/{contact_id}/edit', methods=['POST'])
@ar.post('/contacts/{contact_id}/edit')
async def contacts_edit_post(request: Request, contact_id: int = 0):

    form_data = await request.form()

    c = Contact.find(contact_id)

    c.update(
        first=form_data.get('first_name'),
        last =form_data.get('last_name'),
        phone=form_data.get('phone'),
        email=form_data.get('email')
    )

    if c.save():
        print('Updated Contact!')
        # flash("Updated Contact!")        
        return RedirectResponse(url=f'/contacts/{contact_id}', status_code=303)
    else:
        return template_edit(c)
