$(function () {
    let isMouseDown = false;
    let idx;
    let firstIdx;
    let lastIdx;
    let strtTime;
    let endTime;

    $("#calendar_table td")
        .mousedown(function () {
            isMouseDown = true;
            idx = $(this).index();
            firstIdx = $(this).closest("tr").index();
            $(this).toggleClass("busy-time");
            $(this).toggleClass("free-time");
            return false;
        })
        .mouseover(function () {
            if (isMouseDown && ($(this).index() === idx) ) {
                $(this).toggleClass("busy-time");
                $(this).toggleClass("free-time");
                lastIdx = $(this).closest("tr").index();
            }
        });

    $(document)
        .mouseup(function () {
            isMouseDown = false;
            strtTime = convert(firstIdx);
            endTime = convert(lastIdx);

            //Reset values
            firstIdx = -1;
            lastIdx = -1;
        });
});
