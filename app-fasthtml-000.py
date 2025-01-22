
from fasthtml.common import *

from fasthtml.components import All_caps, Sub_title

import starlette
import starlette.responses

# from flask import (
#     Flask, 
#     # request, 
#     flash, jsonify, send_file
# )

# from flask import send_file

from contacts_model import Contact, Archiver

import time

Contact.load_db()

app, rt = fast_app(
    pico=False,
    hdrs=(
        Link(rel='stylesheet', href='https://the.missing.style/v0.2.0/missing.min.css'),
        Link(rel='stylesheet', href='/static/site.css'),
        # Script(src='/static/js/htmx-1.8.0.js'),
        # Script(src='/static/js/_hyperscript-0.9.7.js'),
        Script(src='/static/js/rsjs-menu.js', type='module'),
        Script(src='https://unpkg.com/alpinejs@3/dist/cdn.min.js', defer=True)
    )
)

# ---------------------------------------------------------
@app.route('/')
def index():
    return RedirectResponse(url='/contacts')
# ---------------------------------------------------------
from template_layout import layout

from template_archive_ui import template_archive_ui

from template_index import template_index
# ---------------------------------------------------------

import route_contacts_get

route_contacts_get.ar.to_app(app)

# ---------------------------------------------------------
import route_contacts_archive_post

route_contacts_archive_post.ar.to_app(app)
# ---------------------------------------------------------
import route_contacts_archive_get

route_contacts_archive_get.ar.to_app(app)

# ---------------------------------------------------------
import route_contacts_archive_file_get

route_contacts_archive_file_get.ar.to_app(app)
# ---------------------------------------------------------
import route_contacts_archive_delete

route_contacts_archive_delete.ar.to_app(app)
# ---------------------------------------------------------
import route_contacts_count_get

route_contacts_count_get.ar.to_app(app)
# ---------------------------------------------------------
from template_new import template_new

# @app.route("/contacts/new", methods=['GET'])
# def contacts_new_get():

#     print('/contacts/new GET')

#     return template_new(contact=Contact())

import route_contacts_new_get

route_contacts_new_get.ar.to_app(app)

# @app.route("/contacts/new", methods=['GET'])
# def contacts_new_get():
#     return render_template("new.html", contact=Contact())
# ---------------------------------------------------------
@app.route('/contacts/new', methods=['POST'])
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
        return RedirectResponse(url='/contacts')
    else:
        print('calling template_new')
        return template_new(c)
# ---------------------------------------------------------
def template_show(contact):
    return layout(
        H1(contact.first, ' ', contact.last),

        Div(
            Div(f'Phone: {contact.phone}'),
            Div(f'Email: {contact.email}')
        ),

        P(
            A('Edit', href=f'/contacts/{contact.id}/edit'),
            A('Back', href='/contacts')
        )
    )

@app.route('/contacts/{contact_id}')
def contacts_view(contact_id: int = 0):
    contact = Contact.find(contact_id)
    return template_show(contact)
    
# print(to_xml(str(contacts_view).format(contact_id=123)))

# print(to_xml(str(contacts_view).format(contact_id3=123)))



# @app.route("/contacts/<contact_id>")
# def contacts_view(contact_id=0):
#     contact = Contact.find(contact_id)
#     return render_template("show.html", contact=contact)
# ---------------------------------------------------------

def template_edit(contact):

    def row(label, id, value, errors):
        return P(
            Label(label, _for=id),
            Input(
                name=id,
                id=id,
                type='text',
                placeholder=label,
                value=value or ''
            ),
            Span(
                # contact.errors[errors],
                contact.errors[errors] if (errors in contact.errors) else '',
                cls='error')
        )        

    return layout(

        Form(

            Fieldset(
                Legend('Contact Values'),

                Div(
                    
                    P(
                        Label('Email', _for='email'),
                        Input(
                            name='email',
                            id='email',
                            type='text',
                            hx_get=f'/contacts/{contact.id}/email',
                            hx_target='next .error',
                            hx_trigger='change, keyup delay:200ms',
                            placeholder='Email',
                            value=contact.email
                        ),
                        Span(
                            contact.errors['email'] if 'email' in contact.errors else '',
                            cls='error')
                    ),

                    row(label='First Name', id='first_name', value=contact.first, errors='first'),
                    row(label='Last Name',  id='last_name',  value=contact.last,  errors='last'),
                    row(label='Phone',      id='phone',      value=contact.phone, errors='phone'),

                    cls='table rows'
                ),

                Button('Save')
            ),

            action=f'/contacts/{contact.id}/edit',
            method='post'
        ),

        Button(
            'Delete Contact',
            hx_delete=f'/contacts/{contact.id}',
            hx_push_url='true',
            hx_confirm='Are you sure you want to delete this contact?',
            hx_target='body'
        ),

        P(A('Back', href='/contacts'))
    )

@app.route('/contacts/{contact_id}/edit', methods=['GET'])
def contacts_edit_get(contact_id: int = 0):
    contact = Contact.find(contact_id)
    return template_edit(contact)

# @app.route("/contacts/<contact_id>/edit", methods=["GET"])
# def contacts_edit_get(contact_id=0):
#     contact = Contact.find(contact_id)
#     return render_template("edit.html", contact=contact)

# ---------------------------------------------------------
@app.route('/contacts/{contact_id}/edit', methods=['POST'])
async def contacts_edit_post(request: Request, contact_id: int = 0):

    # print('/contacts/{contact_id}/edit POST')

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
        return RedirectResponse(url=f'/contacts/{contact_id}')
    else:
        # print('calling template_edit')
        return template_edit(c)

