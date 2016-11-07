import argparse
import json
import os

from setuptools import namespaces


FILENAME = 'danny-hack-nspkg.pth'
VERSION = '0.20.0'
CORE_DIST_INFO = 'google_cloud_core-{}.dist-info'.format(VERSION)
CORE_METADATA = {
    'metadata_version': '2.0',
    'name': 'google-cloud-core',
    'version': VERSION,
}
CURR_DIR = os.path.abspath(os.path.dirname(__file__))
CORE_DIR = os.path.abspath(
    os.path.join(CURR_DIR, '..', 'core'))
EXTRA_PATH_TEMPLATE = (
    'import sys;'
    'mp = sys.modules[{!r}].__path__;'
    'p1 = {!r};'
    '(p1 not in mp) and mp.append(p1);'
    'p2 = {!r};'
    '(p2 not in mp) and mp.append(p2)\n')


def fake_core_dist_info(site_packages):
    """Fake the dist. info of google-cloud-core.

    It needs to be faked since we don't actually install it.
    """
    dist_info = os.path.join(site_packages, CORE_DIST_INFO)
    if not os.path.isdir(dist_info):
        os.mkdir(dist_info)
    meta = os.path.join(dist_info, 'metadata.json')
    if not os.path.exists(meta):
        with open(meta, 'w') as file_obj:
            json.dump(CORE_METADATA, file_obj)


def add_hacked_pth_file(site_packages):
    """Add the hacked .PTH file to the site packages dir."""
    installer = namespaces.Installer()
    part1 = installer._gen_nspkg_line('google')
    part2 = EXTRA_PATH_TEMPLATE.format(
        'google', os.path.join(CORE_DIR, 'google'),
        os.path.join(CURR_DIR, 'google'))
    part3 = installer._gen_nspkg_line('google.cloud')
    part4 = EXTRA_PATH_TEMPLATE.format(
        'google.cloud', os.path.join(CORE_DIR, 'google', 'cloud'),
        os.path.join(CURR_DIR, 'google', 'cloud'))

    file_contents = ''.join([part1, part2, part3, part4])
    full_path = os.path.join(site_packages, FILENAME)
    with open(full_path, 'w') as file_obj:
        file_obj.write(file_contents)


def main(site_packages):
    add_hacked_pth_file(site_packages)
    fake_core_dist_info(site_packages)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Make a hacked PTH file to emulate "setup.py develop"')
    help_txt = 'Site packages directory where .pth file will be added.'
    parser.add_argument('--site-packages', dest='site_packages',
                        required=True, help=help_txt)
    args = parser.parse_args()
    main(args.site_packages)
