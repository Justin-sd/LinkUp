//to change event title
const editable2 = document.getElementById('EventTitle');
editable2.addEventListener('blur', function() {
    const eventID = window.location.pathname.split("/").pop();
$.ajax({
  type: "POST",
  url:   "changeeventtitle/",
  data: { newTitle: editable2.innerText , eventid: eventID },
  csrfmiddlewaretoken: '{{ csrf_token }}'
});
    alert('Change of Name Sucessful !')
});


