
from fasthtml.common import *

from template_layout import layout

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
