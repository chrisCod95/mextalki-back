import logging
from django.utils.text import slugify
from src.mextalki.models import Podcast

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()


def run():
    podcasts = Podcast.objects.all()
    for podcast in podcasts:
        logger.info(podcast)
        logger.info(podcast.title)
        logger.info(slugify(podcast.title))
        podcast.slug = slugify(podcast.title)
        podcast.save()
