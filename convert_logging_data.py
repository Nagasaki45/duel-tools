'''
Comvert the DUEL logging data from gzipped XMLs to multiple CSVs,
one per sensor.
'''
import argparse
import csv
import pathlib
import shutil
import xml.etree.ElementTree as ET

import xml_parser


OUT_DIR = pathlib.Path('data')


def get_csv_filepath(session_dir, type_, sensor_name):
    if sensor_name:
        clean_sensor_name = sensor_name.replace('/', '_')
        filename = f'{type_}~{clean_sensor_name}.csv'
    else:
        filename = f'{type_}.csv'
    return session_dir / filename


def convert_session(input_file, output_dir):
    files = {}  # filepath -> file_handler
    try:
        for element in xml_parser.parse(input_file):
            type_ = element.pop('type')
            sensor_name = element.pop('sensorName', None)
            filepath = get_csv_filepath(output_dir, type_, sensor_name)
            if filepath not in files:
                files[filepath] = open(filepath, 'w')
                csv.writer(files[filepath]).writerow(element.keys())
            csv.writer(files[filepath]).writerow(element.values())
    finally:
        for f in files.values():
            f.close()


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('duel_logging_dir',
                        help='Path to the DUEL logging directory')
    return parser.parse_args()


def main():
    args = parse_args()

    duel_logging_dir = pathlib.Path(args.duel_logging_dir)
    assert duel_logging_dir.is_dir(), f'No such directory: {duel_logging_dir}'

    for session_in_dir in duel_logging_dir.iterdir():
        for session_in_file in session_in_dir.glob('*.xio.gz'):
            session_out_dir = OUT_DIR / session_in_file.name.split('.')[0]
            session_out_dir.mkdir()
            print(f'Processing {session_in_file}')
            try:
                convert_session(session_in_file, session_out_dir)
            except ET.ParseError as e:
                print('Invalid XML. Deleting directory and skipping')
                session_out_dir.rmdir()


if __name__ == '__main__':
    main()
