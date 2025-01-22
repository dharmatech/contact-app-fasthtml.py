
from fasthtml.common import *

from contacts_model import Archiver

from template_layout import layout

from template_archive_ui import template_archive_ui

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
                                        # A('Edit', role='menuitem', href=str(contacts_edit_get).format(contact_id=contact.id)),
                                        A('View', role='menuitem', href=f'/contacts/{contact.id}'),
                                        A('Delete', role='menuitem', href='#',
                                            hx_delete=f'/contacts/{contact.id}',

                                            # hx_delete=str(contacts_delete).format(contact_id=contact.id),

                                            hx_confirm='Are you sure you want to delete this contact?',
                                            hx_swap='outerHTML swap:1s',
                                            hx_target='closest tr'),

                                        role='menu',
                                        hidden_id=f'contact-menu-{contact.id}'),

                                    data_overflow_menu=True)))
                    
                        for contact in contacts_set
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

            # A('Add Contact', href=contacts_new_get),

            # contacts_new_get.A('Add Contact')

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
