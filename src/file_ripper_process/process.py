import json
import os
from datetime import datetime
from glob import glob
from typing import List

from file_ripper import FileDefinition, rip_file

from file_ripper_process import constants as pc
from file_ripper_process.logger import create_logger

logger = create_logger()


def process_file_definition(file_definition, data_exporter_factory):
    os.chdir(file_definition.input_directory)
    data_sender = data_exporter_factory(file_definition.export_definition)
    for file_name in glob(file_definition.file_mask):
        logger.info(f'Processing file {file_name}...')
        with open(file_name, 'r') as file:
            data_sender.export_data(rip_file(file, file_definition))


def create_file_definitions(json_data) -> List[FileDefinition]:
    return [FileDefinition.create_from_dict(file_def) for file_def in json_data[pc.FILE_DEFINITIONS]]


def process_definitions(file_definitions: List[FileDefinition], file_def_processor=process_file_definition):
    for file_def in file_definitions:
        file_def_processor(file_def)


def execute_process(definitions_file_name):
    logger.info(f"Starting file-ripper at {datetime.now().isoformat(' ', timespec='milliseconds')}")
    with open(definitions_file_name, 'r') as file:
        file_definitions = create_file_definitions(json.loads(file.read()))
        process_definitions(file_definitions)
