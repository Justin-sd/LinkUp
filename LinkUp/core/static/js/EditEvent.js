$(document).ready(function(){
    // To change event title
    $('#EventTitle').on('blur', function() {
        const eventID = window.location.pathname.split("/").pop();
        $.ajax({
            headers: {"X-CSRFToken": CSRF_TOKEN},
            type: "POST",
            url:   "change_event_title/",
            data: { "new_title": $('#EventTitle').text(), "event_id": eventID },
        }).success(function (){
            alert('Event title changed!');
        }).fail(function () {
            alert('Failed to change event title!');
        });
    });

    // To change event description
    $('#EventDescription').on('blur', function() {
        const eventID = window.location.pathname.split("/").pop();
        $.ajax({
            headers: {"X-CSRFToken": CSRF_TOKEN},
            type: "POST",
            url:   "change_event_description/",
            data: { "new_description": $('#EventDescription').text() , "event_id": eventID },
        }).success(function (){
            alert('Event description changed!');
        }).fail(function () {
            alert('Failed to change event Description');
        });
    });
});

