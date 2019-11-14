$(function () {
  let isMouseDown = false;
  let idx;
  let firstIdx;
  let lastIdx;
  let strtTime;
  let endTime;

  $("#calendarTable td")
    .mousedown(function () {
      isMouseDown = true;
      idx = $(this).index();
      firstIdx = $(this).closest("tr").index();
      $(this).toggleClass("highlighted");
      return false;
    })
    .mouseover(function () {
      if (isMouseDown && ($(this).index() === idx) ) {
        $(this).toggleClass("highlighted");
        lastIdx = $(this).closest("tr").index();
      }
    });

  $(document)
    .mouseup(function () {
      isMouseDown = false;
      strtTime = convert(firstIdx);
      endTime = convert(lastIdx);
      if(  (firstIdx !== -1) && (lastIdx !== -1) ) {
        if ( confirm("Confirm: Do you want to set unavailability from: " + strtTime + " to: " + endTime) ) {
            //createUnavailability();
        }
      }
      //Reset values
      firstIdx = -1;
      lastIdx = -1;
    });
});

function convert(idx) {
    switch(idx) {
        case 0:
            return "12:00 am";
        case 1:
            return "12:30 am";
        case 2:
            return "1:00 am";
        case 3:
            return "1:30 am";
        case 4:
            return "2:00 am";
        case 5:
            return "2:30 am";
        case 6:
            return "3:00 am";
        case 7:
            return "3:30 am";
        case 8:
            return "4:00 am";
        case 9:
            return "4:30 am";
        case 10:
            return "5:00 am";
        case 11:
            return "5:30 am";
        case 12:
            return "6:00 am";
        case 13:
            return "6:30 am";
        case 14:
            return "7:00 am";
        case 15:
            return "7:30 am";
        case 16:
            return "8:00 am";
        case 17:
            return "8:30 am";
        case 18:
            return "9:00 am";
        case 19:
            return "9:30 am";
        case 20:
            return "10:00 am";
        case 21:
            return "10:30 am";
        case 22:
            return "11:00 am";
        case 23:
            return "11:30 am";
        case 24:
            return "12:00 pm";
        case 25:
            return "12:30 pm";
        case 26:
            return "1:00 pm";
        case 27:
            return "1:30 pm";
        case 28:
            return "2:00 pm";
        case 29:
            return "2:30 pm";
        case 30:
            return "3:00 pm";
        case 31:
            return "3:30 pm";
        case 32:
            return "4:00 pm";
        case 33:
            return "4:30 pm";
        case 34:
            return "5:00 pm";
        case 35:
            return "5:30 pm";
        case 36:
            return "6:00 pm";
        case 37:
            return "6:30 pm";
        case 38:
            return "7:00 pm";
        case 39:
            return "7:30 pm";
        case 40:
            return "8:00 pm";
        case 41:
            return "8:30 pm";
        case 42:
            return "9:00 pm";
        case 43:
            return "9:30 pm";
        case 44:
            return "10:00 pm";
        case 45:
            return "10:30 pm";
        case 46:
            return "11:00 pm";
        case 47:
            return "11:30 pm";
        default:
            return "null";
    }
}

