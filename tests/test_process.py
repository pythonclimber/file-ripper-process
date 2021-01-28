import json
import os
import shutil
import unittest

import file_ripper.fileconstants as fc
from file_ripper_process import constants as pc
from file_ripper_process.process import FileRipperProcess

from tests.utils import create_definitions_file


class CreateFileDefinitionsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.json_data = create_definitions_file()
        self._file_name = 'files/definitions.json'
        if not os.path.exists('files'):
            os.mkdir('files')

    def test_valid_definitions_file(self):
        file_name = self.write_file(json.dumps(self.json_data), self._file_name)
        process = FileRipperProcess(file_name)
        self.assertEqual(2, len(process._file_definitions))
        
    def test_invalid_definitions_file(self):
        self.json_data[pc.FILE_DEFINITIONS][0][fc.DELIMITER] = None
        file_name = self.write_file(json.dumps(self.json_data), self._file_name)
        with self.assertRaises(ValueError):
            FileRipperProcess(file_name)

    def write_file(self, file_text, file_name):
        with open(self._file_name, 'wt') as file:
            file.write(file_text)
            return os.path.abspath(self._file_name)

    def tearDown(self) -> None:
        shutil.rmtree('files')
    
# class FileRipperProcessTests(unittest.TestCase):
#     def setUp(self):
#         self.json_data = self.create_file_def_json()
#         self.file_name = 'Valid-09092019.csv'
#         self.definitions_file = 'file_definitions.json'
#         with open(self.file_name, 'w') as file:
#             file.write("Name,Age,DOB\n")
#             file.write("Jason,99,01/01/1970")
#         with open(self.definitions_file, 'w') as file:
#             file.write(json.dumps(self.create_file_defs_json(self.json_data)))
#
#     def test_process_file_definition_given_delimited_file(self):
#         file_definition = FileDefinition.create_from_dict(self.json_data)
#         data_sender = MagicMock()
#         file_mover = MagicMock()
#         process_file_definition(file_definition, data_sender, file_mover)
#         data_sender.assert_called_once()
#         file_mover.assert_called_once()
#
#     def test_execute_process(self):
#         file_processor = MagicMock()
#         execute_process(self.definitions_file, file_processor)
#         file_processor.assert_called_once()
#
#     def tearDown(self):
#         try:
#             if self.file_name:
#                 os.remove(self.file_name)
#             if self.definitions_file:
#                 os.remove(self.definitions_file)
#         except Exception as ex:
#             print(ex)
#
#     @staticmethod
#     def create_file_def_json():
#         return {
#             fc.FILE_MASK: 'Valid-*.csv',
#             fc.FILE_TYPE: fc.DELIMITED,
#             fc.DELIMITER: ',',
#             fc.HAS_HEADER: True,
#             fc.INPUT_DIRECTORY: os.getcwd(),
#             fc.FIELD_DEFINITIONS: [
#                 {fc.FIELD_NAME: 'name'},
#                 {fc.FIELD_NAME: 'age'},
#                 {fc.FIELD_NAME: 'dob'}
#             ]
#         }
#
#     @staticmethod
#     def create_file_defs_json(file_def):
#         return {
#             pc.FILE_DEFINITIONS: [
#                 file_def
#             ]
#         }
