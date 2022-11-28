from src.mextalki.utils.coupons import set_used_coupon, set_used_credits
from src.mextalki.utils.event_time_slots import (
    redeem_purchased_conversation_club_seats,
    redeem_purchased_lesson_hours,
    redeem_purchased_practice_hours,
    return_event_time_or_slot,
)
from src.mextalki.utils.get_comment_by_id import get_comment_by_id
from src.mextalki.utils.get_common_video_by_uid import (
    get_video_by_uid,
    get_video_score_by_user,
)
from src.mextalki.utils.get_event_type_by_uid import get_event_type_by_uid
from src.mextalki.utils.get_plan_by_uid import get_plan_by_uid
from src.mextalki.utils.get_podcast_by_uid import (
    get_podcast_by_uid,
    get_podcast_video_score_by_user,
)
from src.mextalki.utils.get_post_by_uid import get_post_by_uid
from src.mextalki.utils.get_request_payload import get_request_payload
from src.mextalki.utils.get_teacher_by_uid import get_teacher_by_uid
from src.mextalki.utils.get_user_by_referral_code import (
    get_user_by_referral_code,
    get_user_by_slug,
)
from src.mextalki.utils.get_user_by_uid import get_user_by_uid
from src.mextalki.utils.lesson_exp_points import (
    redeem_lesson_exp_points,
    redeem_points,
    remove_lesson_exp_points,
)
from src.mextalki.utils.send_purchase_hours_email import send_purchase_hours_email
from src.mextalki.utils.send_reminder_email import send_reminder
from src.mextalki.utils.chat import reset_unread_messages, show_unread_messages
