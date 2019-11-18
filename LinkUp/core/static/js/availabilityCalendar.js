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
      if(  (firstIdx !== -1) && (lastIdx !== -1) && (lastIdx !== firstIdx)) {
        if ( confirm("Confirm: Do you want to set unavailability from: " + strtTime + " to: " + endTime) ) {
            update();
        }
      }
      //Reset values
      firstIdx = -1;
      lastIdx = -1;
    });
});

function update() {
    let calendar = {};
    //Loop over every hour
    $("table tbody").find('tr').each(function (row) {
        let $tds = $(this).find('td');
        calendar[convert(row)] = [];
        //Loop over every day for that hour
        for (let i = 0; i < $tds.length; i++) {
            if($tds.eq(i).attr('class') === "busy-time") {
                calendar[convert(row)].push(true);
            } else {
                calendar[convert(row)].push(false);
            }
        }
    });
}

function convert(idx) {
    switch(idx) {
        case 0:
            return "12:00 AM";
        case 1:
            return "12:30 AM";
        case 2:
            return "1:00 AM";
        case 3:
            return "1:30 AM";
        case 4:
            return "2:00 AM";
        case 5:
            return "2:30 AM";
        case 6:
            return "3:00 AM";
        case 7:
            return "3:30 AM";
        case 8:
            return "4:00 AM";
        case 9:
            return "4:30 AM";
        case 10:
            return "5:00 AM";
        case 11:
            return "5:30 AM";
        case 12:
            return "6:00 AM";
        case 13:
            return "6:30 AM";
        case 14:
            return "7:00 AM";
        case 15:
            return "7:30 AM";
        case 16:
            return "8:00 AM";
        case 17:
            return "8:30 AM";
        case 18:
            return "9:00 AM";
        case 19:
            return "9:30 AM";
        case 20:
            return "10:00 AM";
        case 21:
            return "10:30 AM";
        case 22:
            return "11:00 AM";
        case 23:
            return "11:30 AM";
        case 24:
            return "12:00 PM";
        case 25:
            return "12:30 PM";
        case 26:
            return "1:00 PM";
        case 27:
            return "1:30 PM";
        case 28:
            return "2:00 PM";
        case 29:
            return "2:30 PM";
        case 30:
            return "3:00 PM";
        case 31:
            return "3:30 PM";
        case 32:
            return "4:00 PM";
        case 33:
            return "4:30 PM";
        case 34:
            return "5:00 PM";
        case 35:
            return "5:30 PM";
        case 36:
            return "6:00 PM";
        case 37:
            return "6:30 PM";
        case 38:
            return "7:00 PM";
        case 39:
            return "7:30 PM";
        case 40:
            return "8:00 PM";
        case 41:
            return "8:30 PM";
        case 42:
            return "9:00 PM";
        case 43:
            return "9:30 PM";
        case 44:
            return "10:00 PM";
        case 45:
            return "10:30 PM";
        case 46:
            return "11:00 PM";
        case 47:
            return "11:30 PM";
        default:
            return "null";
    }
}