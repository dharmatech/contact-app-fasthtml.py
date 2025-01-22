
from fasthtml.common import *

from fasthtml.components import All_caps, Sub_title

def layout(*content):

    return Main(
        Header(
            H1(
                All_caps('contacts.app'),
                Sub_title('A Demo Contacts Application')
                )
            ),        

        # [Div(message, cls='flash') for message in flask.get_flashed_messages()],

        Script('htmx.config.methodsThatUseUrlParams = ["get"];'),
        
        *content
    )