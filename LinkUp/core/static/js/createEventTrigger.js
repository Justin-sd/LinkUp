
function validateCreateEventForm() {
    const eventDuration = $("#id_duration").val();
    const eventStartDate = Date.parse($("#id_potential_start_date").val());
    const eventEndDate = Date.parse($("#id_potential_end_date").val());
    let eventStartTime = $("#id_no_earlier_than").val();
    let eventEndTime = $("#id_no_later_than").val();
    const eventStartTimeHour = parseInt(eventStartTime.substring(0, 2));
    const eventEndTimeHour = parseInt(eventEndTime.substring(0, 2));
    const eventStartTimeMin = parseInt(eventStartTime.substring(3, 5)) / 60;
    const eventEndTimeMin = parseInt(eventEndTime.substring(3, 5)) / 60;
    eventStartTime = eventStartTimeHour + eventStartTimeMin;
    eventEndTime = eventEndTimeHour + eventEndTimeMin;

    let validationStatus = true;
    if (eventStartDate > eventEndDate) {
        $("#id_potential_start_date").after("<div><p class='has-text-danger'>Potential start date must be before potential end date.</p></div>");
        validationStatus = false;
    }
    if (eventDuration <= 0) {
        $("#id_duration").after("<div><p class='has-text-danger'>Duration must be greater than 0 minutes.</p></div>");
        validationStatus = false;
    }
    if (eventEndTime - eventStartTime < 1) {
            $("#id_no_earlier_than").after("<div><p class='has-text-danger'>Must be 1 hour or more between start and end time</p></div>");
            validationStatus = false;
    }
    if (validationStatus) {
        modal.style.display = "none";
    }
    return validationStatus;
}