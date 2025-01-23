
from fasthtml.common import *

# from flask import flash

from contacts_model import Contact

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

@app.route('/')
def index():
    return RedirectResponse(url='/contacts')

import route_contacts_get
import route_contacts_archive_post
import route_contacts_archive_get
import route_contacts_archive_file_get
import route_contacts_archive_delete
import route_contacts_count_get
import route_contacts_new_get
import route_contacts_new_post
import route_contacts_id_get
import route_contacts_id_edit_get
import route_contacts_id_edit_post
import route_contacts_id_email_get
import route_contacts_id_delete
import route_contacts_delete
import route_api_v1_contacts_get
import route_api_v1_contacts_post
import route_api_v1_contacts_id_get
import route_api_v1_contacts_id_put
import route_api_v1_contacts_id_delete

route_contacts_get.ar.to_app(app)
route_contacts_archive_post.ar.to_app(app)
route_contacts_archive_get.ar.to_app(app)
route_contacts_archive_file_get.ar.to_app(app)
route_contacts_archive_delete.ar.to_app(app)
route_contacts_count_get.ar.to_app(app)
route_contacts_new_get.ar.to_app(app)
route_contacts_new_post.ar.to_app(app)
route_contacts_id_get.ar.to_app(app)
route_contacts_id_edit_get.ar.to_app(app)
route_contacts_id_edit_post.ar.to_app(app)
route_contacts_id_email_get.ar.to_app(app)
route_contacts_id_delete.ar.to_app(app)
route_contacts_delete.ar.to_app(app)
route_api_v1_contacts_get.ar.to_app(app)
route_api_v1_contacts_post.ar.to_app(app)
route_api_v1_contacts_id_get.ar.to_app(app)
route_api_v1_contacts_id_put.ar.to_app(app)
route_api_v1_contacts_id_delete.ar.to_app(app)

serve()