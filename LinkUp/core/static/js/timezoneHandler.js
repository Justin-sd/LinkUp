function setUserTimeZone(userTimeZone) {
    const data = {"time_zone": userTimeZone};
    $.ajax({
        headers: {"X-CSRFToken": CSRF_TOKEN},
        type: "POST",
        url: "update_timezone/",
        data: data,
    }).done(function(data) {
        // Pass
    });
}

function getBrowserTimeZone() {
    return Intl.DateTimeFormat().resolvedOptions().timeZone;
}

$(document).ready(function () {
    const userTimeZone = getBrowserTimeZone();
    setUserTimeZone(userTimeZone);
});

