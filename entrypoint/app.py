import cgi
from io import BytesIO

from chalice import Chalice

app = Chalice(app_name='entrypoint')


def _get_parts():
    rfile = BytesIO(app.current_request.raw_body)
    content_type = app.current_request.headers['content-type']
    _, parameters = cgi.parse_header(content_type)
    parameters['boundary'] = parameters['boundary'].encode('utf-8')
    parsed = cgi.parse_multipart(rfile, parameters)
    return parsed['file'][0], parsed['fileDefinition'][0]


@app.route(
    '/rip-file',
    methods=['POST'],
    content_types=['multipart/form-data'],
    cors=True
)
def rip_file():
    file_data, file_definition = _get_parts()
    print(file_data)
    print(file_definition)
    return {'hello': 'from rip-files'}