# @app.route("/contacts/<contact_id>/edit", methods=["POST"])
# def contacts_edit_post(contact_id=0):
#     c = Contact.find(contact_id)
#     c.update(request.form['first_name'], request.form['last_name'], request.form['phone'], request.form['email'])
#     if c.save():
#         flash("Updated Contact!")
#         return redirect("/contacts/" + str(contact_id))
#     else:
#         return render_template("edit.html", contact=c)
# ---------------------------------------------------------

@app.route('/contacts/{contact_id}/email', methods=['GET'])
def contacts_email_get(email: str, contact_id: int = 0):

    # form_data = await request.form()

    c = Contact.find(contact_id)
    # c.email = request.args.get('email')
    c.email = email
    c.validate()
    return c.errors.get('email') or ""

# @app.route("/contacts/<contact_id>/email", methods=["GET"])
# def contacts_email_get(contact_id=0):
#     c = Contact.find(contact_id)
#     c.email = request.args.get('email')
#     c.validate()
#     return c.errors.get('email') or ""

# ---------------------------------------------------------
@app.route('/contacts/{contact_id}', methods=['DELETE'])
def contacts_delete(request: Request, contact_id: int = 0):
    contact = Contact.find(contact_id)
    contact.delete()
    if request.headers.get('HX-Trigger') == 'delete-btn':
        # flash("Deleted Contact!")
        print('Deleted Contact!')
        return RedirectResponse(url='/contacts', status_code=303)
    else:
        return ''

# print(to_xml(
#     str(contacts_delete).format(contact_id=123)
# ))

# @app.route("/contacts/<contact_id>", methods=["DELETE"])
# def contacts_delete(contact_id=0):
#     contact = Contact.find(contact_id)
#     contact.delete()
#     if request.headers.get('HX-Trigger') == 'delete-btn':
#         flash("Deleted Contact!")
#         return redirect("/contacts", 303)
#     else:
#         return ""
# ---------------------------------------------------------



@app.route('/contacts', methods=['DELETE'])
async def contacts_delete_all(request: Request):
        
    form_data: starlette.datastructures.FormData = await request.form()

    contact_ids = form_data.getlist('selected_contact_ids')

    contact_ids = list(map(int, contact_ids))

    for id in contact_ids:
        contact = Contact.find(id)
        contact.delete()

    # flash("Deleted Contacts!")

    print('Deleted Contacts!')

    contacts_set = Contact.all()

    return template_index(None, contacts_set)

# @app.route("/contacts/", methods=["DELETE"])
# def contacts_delete_all():
#     contact_ids = list(map(int, request.form.getlist("selected_contact_ids")))
#     for contact_id in contact_ids:
#         contact = Contact.find(contact_id)
#         contact.delete()
#     flash("Deleted Contacts!")
#     contacts_set = Contact.all(1)
#     return render_template("index.html", contacts=contacts_set)
# ---------------------------------------------------------

# # ===========================================================
# # JSON Data API
# # ===========================================================

@app.route("/api/v1/contacts", methods=['GET'])
def json_contacts():
    contacts_set = Contact.all()
    return {"contacts": [c.__dict__ for c in contacts_set]}

# @app.route("/api/v1/contacts", methods=["GET"])
# def json_contacts():
#     contacts_set = Contact.all()
#     return {"contacts": [c.__dict__ for c in contacts_set]}
# ---------------------------------------------------------

@app.route("/api/v1/contacts", methods=['POST'])
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

# @app.route("/api/v1/contacts", methods=["POST"])
# def json_contacts_new():
#     c = Contact(None, request.form.get('first_name'), request.form.get('last_name'), request.form.get('phone'),
#                 request.form.get('email'))
#     if c.save():
#         return c.__dict__
#     else:
#         return {"errors": c.errors}, 400
# ---------------------------------------------------------
@app.route("/api/v1/contacts/{contact_id}", methods=['GET'])
def json_contacts_view(contact_id: int = 0):
    contact = Contact.find(contact_id)
    return contact.__dict__

# @app.route("/api/v1/contacts/<contact_id>", methods=["GET"])
# def json_contacts_view(contact_id=0):
#     contact = Contact.find(contact_id)
#     return contact.__dict__
# ---------------------------------------------------------

@app.route("/api/v1/contacts/{contact_id}", methods=['PUT'])
async def json_contacts_edit(request: Request, contact_id: int = 0):

    print(f'/api/vs/contacts/{contact_id} PUT')

    form_data = await request.form()

    print(f'first_name: {form_data.get('first_name')}')

    c = Contact.find(contact_id)

    print(c)

    c.update(
        first=form_data.get('first_name'),
        last =form_data.get('last_name'),
        phone=form_data.get('phone'),
        email=form_data.get('email')
    )

    if c.save():
        return c.__dict__
    else:
        return {"errors": c.errors}, 400


# @app.route("/api/v1/contacts/<contact_id>", methods=["PUT"])
# def json_contacts_edit(contact_id):
#     c = Contact.find(contact_id)
#     c.update(request.form['first_name'], request.form['last_name'], request.form['phone'], request.form['email'])
#     if c.save():
#         return c.__dict__
#     else:
#         return {"errors": c.errors}, 400
# ---------------------------------------------------------
@app.route("/api/v1/contacts/{contact_id}", methods=['DELETE'])
def json_contacts_delete(contact_id: int = 0):
    contact = Contact.find(contact_id)
    contact.delete()
    return {"success": True}

# @app.route("/api/v1/contacts/<contact_id>", methods=["DELETE"])
# def json_contacts_delete(contact_id=0):
#     contact = Contact.find(contact_id)
#     contact.delete()
#     return jsonify({"success": True})
# ---------------------------------------------------------

# if __name__ == "__main__":
#     app.run()

serve()