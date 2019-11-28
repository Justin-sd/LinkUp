
function validateCreateEventForm() {

    /*
    let eventStartTime = new Date($("#id_no_earlier_than").val());
    let eventEndTime = $("#id_no_later_than").val();
    const eventStartTimeHour = eventStartTime.getHour();
    const eventEndTimeHour = eventEndTime.getHours();
    const eventStartTimeMin = eventStart.getMinutes();
    const eventEndTimeMin = eventEndDate.getMinutes();
    eventStartTime = eventStartTimeHour + eventStartTimeMin;
    eventEndTime = eventEndTimeHour + eventEndTimeMin;
     */

    //start and end times as DATE object
    const eventStartDate = new Date($("#id_potential_start_date").val());
    const eventEndDate = new Date($("#id_potential_end_date").val());
    const eventDuration = $("#id_duration").val();  //In hours?

    //get number of milliseconds since Unix Epoch in local time.
    const eventStartMil =  eventStartDate.getTime() + (eventStartDate.getTimezoneOffset()*60000);
    const eventEndMil = eventEndDate.getTime() + (eventEndDate.getTimezoneOffset()*60000);
    todayTime = Date.now();

    let eventStartTime = $("#id_no_earlier_than").val();
    let eventEndTime = $("#id_no_later_than").val();
    const eventStartTimeHour = parseInt(eventStartTime.substring(0, 2));
    const eventEndTimeHour = parseInt(eventEndTime.substring(0, 2));
    const eventStartTimeMin = parseInt(eventStartTime.substring(3, 5)) / 60;
    const eventEndTimeMin = parseInt(eventEndTime.substring(3, 5)) / 60;
    eventStartTime = eventStartTimeHour + eventStartTimeMin;
    eventEndTime = eventEndTimeHour + eventEndTimeMin;

    let validationStatus = true;
    if (eventStartMil > eventEndMil) {
        $("#id_potential_start_date").after("<div><p class='has-text-danger'>Potential start date must be before potential end date.</p></div>");
        validationStatus = false;
    }
    if (eventStartMil < todayTime) {
        const errorMessage = "<div><p class='has-text-danger'>startDate:" + eventStartMil + "current time: " + todayTime + " unparsed date: " + $("#id_potential_start_date").val() +"</p></div>"
        $("#id_potential_start_date").after("<div><p class='has-text-danger'>Potential start date must be in the future</p></div>");
        validationStatus = false;
    }
    if (eventEndMil < todayTime ) {
        $("#id_potential_end_date").after("<div><p class='has-text-danger'>Potential end date must be in the future.</p></div>");
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