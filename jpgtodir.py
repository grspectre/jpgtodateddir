#!-*- coding: utf8 -*-

import argparse
import os
import sys
import imghdr
import exifread
import datetime
import shutil
import re
from typing import Optional


def main():
    allowed_file_types = ['jpeg', 'tiff']
    allowed_file_ext = ['.mp4', '.ogg']
    path, postfix = get_params()
    # curious bug with path in "" (win10)
    if path[-1] == '"':
        path = path[:-1]
    if not os.path.isdir(path):
        print_error('"%s" path is not directory' % path)
        sys.exit(13)
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                file_path = os.path.join(path, entry.name)
                file_type = imghdr.what(file_path)
                file_ext = os.path.splitext(file_path)[-1]
                if file_type in allowed_file_types or file_ext in allowed_file_ext:
                    part_path = process_file(file_path, postfix)
                    new_path = os.path.join(path, part_path)
                    new_path = os.path.normpath(new_path)
                    if not os.path.isdir(new_path):
                        os.makedirs(new_path)
                    new_file = os.path.join(new_path, entry.name)
                    if not os.path.exists(new_file):
                        shutil.move(file_path, new_file)


def process_file(img_path, postfix):
    print('process {}'.format(img_path))
    time_format = '%Y:%m:%d %H:%M:%S'
    default_path = 'unsorted'
    if postfix is not None:
        default_path += ' ' + postfix
    date_tag_name = 'EXIF DateTimeOriginal'
    f = open(img_path, 'rb')
    tags = exifread.process_file(f, stop_tag=date_tag_name)
    tag_keys = tags.keys()
    if date_tag_name not in tag_keys:
        img_datetime = find_date_in_file_name(img_path)
        return default_path if img_datetime is None else get_output_path(img_datetime, postfix)
    img_datetime = datetime.datetime.strptime(str(tags[date_tag_name]), time_format)
    f.close()
    return get_output_path(img_datetime, postfix)


def get_output_path(dt: datetime.datetime, postfix: str) -> str:
    path_format = '%Y/%m/%Y%m%d'
    output_path = dt.strftime(path_format)
    if postfix is not None:
        output_path += ' ' + postfix
    return output_path


def find_date_in_file_name(path: str) -> Optional[datetime.datetime]:
    params = [
        {'re': re.compile('\d{4}-\d{2}-\d{2}'), 'format': '%Y-%m-%d'},
        {'re': re.compile('\d{2}-\d{2}-\d{4}'), 'format': '%d-%m-%Y'},
        {'re': re.compile('\d{8}'), 'format': '%Y%m%d'},
    ]
    file_name = os.path.split(path)[-1]
    for param in params:
        result = re.findall(param['re'], file_name)
        for date_str in result:
            try:
                return datetime.datetime.strptime(date_str, param['format'])
            except ValueError:
                pass
    return None


def get_params():
    parser = argparse.ArgumentParser(description="Move JPG and TIFF images to dated directory")
    parser.add_argument('source_dir', help="Source directory")
    parser.add_argument('-p', '--postfix', type=str, help="Postfix for dated directory")
    args = parser.parse_args()
    return [args.source_dir, args.postfix]


def print_error(message):
    sys.stderr.write(message+"\n")


if __name__ == '__main__':
    main()
