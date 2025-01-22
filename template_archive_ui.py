
from fasthtml.common import *

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
