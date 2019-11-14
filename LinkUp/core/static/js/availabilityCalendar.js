$(document).on('click', ".free-time", function() {
        $(this).removeClass("free-time");
        $(this).addClass("busy-time");
});

$(document).on('click', ".busy-time", function() {
        $(this).removeClass("busy-time");
        $(this).addClass("free-time");
});