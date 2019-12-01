$(document).ready(function(){
    // To change event title
    $('#EventTitle').on('blur', function() {
        const eventID = window.location.pathname.split("/").pop();
        $.ajax({
            headers: {"X-CSRFToken": CSRF_TOKEN},
            type: "POST",
            url:   "change_event_title/",
            data: { "new_title": $('#EventTitle').text(), "event_id": eventID },
        }).success(function (){
           // alert('Event title changed!');
            location.reload();
        }).fail(function () {
            alert('Failed to change event title!');
        });
    });

    // To change event description
    $('#EventDescription').on('blur', function() {
        const eventID = window.location.pathname.split("/").pop();
        $.ajax({
            headers: {"X-CSRFToken": CSRF_TOKEN},
            type: "POST",
            url:   "change_event_description/",
            data: { "new_description": $('#EventDescription').text() , "event_id": eventID },
        }).success(function (){
           // alert('Event description changed!');
           // location.reload();
        }).fail(function () {
            alert('Failed to change event Description');
        });
    });

    $(".li-admin-option").on('click', function () {
        const newAdminName = $(this).text();
        const eventID = window.location.pathname.split("/").pop();
        $.ajax({
            headers: {"X-CSRFToken": CSRF_TOKEN},
            type: "POST",
            url:   "add_event_admin/",
            data: { "new_admin": newAdminName , "event_id": eventID },
        }).success(function (){
            alert(newAdminName + ' has been added as a administrator !');
        }).fail(function () {
            alert('Event Admin not Added');
        });
    });
});




//// Add Admin
function Search() {
  document.getElementById("myDropdown").classList.toggle("show");
}

function filterFunction() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  console.log(filter);
  let div = document.getElementById("myDropdown");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

//end of function

////Add admin



