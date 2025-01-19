
from fasthtml.common import *

from fasthtml.components import All_caps, Sub_title

# from flask import (
#     Flask, 
#     # redirect,
#     render_template, 
#     # request, 
#     flash, jsonify, send_file
# )

from contacts_model import Contact, Archiver

import time

Contact.load_db()

# ========================================================
# Flask App
# ========================================================

# app = Flask(__name__)

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

# app.secret_key = b'hypermedia rocks'
# ---------------------------------------------------------
# @rt('/')
@app.route('/')
def index():
    # return 'abc'
    return RedirectResponse(url='/contacts')

# @app.route("/")
# def index():
#     return redirect("/contacts")
# ---------------------------------------------------------
def layout(*content):

    return Main(
        Header(
            H1(
                All_caps('contacts.app'),
                Sub_title('A Demo Contacts Application')
                )
            ),        

        # [Div(message, cls='flash') for message in flask.get_flashed_messages()],
        
        *content
    )
# ---------------------------------------------------------
def template_archive_ui(archiver):
    return Div(

        Button('Download Contact Archive', hx_post='/contacts/archive')
        if archiver.status() == 'Waiting'

        else
        Div(
            'Creating Archive...',

            Div(
                Div(
                    Div(
                        id='archive-progress',
                        cls='progress-bar',
                        style=f'width: {archiver.progress() * 100}%'
                    )
                ),

                cls='progress'
            ),

            hx_get='/contacts/archive',
            hx_trigger='load delay:500ms'
        )
        if archiver.status() == 'Running'

        else
        A(
            'Archive Downloading!  Click here if the download does not start.',
            hx_boost='false',
            href='/contacts/archive/file',
            _='on load click() me'
        )
        if archiver.status() == 'Complete'
        else
        Div(),
        
        id='archive-ui',
        hx_target='this',
        hx_swap='outerHTML'
    )

def template_index(q, contacts_set):
    return layout(

        template_archive_ui(Archiver.get()),

        Form(
            
            Label('Search Term', _for='search'),

            Input(
                id='search',
                type='search',
                name='q',
                value=q or '',
                hx_get='/contacts',
                hx_trigger='tbody',
                hx_push_url='true',
                hx_indicator='#spinner'
            ),

            Img(
                style='height: 20px',
                id='spinner',
                cls='htmx-indicator',
                src='/static/img/spinning-circles.svg'
            ),

            Input(type='submit', value='Search'),

            action='/contacts',
            method='get',
            cls='tool-bar',
            enctype=False
        ),

        Form(

            Template(

                Div(
                    Slot(x_text='selected.length'),
                    'contacts selected',

                    Button(
                        'Delete',
                        type='button',
                        cls='bad bg color border',

                        **{
                            '@click' : NotStr("confirm(`Delete ${selected.length} contacts?`) && htmx.ajax('DELETE', '/contacts', { source: $root, target: document.body })")
                        }
                    ),

                    Hr(aria_orientation='vertical'),

                    Button(
                        'Cancel',
                        type='button',
                        **{ '@click' : 'selected = []' }
                    ),

                    cls='box info tool-bar flxed top'
                ),

                x_if='selected.length > 0'

            ),

            Table(
                Thead(
                    Tr(
                        Th(), Th('First'), Th('Last'), Th('Phone'), Th('Email'), Th()
                    )
                ),
                Tbody(            
                    *[
                        Tr(
                            Td(
                                Input(
                                    type='checkbox',
                                    name='selected_contact_ids',
                                    value=contact.id,
                                    x_model='selected'
                                    )
                            ),
                            Td(contact.first),
                            Td(contact.last),
                            Td(contact.phone),
                            Td(contact.email),
                            Td(
                                Div(
                                    Button(
                                        'Options',
                                        type='button',
                                        aria_haspopup='menu',
                                        aria_controls=f'contact-menu-{contact.id}'
                                    ),

                                    Div(
                                        A('Edit', role='menuitem', href=f'/contacts/{contact.id}/edit'),
                                        A('View', role='menuitem', href=f'/contacts/{contact.id}'),
                                        A('Delete', role='menuitem', href='#',
                                        hx_delete=f'/contacts/{contact.id}',
                                        hx_confirm='Are you sure you want to delete this contact?',
                                        hx_swap='outerHTML swap:1s',
                                        hx_target='closest tr'),

                                        role='menu',
                                        hidden_id=f'contact-menu-{contact.id}'),

                                    data_overflow_menu=True)))
                    
                        for contact in contacts_set
                        

                        # Tr(Td('abc')),
                        # Tr(Td('bcd'))
                    ]
                )
            ),
            
            Button(
                'Delete Selected Contacts',
                hx_delete='/contacts',
                hx_confirm='Are you sure you want to delete these contacts?',
                hx_target='body'
            ),

            x_data='{ selected: [] }'
        ),

        P(
            A('Add Contact', href='/contacts/new'),
            Span(

                Img(
                    id='spinner',
                    style='height: 20px',
                    cls='htmx-indicator',
                    src='/static/img/spinning-circles.svg'
                ),

                hx_get='/contacts/count',
                hx_trigger='revealed'
            )
        )
    
    )
    
