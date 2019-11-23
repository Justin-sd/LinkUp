$(document).ready(function() {
    // Get the modal
    const modal = document.getElementById("createEventModal");

    // Get the button that opens the modal
    const btnCreateEventModal = document.getElementById("btn-open-create-event-modal");

    // Get the <span> element that closes the modal
    const span = document.getElementsByClassName("close")[0];

    // When the user clicks the button, open the modal
    btnCreateEventModal.onclick = function () {
        renderCreateEventForm();
        modal.style.display = "block";
    };

    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    };

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
});

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

        let validationStatus = true;
        if (eventStart >= eventEnd) {
            $("#id_potential_start_date").after("<div><p class='has-text-danger'>Potential start date must be before potential end date.</p></div>");
            validationStatus = false;
        }
        if (eventDuration < 0) {
            $("#id_duration").after("<div><p class='has-text-danger'>Duration must be greater than 0 minutes.</p></div>");
            validationStatus = false;
        }
        if (validationStatus) {
            modal.style.display = "none";
        }
        return validationStatus;
    }