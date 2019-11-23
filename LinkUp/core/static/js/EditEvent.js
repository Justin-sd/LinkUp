//to change event title
const eventTitle = document.getElementById('EventTitle');

eventTitle.addEventListener('blur', function() {
    const eventID = window.location.pathname.split("/").pop();
    $.ajax({
        headers: {"X-CSRFToken": CSRF_TOKEN},
        type: "POST",
        url:   "change_event_title/",
        data: { "new_title": eventTitle.innerText , "event_id": eventID },
    }).success(function (){
        alert('Event title changed!');
    }).fail(function () {
        alert('Failed to change event title!');
    });
});


//to change event description
const eventDescription = document.getElementById('EventDescription');

eventDescription.addEventListener('blur', function() {
    const eventID = window.location.pathname.split("/").pop();
    $.ajax({
        headers: {"X-CSRFToken": CSRF_TOKEN},
        type: "POST",
        url:   "change_event_description/",
        data: { "new_description": eventDescription.innerText , "event_id": eventID },
    }).success(function (){
        alert('Event description changed!');
    }).fail(function () {
        alert('Failed to change event Description');
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

function AddAdmin(){

    const newAdmin = document.getElementById("member").innerText;

    const eventID = window.location.pathname.split("/").pop();
    $.ajax({
        headers: {"X-CSRFToken": CSRF_TOKEN},
        type: "POST",
        url:   "add_event_admin/",
        data: { "new_admin": newAdmin , "event_id": eventID },
    }).success(function (){
        alert('Event Admin Added!');
    }).fail(function () {
        alert('Event Admin not Added');
    });

}//end of function

////Add admin



