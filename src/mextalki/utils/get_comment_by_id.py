from src.mextalki.models import Comment


def get_comment_by_id(comment_id):
    try:
        return Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return None
