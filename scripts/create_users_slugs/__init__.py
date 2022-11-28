import logging
from django.utils.text import slugify
from src.users.models import User

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()


def run():
    users = User.objects.all()
    for user in users:
        logger.info(user)
        logger.info(user.username)
        logger.info(slugify(user.username))
        user.slug = slugify(user.username)
        user.save()
