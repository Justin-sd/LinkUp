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
        let newAdminEmail = $(this).text();
        const index1 = newAdminEmail.indexOf("[");
        const index2 = newAdminEmail.indexOf("]");
        const size = index2-1 - index1;
        newAdminEmail = newAdminEmail.substr(index1+1,size);
        const eventID = window.location.pathname.split("/").pop();
        $.ajax({
            headers: {"X-CSRFToken": CSRF_TOKEN},
            type: "POST",
            url:   "add_event_admin/",
            data: { "new_admin": newAdminEmail , "event_id": eventID },
        }).success(function (){
            alert(newAdminEmail + ' has been added as a administrator !');
        }).fail(function () {
            alert('Event Admin not Added');
        });
    });

       $(".li-removeadm-option").on('click', function () {
        let removedAdmin = $(this).text();
        const index1 = removedAdmin.indexOf("[");
        const index2 = removedAdmin.indexOf("]");
        const size = index2-1 - index1;
        removedAdmin = removedAdmin.substr(index1+1,size);
        const eventID = window.location.pathname.split("/").pop();
        $.ajax({
            headers: {"X-CSRFToken": CSRF_TOKEN},
            type: "POST",
            url:   "remove_event_admin/",
            data: { "old_admin": removedAdmin , "event_id": eventID },
        }).success(function (){
            alert(removedAdmin + ' has been removed as a administrator !');
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


//Remove an admin
function filterFunction2() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput2");
  filter = input.value.toUpperCase();
  let div = document.getElementById("myDropdown2");
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



