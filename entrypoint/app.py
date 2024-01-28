import cgi
import json
import os
import pprint
from io import BytesIO
from json import loads
from datetime import datetime
import tempfile
import boto3

from chalice import Chalice, AuthResponse
from chalice.app import AuthRequest

from file_ripper import rip_file, FileDefinition

app = Chalice(app_name='entrypoint')
s3_bucket = f'entrypoint-file-storage-{os.environ["environment"]}'


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


def build_file_name():
    current_timestamp = int(round(datetime.now().timestamp() * 1000))
    file_extension = app.current_request.json_body['fileExtension']
    file_definition_id = app.current_request.json_body['fileDefinitionId']
    return f'{file_definition_id}|{current_timestamp}.{file_extension}'


@app.authorizer()
def authorizer(auth_request: AuthRequest):
    print(auth_request.token)
    return AuthResponse(routes=['*'], principal_id='user')


@app.route('/upload-data', methods=['POST'], content_types=['application/json'], authorizer=authorizer)
def upload_data():
    try:
        file_contents = app.current_request.json_body['fileContents']
        file_name = build_file_name()

        boto3.client('s3').put_object(
            Body=file_contents,
            Bucket=s3_bucket,
            Key=file_name
        )

        return {
            "message": "Success",
            "fileNameWithTimestamp": file_name
        }
    except Exception as err:
        return {
            "message": f"Error encountered: {err}",
            "fileNameWithTimestamp": None,
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

    pprint.pprint(json.dumps(file_definition))

    with tempfile.TemporaryDirectory() as tempdir:
        os.chdir(tempdir)
        _create_file(file_data)

        with open('current_file.txt', 'rt') as file:
            file_instance = rip_file(file, FileDefinition.create_from_dict(file_definition))
            print(f'file_instance: {len(file_instance)}')

    return file_instance.to_dict()
