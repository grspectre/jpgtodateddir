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
                if file_type in allowed_file_types:
                    part_path = process_file(file_path, postfix)
                    new_path = os.path.join(path, part_path)
                    new_path = os.path.normpath(new_path)
                    if not os.path.isdir(new_path):
                        os.makedirs(new_path)
                    new_file = os.path.join(new_path, entry.name)
                    if not os.path.exists(new_file):
                        shutil.move(file_path, new_file)


def process_file(img_path, postfix):
    time_format = '%Y:%m:%d %H:%M:%S'
    path_format = '%Y/%m/%Y%m%d'
    default_path = 'unsorted'
    if postfix is not None:
        default_path += ' ' + postfix
    date_tag_name = 'EXIF DateTimeOriginal'
    f = open(img_path, 'rb')
    tags = exifread.process_file(f, stop_tag=date_tag_name)
    tag_keys = tags.keys()
    if date_tag_name not in tag_keys:
        return default_path
    img_datetime = datetime.datetime.strptime(str(tags[date_tag_name]), time_format)
    f.close()
    output_path = img_datetime.strftime(path_format)
    if postfix is not None:
    	output_path += ' ' + postfix
    return output_path


def get_params():
    parser = argparse.ArgumentParser(description="Move JPG and TIFF images to dated directory")
    parser.add_argument('source_dir', help="Source directory")
    parser.add_argument('-p', '--postfix', type=str, help="Postfix for dated directory")
    args = parser.parse_args()
    return [args.source_dir, args.postfix]


def print_error(message):
    sys.stderr.write(message+"\n")


if __name__=='__main__':
    main()
