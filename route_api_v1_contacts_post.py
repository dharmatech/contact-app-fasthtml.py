
import fasthtml

from fasthtml.common import Request

from contacts_model import Contact

ar = fasthtml.APIRouter()

# @app.route("/api/v1/contacts", methods=['POST'])
@ar.post('/api/v1/contacts')
async def json_contacts_new(request: Request):

    form_data = await request.form()

    c = Contact(
        id_=None,
        first=form_data.get('first_name'),
        last =form_data.get('last_name'),
        phone=form_data.get('phone'),
        email=form_data.get('email')
    )

    if c.save():
        return c.__dict__
    else:
        return {"errors": c.errors}, 400