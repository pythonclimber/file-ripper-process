import json
import logging
import os

from chalice import Chalice
from chalice.app import S3Event
from file_ripper import FileDefinition

logging.getLogger().setLevel('INFO')
app = Chalice(app_name='determine_definition')
definitions_file = os.path.join(os.path.dirname(__file__), 'chalicelib', 'definitions.json')


def find_definition(definition_id: str):
    with open(definitions_file, 'rt') as file:
        definitions = json.load(file)
        for definition in definitions:
            if definition['definitionId'] == definition_id:
                return FileDefinition.create_from_dict(definition)
        else:
            raise ValueError("Invalid definitionId provided.")


@app.on_s3_event(
    os.environ['s3_bucket_name'],
    events=['s3:ObjectCreated:*'])
def handle_s3_event(event: S3Event):
    try:
        definition_id = event.key.split('|')[0]
        definition = find_definition(definition_id)
        logging.info(f'Found definition {definition_id}: {definition}')
    except Exception:
        pass
