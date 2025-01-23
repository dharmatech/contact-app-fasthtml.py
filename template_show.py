
from fasthtml.common import *

from template_layout import layout

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