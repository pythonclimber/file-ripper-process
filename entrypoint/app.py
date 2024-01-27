import cgi
import os
from io import BytesIO
from json import loads
import tempfile

from chalice import Chalice, AuthResponse
from chalice.app import AuthRequest

from file_ripper import rip_file, FileDefinition

app = Chalice(app_name='entrypoint')


def _get_parts():
    rfile = BytesIO(app.current_request.raw_body)
    content_type = app.current_request.headers['content-type']
    _, parameters = cgi.parse_header(content_type)
    parameters['boundary'] = parameters['boundary'].encode('utf-8')
    parsed = cgi.parse_multipart(rfile, parameters)
    return parsed['file'][0], loads(parsed['fileDefinition'][0])


def _create_file(file_data: bytes):
    with open('current_file.txt', 'wt') as file:
        file_contents = file_data.decode('utf-8')
        print(f'file_contents: {file_contents}')
        file.write(file_contents)


@app.authorizer()
def authorizer(auth_request: AuthRequest):
    print(auth_request.token)
    return AuthResponse(routes=['*'], principal_id='user')


@app.route('/upload-data', methods=['POST'], content_types=['application/json'], authorizer=authorizer)
def upload_data():
    print(type(app.current_request.json_body))
    return {
        "message": "Success"
    }


@app.route(
    '/rip-file',
    methods=['POST'],
    content_types=['multipart/form-data'],
    cors=True,
    authorizer=authorizer
)
def rip_file_web():
    file_data, file_definition = _get_parts()

    with tempfile.TemporaryDirectory() as tempdir:
        os.chdir(tempdir)
        _create_file(file_data)

        with open('current_file.txt', 'rt') as file:
            file_instance = rip_file(file, FileDefinition.create_from_dict(file_definition))
            print(f'file_instance: {len(file_instance)}')

    return file_instance.to_dict()