@app.route("/contacts")
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
   
    # if search is not None:
    #     contacts_set = Contact.search(search)
    #     if request.headers.get('HX-Trigger') == 'search':
    #         return render_template("rows.html", contacts=contacts_set)
    # else:
    #     contacts_set = Contact.all()
    # return render_template("index.html", contacts=contacts_set, archiver=Archiver.get())
# ---------------------------------------------------------
@app.route("/contacts/archive", methods=['POST'])
def start_archive():

    archiver = Archiver.get()
    archiver.run()
    return template_archive_ui(archiver)

# @app.route("/contacts/archive", methods=["POST"])
# def start_archive():
#     archiver = Archiver.get()
#     archiver.run()
#     return render_template("archive_ui.html", archiver=archiver)
# ---------------------------------------------------------

@app.route("/contacts/archive", methods=['GET'])
def archive_status():

    archiver = Archiver.get()
    return template_archive_ui(archiver)

# @app.route("/contacts/archive", methods=["GET"])
# def archive_status():
#     archiver = Archiver.get()
#     return render_template("archive_ui.html", archiver=archiver)
# ---------------------------------------------------------
@app.route("/contacts/archive/file", methods=['GET'])
def archive_content():
    archiver = Archiver.get()
    # return send_file(archiver.archive_file(), "archive.json", as_attachment=True)
    return 'send_file'

# @app.route("/contacts/archive/file", methods=["GET"])
# def archive_content():
#     archiver = Archiver.get()
#     return send_file(archiver.archive_file(), "archive.json", as_attachment=True)
# ---------------------------------------------------------
@app.route("/contacts/archive", methods=['DELETE'])
def reset_archive():

    archiver = Archiver.get()
    archiver.reset()
    return template_archive_ui(archiver)

# @app.route("/contacts/archive", methods=["DELETE"])
# def reset_archive():
#     archiver = Archiver.get()
#     archiver.reset()
#     return render_template("archive_ui.html", archiver=archiver)
# ---------------------------------------------------------

@app.route("/contacts/count", methods=['GET'])
def contacts_count():
    count = Contact.count()
    return "(" + str(count) + " total Contacts)"

# @app.route("/contacts/count")
# def contacts_count():
#     count = Contact.count()
#     return "(" + str(count) + " total Contacts)"
# ---------------------------------------------------------
def template_new(contact):

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
                    
                    row(label='Email',      id='email',      value=contact.email, errors='email'),
                    row(label='First Name', id='first_name', value=contact.first, errors='first'),
                    row(label='Last Name',  id='last_name',  value=contact.last,  errors='last'),
                    row(label='Phone',      id='phone',      value=contact.phone, errors='phone'),

                    cls='table rows'
                ),

                Button('Save')
            ),

            action='/contacts/new',
            method='post'
        ),

        P(A('Back', href='/contacts'))
    )

@app.route("/contacts/new", methods=['GET'])
def contacts_new_get():

    print('/contacts/new GET')

    return template_new(contact=Contact())

# @app.route("/contacts/new", methods=['GET'])
# def contacts_new_get():
#     return render_template("new.html", contact=Contact())
# ---------------------------------------------------------
@app.route('/contacts/new', methods=['POST'])
async def contacts_new(request: Request):

    print('/contacts/new POST')

    print(request)

    print(request.form)

    # print(request.form().get('first_name'))

    print('calling request.form()')

    form_data = await request.form()

    # print(f"first_name: {form_data.get('first_name')}")
    
    c = Contact(
        id_=None,
        # first=request.form['first_name'],
        # last=request.form['last_name'],
        # phone=request.form['phone'],
        # email=request.form['email']

        first=form_data.get('first_name'),
        last =form_data.get('last_name'),
        phone=form_data.get('phone'),
        email=form_data.get('email')
    )


    if c.save():
        print('Created New Contact!')

        # flash('Created New Contact!')

        # return redirect('/contacts')

        return RedirectResponse(url='/contacts')
    else:
        print('calling template_new')
        return template_new(c)


# @app.route("/contacts/new", methods=['POST'])
# def contacts_new():
#     c = Contact(None, request.form['first_name'], request.form['last_name'], request.form['phone'],
#                 request.form['email'])
#     if c.save():
#         flash("Created New Contact!")
#         return redirect("/contacts")
#     else:
#         return render_template("new.html", contact=c)
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

@app.route('/contacts/', methods=['DELETE'])
# def contacts_delete_all(selected_contact_ids):
# async def contacts_delete_all(selected_contact_ids: str):
async def contacts_delete_all(request: Request):

    # print(selected_contact_ids)

    form_data = await request.form()

    print(form_data)

    # selected_contact_ids = request.form.getlist("selected_contact_ids")

    # selected_contact_ids = form_data.getlist("selected_contact_ids")
    
    # print(selected_contact_ids)

    # contact_ids = list(map(int, selected_contact_ids))

    # print(contact_ids)

    return ''

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