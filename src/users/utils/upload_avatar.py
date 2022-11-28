import os

from src.mextalki.models.utils import hash_file


def upload_avatar_to(instance, filename):
    file = instance.avatar
    file.open()
    file_ext = os.path.splitext(filename)[1]
    file_path = 'avatar/'

    return '{path}{file_name}{file_ext}'.format(
        path=file_path,
        file_name=hash_file(file),
        file_ext=file_ext,
    )
