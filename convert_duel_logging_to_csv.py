'''
Convert the DUEL logging data from gzipped XMLs to multiple CSVs,
one per sensor.
'''
import argparse
import csv
import pathlib
import xml.etree.ElementTree as ET

import xml_parser


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
        for element in xml_parser.parse(input_file):  # gunzip automatically
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
    parser.add_argument('in_dir', help='Path to the DUEL logging directory')
    parser.add_argument('out_dir', help='Path to output directory')
    return parser.parse_args()


def main(in_dir, out_dir):
    '''
    Convert the DUEL logging data from gzipped XMLs to multiple CSVs,
    one per sensor.

    in_dir: Path to DUEL logging directory
    out_dir: Path to output directory
    '''
    in_dir = pathlib.Path(in_dir)
    assert in_dir.is_dir(), f'No such directory: {in_dir}'

    out_dir = pathlib.Path(out_dir)

    for session_in_dir in in_dir.iterdir():
        for session_in_file in session_in_dir.glob('r*.xio.gz'):
            session_out_dir = out_dir / session_in_dir.name
            session_out_dir.mkdir(exist_ok=True, parents=True)
            print(f'Processing {session_in_file} into {session_out_dir}')
            try:
                convert_session(session_in_file, session_out_dir)
            except ET.ParseError as e:
                print('Invalid XML. Deleting directory and skipping')
                session_out_dir.rmdir()


if __name__ == '__main__':
    args = parse_args()
    main(args.in_dir, args.out_dir)
