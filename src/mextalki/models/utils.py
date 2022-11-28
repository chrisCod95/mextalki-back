import hashlib
import os
import uuid
import warnings
from functools import partial


def hash_file(file, block_size=65536):
    hasher = hashlib.md5()
    for buf in iter(partial(file.read, block_size), b''):
        hasher.update(buf)

    return hasher.hexdigest()


def upload_thumbnail_to(instance, filename):
    file = instance.thumbnail
    file.open()
    warnings.warn('Deprecated: use upload_to()', DeprecationWarning)
    return upload_to(instance, filename, file)


def upload_file_to(instance, filename):
    file = instance.file
    file.open()
    warnings.warn('Deprecated: use upload_to()', DeprecationWarning)
    return upload_to(instance, filename, file)


def upload_image_to(instance, filename):
    file = instance.image
    file.open()
    warnings.warn('Deprecated: use upload_to()', DeprecationWarning)
    return upload_to(instance, filename, file)


def upload_to(instance, filename, file):
    file_ext = os.path.splitext(filename)[1]
    file_path = ''
    if instance.file_path:
        file_path = '{file_path}/'.format(
            file_path=instance.file_path,
        )

    return '{path}{file_name}{file_ext}'.format(
        path=file_path,
        file_name=hash_file(file),
        file_ext=file_ext,
    )


def upload_to_v2(instance, filename):
    file_path = ''
    if instance.file_path:
        file_path = instance.file_path
    return '{path}/{file_name}{file_ext}'.format(
        path=file_path,
        file_name=uuid.uuid4(),
        file_ext=os.path.splitext(filename)[1],
    )
