
function validateCreateEventForm() {
    const eventDuration = $("#id_duration").val();
    const eventStart = Date.parse($("#id_potential_start_date").val());
    const eventEnd = Date.parse($("#id_potential_end_date").val());

    let validationStatus = true;
    if (eventStart >= eventEnd) {
        $("#id_potential_start_date").after("<div><p class='has-text-danger'>Potential start date must be before potential end date.</p></div>");
        validationStatus = false;
    }
    if (eventDuration <= 0) {
        $("#id_duration").after("<div><p class='has-text-danger'>Duration must be greater than 0 minutes.</p></div>");
        validationStatus = false;
    }
    if (validationStatus) {
        modal.style.display = "none";
    }
    return validationStatus;
}