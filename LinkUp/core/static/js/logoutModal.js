const modal2 = document.getElementById("LogOutModal");

// Get the button that opens the modal
const btn2 = document.getElementById("logoutbutton");

// Get the <span> element that closes the modal
const span2 = document.getElementsByClassName("close1")[0];

// When the user clicks the button, open the modal
btn2.onclick = function() {
  modal2.style.display = "block";
};

// When the user clicks on <span> (x), close the modal
span2.onclick = function() {
  modal2.style.display = "none";
};




window.onclick = function(event) {
  if (event.target === modal2) {
    modal2.style.display = "none";

  }
};