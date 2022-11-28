function convertTZ(date, tzString) {
    return moment.tz(date, tzString);
}

function weekDayDate(indexDay) {
    now = moment().tz("America/Mexico_City");
    if(indexDay < now.weekday()) {
        now.subtract(now.weekday() - indexDay, "d");
    } else {
        now.add(indexDay - now.weekday(), "d");
    }
    return now;
}

$(function () {
    let tableRows = $('.convert-to-tz');
    let userTz = moment.tz.guess()
    tableRows.each(function () {
       let currentRow = $(this);
       let dayDisplay = currentRow.find('#day-display');
       let hourDisplay = currentRow.find('#hour-display');
       let day = dayDisplay.data('day');
       let hour = hourDisplay.data('hour');
       let weekDay = weekDayDate(day);
       let splitHour = hour.split(':');
       weekDay.set({'hour': splitHour[0], 'minute': splitHour[1], 'second':0, 'millisecond':0});
       let userConvertedTime = convertTZ( weekDay.toISOString(), userTz);
       dayDisplay.text(userConvertedTime.format('dddd'));
       hourDisplay.text(userConvertedTime.format('HH:mm'));
    });
    $('.user-timezone').append(`*Your Local Time ${userTz}`);
});



