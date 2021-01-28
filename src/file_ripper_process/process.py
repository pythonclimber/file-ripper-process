import json
import os
from datetime import datetime
from glob import glob

from file_ripper import FileDefinition, rip_file
from file_ripper_process import constants as pc
from file_ripper_process.logger import create_logger

logger = create_logger()


class DefaultDataExporter:
    def export_data(self, data):
        print(data)


class FileRipperProcess:
    def __init__(self, definitions_file, data_exporter=DefaultDataExporter()):
        self._data_exporter = data_exporter
        with open(definitions_file, 'rt') as file:
            self._file_definitions = self.create_file_definitions(json.loads(file.read()))

    def execute(self):
        logger.info(f"Started file-ripper at {datetime.now().isoformat(' ', timespec='milliseconds')}")
        for file_definition in self._file_definitions:
            self.process_file_definition(file_definition)
        logger.info(f"Finished file-ripper at {datetime.now().isoformat(' ', timespec='milliseconds')}")

    def process_file_definition(self, file_definition):
        os.chdir(file_definition.input_directory)
        for file_name in glob(file_definition.file_mask):
            logger.info(f'Processing file {file_name}...')
            with open(file_name, 'r') as file:
                self._data_exporter.export_data(rip_file(file, file_definition))

    @staticmethod
    def create_file_definitions(json_data):
        return [FileDefinition.create_from_dict(file_def) for file_def in json_data[pc.FILE_DEFINITIONS]]