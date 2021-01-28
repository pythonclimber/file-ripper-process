import os

from file_ripper import fileconstants as fc
from file_ripper_process import constants as pc


def create_definitions_file():
    return {
        pc.FILE_DEFINITIONS: [
            {
                fc.FILE_MASK: 'Valid-*.csv',
                fc.FILE_TYPE: fc.DELIMITED,
                fc.DELIMITER: ',',
                fc.INPUT_DIRECTORY: os.path.join(os.getcwd(), 'files/delimited'),
                fc.COMPLETED_DIRECTORY: os.path.join(os.getcwd(), 'files/delimited/completed'),
                fc.FIELD_DEFINITIONS: [
                    {
                        fc.FIELD_NAME: 'name',
                        fc.POSITION_IN_ROW: 0
                    }
                ]
            },
            {
                fc.FILE_MASK: 'Valid-*.txt',
                fc.FILE_TYPE: fc.FIXED,
                fc.INPUT_DIRECTORY: os.path.join(os.getcwd(), 'files/fixed'),
                fc.COMPLETED_DIRECTORY: os.path.join(os.getcwd(), 'files/fixed/completed'),
                fc.FIELD_DEFINITIONS: [
                    {
                        fc.FIELD_NAME: 'name',
                        fc.START_POSITION: 0,
                        fc.FIELD_LENGTH: 12
                    }
                ]
            }
        ]
    }
