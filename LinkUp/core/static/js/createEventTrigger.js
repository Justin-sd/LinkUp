
function validateCreateEventForm() {

    const eventStartDate = new Date($("#id_potential_start_date").val());
    const eventEndDate = new Date($("#id_potential_end_date").val());
    const eventDuration = $("#id_duration").val();  //In hours?

    //get number of milliseconds since Unix Epoch in local time.
    const eventStart =  eventStartDate.getTime() + (eventStartDate.getTimezoneOffset()*60000);
    const eventEnd = eventEndDate.getTime() + (eventEndDate.getTimezoneOffset()*60000);
    todayTime = Date.now();

    let validationStatus = true;
    if (eventStart >= eventEnd) {
        $("#id_potential_start_date").after("<div><p class='has-text-danger'>Potential start date must be before potential end date.</p></div>");
        validationStatus = false;
    }
    if (eventStart < todayTime) {
        const errorMessage = "<div><p class='has-text-danger'>startDate:" + eventStart + "current time: " + todayTime + " unparsed date: " + $("#id_potential_start_date").val() +"</p></div>"
        $("#id_potential_start_date").after(errorMessage);
        validationStatus = false;
    }
    if (eventEnd < todayTime ) {
        $("#id_potential_end_date").after("<div><p class='has-text-danger'>Potential end date must be in the future.</p></div>");
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