//to change event title
const eventTitle = document.getElementById('EventTitle');

eventTitle.addEventListener('blur', function() {
    const eventID = window.location.pathname.split("/").pop();
    $.ajax({
        headers: {"X-CSRFToken": CSRF_TOKEN},
        type: "POST",
        url:   "change_event_title/",
        data: { "new_title": eventTitle.innerText , "event_id": eventID },
    }).success(function (){
        alert('Event title changed!');
    }).fail(function () {
        alert('Failed to change event title!');
    });
});


//to change event description
const eventDescription = document.getElementById('EventDescription');

eventDescription.addEventListener('blur', function() {
    const eventID = window.location.pathname.split("/").pop();
    $.ajax({
        headers: {"X-CSRFToken": CSRF_TOKEN},
        type: "POST",
        url:   "change_event_description/",
        data: { "new_description": eventDescription.innerText , "event_id": eventID },
    }).success(function (){
        alert('Event description changed!');
    }).fail(function () {
        alert('Failed to change event Description');
    });
});


