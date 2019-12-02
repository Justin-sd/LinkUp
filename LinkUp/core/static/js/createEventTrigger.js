
function validateCreateEventForm() {
    // Remove old validation messages
    $(".create_event_validation").remove();

    //start and end times as DATE object
    const eventStartDate = new Date();
    let eventStartString = $("#id_potential_start_date").val();
    eventStartString = eventStartString.split("-");

    eventStartDate.setFullYear(parseInt(eventStartString[0], 10), parseInt(eventStartString[1], 10) - 1, parseInt(eventStartString[2], 10));

    //parse end date
    const eventEndDate = new Date();
    let eventEndString = $("#id_potential_end_date").val();
    eventEndString = eventEndString.split("-");
    eventEndDate.setFullYear(eventEndString[0], eventEndString[1], eventEndString[2]);

    const eventDuration = $("#id_duration").val();  //In hours?

    //get number of milliseconds since Unix Epoch in local time.
    const eventStartMil =  eventStartDate.getTime() + (eventStartDate.getTimezoneOffset()*60000);
    const eventEndMil = eventEndDate.getTime() + (eventEndDate.getTimezoneOffset()*60000);
    let todaysDate  = new Date();

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
        $("#id_potential_start_date").after("<div class='create_event_validation'><p class='has-text-danger'>Potential start date must be before potential end date.</p></div>");
        validationStatus = false;
    }

    //Validating potential starting date
    if (eventStartDate.getMonth() < todaysDate.getMonth()) {
        if (eventStartDate.getFullYear() <= todaysDate.getFullYear()) {
        $("#id_potential_start_date").after("<div class='create_event_validation'><p class='has-text-danger'>Potential start date must be in the future.</p></div>");
        validationStatus = false;
        }
    }
    else if ((eventStartDate.getMonth() === todaysDate.getMonth()) && (eventStartDate.getDate() < todaysDate.getDate())) {
        $("#id_potential_start_date").after("<div class='create_event_validation'><p class='has-text-danger'>Potential start date must be in the future.</p></div>");
        validationStatus = false;
    }

    //Validating potential ending date
    if (eventEndDate.getMonth() < todaysDate.getMonth()) {
         if (eventEndDate.getFullYear() <= todaysDate.getFullYear()) {
             $("#id_potential_end_date").after("<div class='create_event_validation'><p class='has-text-danger'>Potential end date must be in the future.</p></div>");
             validationStatus = false;
         }
    }
    else if ((eventEndDate.getMonth() === todaysDate.getMonth()) && (eventEndDate.getDate() < todaysDate.getDate())) {
        $("#id_potential_end_date").after("<div class='create_event_validation'><p class='has-text-danger'>Potential end date must be in the future.</p></div>");
        validationStatus = false;
    }

    if (eventDuration <= 0) {
        $("#id_duration").after("<div class='create_event_validation'><p class='has-text-danger'>Duration must be greater than 0 minutes.</p></div>");
        validationStatus = false;
    }
    if (eventEndTime - eventStartTime < 1) {
            $("#id_no_earlier_than").after("<div class='create_event_validation'><p class='has-text-danger'>Must be 1 hour or more between start and end time</p></div>");
            validationStatus = false;
    }
    
    if (validationStatus) {
        modal.style.display = "none";
    }


    return validationStatus;
}