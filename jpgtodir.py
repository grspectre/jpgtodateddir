#!-*- coding: utf8 -*-

import argparse
import os
import sys
import imghdr
import exifread
import datetime
import shutil


def main():
    allowed_file_types = ['jpeg', 'tiff']
    path = get_path()
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
                if file_type in allowed_file_types:
                    part_path = process_file(file_path)
                    new_path = os.path.join(path, part_path)
                    new_path = os.path.normpath(new_path)
                    if not os.path.isdir(new_path):
                        os.makedirs(new_path)
                    new_file = os.path.join(new_path, entry.name)
                    if not os.path.exists(new_file):
                        shutil.move(file_path, new_file)


def process_file(img_path):
    time_format = '%Y:%m:%d %H:%M:%S'
    path_format = '%Y/%m/%d'
    default_path = 'unsorted'
    date_tag_name = 'EXIF DateTimeOriginal'
    f = open(img_path, 'rb')
    tags = exifread.process_file(f, stop_tag=date_tag_name)
    tag_keys = tags.keys()
    if date_tag_name not in tag_keys:
        return default_path
    img_datetime = datetime.datetime.strptime(str(tags[date_tag_name]), time_format)
    f.close()
    return img_datetime.strftime(path_format)


def get_path():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    return args.path


def print_error(message):
    sys.stderr.write(message+"\n")


if __name__=='__main__':
    main()