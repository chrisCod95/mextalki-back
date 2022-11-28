 $(".courses-button").hover(
    function() {
        $(".courses-submenu").show();
        $(".courses-submenu").hover(
            function () {
                $(".courses-submenu").show();
            },
            function() {
                $(".courses-submenu").hide();
            }
        );
    },
    function() {
        $(".courses-submenu").hide();
    }
);

const announcements = $(".announcement-link");

announcements.each(function ( index ) {
    if( !localStorage.getItem($(this).text()) ) {
        $(this).append(
            " <span class='badge badge-success new-announcement' style='font-size: 8px;'>New</span>"
        )
    }
})

const newAnnouncements = $(".new-announcement").length;

if( newAnnouncements ) {
    $(`<span class=\"unread-badge\">${newAnnouncements}</span>`).insertBefore(".announcements-icon");
}

const newReminders = $(".reminder-link").length;
if( newReminders ) {
    $(`<div class=\"unread-badge\">${newReminders}</div>`).insertBefore(".reminders-icon");
}
