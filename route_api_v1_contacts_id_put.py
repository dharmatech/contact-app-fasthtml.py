
import fasthtml

# from fasthtml.common import Request

from starlette.requests import Request

from contacts_model import Contact

ar = fasthtml.APIRouter()

# @app.route("/api/v1/contacts/{contact_id}", methods=['GET'])
# @ar.get('/api/v1/contacts/{contact_id}')
# def json_contacts_view(contact_id: int = 0):
#     contact = Contact.find(contact_id)
#     return contact.__dict__

# @app.route("/api/v1/contacts/{contact_id}", methods=['PUT'])
# @ar.put('/api/v1/contacts/{contact_id}')
@ar.post('/api/v1/contacts/{contact_id}')
async def json_contacts_edit(request: Request, contact_id: int = 0):

    print(f'/api/vs/contacts/{contact_id} PUT')

    form_data = await request.form()

    # print(f'first_name: {form_data.get('first_name')}')

    print(request.headers)

    print(form_data)

    c = Contact.find(contact_id)


    # Contact.load_db()

    # c = Contact.find(9)

    # print(c)

    # c.update(first='abc', last='bcd', phone='123', email='xyz@example.com')

    # print(c)


    print(
        form_data.get('first_name'),
        form_data.get('last_name'),
        form_data.get('phone'),
        form_data.get('email')
    )

    c.update(
        first=form_data.get('first_name'),
        last =form_data.get('last_name'),
        phone=form_data.get('phone'),
        email=form_data.get('email')
    )

    print(c)

    if c.save():
        return c.__dict__
    else:
        return {"errors": c.errors}, 400
