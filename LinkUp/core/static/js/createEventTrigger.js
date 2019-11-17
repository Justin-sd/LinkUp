// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
};

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target === modal) {
    modal.style.display = "none";
  }
};


function Create() { // create an event popup when create event button is clicked
      const P = document.getElementById("EventID").value; //get value from user
      const T = document.getElementById("EventTitle").value;
      const des = document.getElementById("description").value;
      const duration = document.getElementById("minutes").value;
      const link = document.getElementById("create"); //trigger link
      const start = document.getElementById("start").value;
      const end = document.getElementById("end").value;
      link.action = "/eventcreation/"+P+"/"+T+"/"+des+"/"+start+"/"+end+"/"+duration; //+"/"+H+"/"+M;
       window.open("/event_page/"+P);
}