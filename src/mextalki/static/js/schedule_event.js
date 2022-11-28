function isCalendlyEvent(e) {
  return e.data.event && e.data.event.indexOf('calendly') === 0;
}
function getEventId(url){
    try {
        return url.split('/')[4]
    } catch (e){
        console.error(e);
        return ''
    }
}
function getInviteeId(url){
    try {
        return url.split('/')[6]
    } catch (e){
        return ''
    }
}

function scheduleEvent(payload){
    let {event, invitee} = payload;
    const csrf_token = Cookies.get('csrftoken');
    let eventId = getEventId(event.uri);
    let inviteeId = getInviteeId(invitee.uri);
    let data = {
        'event_id': eventId,
        'invitee_id': inviteeId,
    }
    $.ajax({
        method: 'post',
        url: event_url,
        headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        dataType: "json",
        data: JSON.stringify(data),
        success: function () {
            setTimeout(
                function() {
                    window.location.href = redirectUrl;
                }, 1500
            )
        }
    });
}

$(function () {
    let scheduleButton = $('.schedule_button');
    scheduleButton.click(function () {
        let self = $(this);
        let calendarUrl = self.data('calendar-url');
        event_url = self.data('schedule-url');
        Calendly.initPopupWidget({
            url: calendarUrl,
            prefill: {
                name: username,
                email: user_email,
            }
        });
    })
});

window.addEventListener(
  'message',
  function(e) {
    if (isCalendlyEvent(e)) {
      let { event, payload } = e.data;
      console.log(e);
      if (event === 'calendly.event_scheduled'){
        scheduleEvent(payload);
      }
    }
  }
);
