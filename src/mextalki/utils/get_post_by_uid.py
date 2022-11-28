from src.mextalki.models import Post


def get_post_by_uid(post_uid):
    try:
        return Post.objects.get(pk=post_uid)
    except Post.DoesNotExist:
        return None
