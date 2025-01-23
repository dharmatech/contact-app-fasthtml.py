
from fasthtml.common import *

from template_layout import layout

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
