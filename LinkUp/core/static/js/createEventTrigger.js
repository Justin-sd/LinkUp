// Get the modal
const modal = document.getElementById("createEventModal");

// Get the button that opens the modal
const btnCreateEventModal = document.getElementById("btn-open-create-event-modal");

// Get the <span> element that closes the modal
const span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btnCreateEventModal.onclick = function() {
    renderCreateEventForm();
    modal.style.display = "block";
};

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
};

function renderCreateEventForm() {
    $.ajax({
        type: "GET",
        url: "/create_event_form/",
    }).success(function (form_content) {
        $("#create-event-body").html(form_content);
    }).fail(function () {
        alert("Failed to load the event form");
    });
}

function validateCreateEventForm() {
    const eventDuration = $("#id_duration").val();
    const eventStart = Date.parse($("#id_potential_start_date").val());
    const eventEnd = Date.parse($("#id_potential_end_date").val());
    console.log(eventDuration, (eventStart), (eventEnd));
}

function createEvent() { // create an event popup when create event button is clicked
    const eventTitle = $("#id_title").val();
    const eventDescription = $("#id_description").val();
    const eventDuration = $("#id_duration").val();
    const eventStart = Date.parse($("#id_potential_start_date").val());
    const eventEnd = Date.parse($("#id_potential_end_date").val());

    const data = {"event_title": eventTitle, "event_description": eventDescription, "event_duration": eventDuration,
                  "event_start": eventStart, "event_end": eventEnd};

    $.ajax({
        headers: {"X-CSRFToken": CSRF_TOKEN},
        type: "POST",
        url: "/create_event/",
        data: data,
    }).success(function (res) {
        if (res === 204) {
            window.location = "/event_page/" + event_id
        } else {
            $("#create-event-body").html(res);
        }
    }).fail(function () {
        alert("Failed to submit the event form");
    });
}


