from flask import jsonify

MAJOR = 2
MINOR = 0
REVISION = 0

VERSION = '{}.{}.{}'.format(MAJOR, MINOR, REVISION)


def read_version():
    app_version = {
        'app_name': 'Scheduler Manager',
        'app_version': VERSION,
        'major': MAJOR,
        'minor': MINOR,
        'revision': REVISION
    }

    return jsonify(app_version)


if __name__ == '__main__':
    print(VERSION)