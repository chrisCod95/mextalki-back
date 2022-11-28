from typing import Optional

from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.dateparse import parse_datetime
from src.mextalki.models import ScheduledEvent
from src.mextalki.utils.schedule_event import (
    create_event_reminder,
    cancel_event_reminder,
)
from src.mextalki.utils import (
    redeem_lesson_exp_points,
    remove_lesson_exp_points,
    return_event_time_or_slot,
)


def _get_scheduled_event_by_id(provider_event_id: str, invite_uuid: Optional[str] = None) -> Optional[ScheduledEvent]:
    try:
        if invite_uuid:
            return ScheduledEvent.objects.get(
                provider_event_id=provider_event_id,
                provider_invite_id=invite_uuid,
            )
        return ScheduledEvent.objects.get(
            provider_event_id=provider_event_id,
        )
    except ScheduledEvent.DoesNotExist:
        return None


def _get_new_or_rescheduled_event(old_event_uuid: str, event_uuid: str, invite_uuid: str) -> Optional[ScheduledEvent]:
    if old_event_uuid:
        old_scheduled_event: ScheduledEvent = _get_scheduled_event_by_id(old_event_uuid)
        new_scheduled_event = old_scheduled_event
        new_scheduled_event.pk = None
        new_scheduled_event.status = ScheduledEvent.RESCHEDULED
        new_scheduled_event.provider_event_id = event_uuid
        new_scheduled_event.save()
        return new_scheduled_event
    return _get_scheduled_event_by_id(event_uuid, invite_uuid)


def process_scheduled_event(resource):
    old_event_uuid = resource.get('old_event_uuid')
    scheduled_event: ScheduledEvent = _get_new_or_rescheduled_event(
        old_event_uuid=old_event_uuid,
        event_uuid=resource.get('event_uuid'),
        invite_uuid=resource.get('invite_uuid'),
    )
    if not old_event_uuid:
        redeem_lesson_exp_points(
            event_type=scheduled_event.event_type,
            user=scheduled_event.user,
        )
    if old_event_uuid:
        cancel_event_reminder(scheduled_event)
    if scheduled_event:
        scheduled_event.provider_invite_id = resource.get('invite_uuid')
        scheduled_event.start_time = parse_datetime(resource.get('event_start_time'))
        scheduled_event.end_time = parse_datetime(resource.get('event_end_time'))
        scheduled_event.time_zone = resource.get('invite_timezone')
        scheduled_event.location = resource.get('event_location')
        scheduled_event.save()
        create_event_reminder(scheduled_event.user, scheduled_event)
        status_code = HttpResponse.status_code
    else:
        status_code = HttpResponseBadRequest.status_code
    return status_code


def process_canceled_event(resource):
    event_uuid = resource.get('event_uuid')
    new_event_uuid = resource.get('new_event_uuid')
    invite_uuid = resource.get('invite_uuid')
    scheduled_event: ScheduledEvent = _get_scheduled_event_by_id(
        event_uuid, invite_uuid,
    )
    if scheduled_event:
        if not new_event_uuid:
            return_event_time_or_slot(
                scheduled_event=scheduled_event,
                user=scheduled_event.user,
            )
            remove_lesson_exp_points(
                event_type=scheduled_event.event_type,
                user=scheduled_event.user,
            )
        scheduled_event.status = ScheduledEvent.CANCELLED
        scheduled_event.save()
        cancel_event_reminder(scheduled_event)
        status_code = HttpResponse.status_code
    else:
        status_code = HttpResponseBadRequest.status_code
    return status_code
