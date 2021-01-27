import sys
import unittest
from time import sleep
import click

from .process import execute_process


@click.command()
@click.option('-t', '--time_interval', 'time_interval', required=True, type=int,
              help='Number of minutes to wait between each iteration of the process')
@click.option('-fdp', '--file_definitions_path', 'file_definitions_path', required=True, type=str,
              help='Absolute path to file definitions stored as valid JSON')
def file_ripper_process(time_interval, file_definitions_path):
    try:
        while True:
            execute_process(file_definitions_path)
            sleep(time_interval * 60)
    except KeyboardInterrupt:
        print('Stopping file_ripper_process....')


if __name__ == "__main__":
    file_ripper_process()
