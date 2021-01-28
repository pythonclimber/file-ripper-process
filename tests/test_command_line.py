import json
import os
import shutil
from unittest import TestCase

from tests.utils import create_definitions_file


class CommandLineTests(TestCase):
    def setUp(self) -> None:
        self.error_result = 512
        self.success_result = 256
        if not os.path.exists('files'):
            os.mkdir('files')
            os.mkdir('files/delimited')
            os.mkdir('files/fixed')
        with open(f'files/definitions.json', 'w') as file:
            file.write(json.dumps(create_definitions_file()))

    def test_call_with_no_args(self):
        result = os.system('python -m file_ripper_process')
        assert result == self.error_result

    def test_call_with_missing_time_interval(self):
        result = os.system('python -m file_ripper_process -fdp files/definitions.json')
        assert result == self.error_result

    def test_call_with_missing_definitions_path(self):
        result = os.system('python -m file_ripper_process -t 5')
        assert result == self.error_result

    def tearDown(self) -> None:
        shutil.rmtree('files')
