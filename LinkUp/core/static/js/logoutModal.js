$(document).ready(function() {
  const modal2 = document.getElementById("LogOutModal");

  // Get the button that opens the modal
  const btn2 = document.getElementById("logoutbutton");

  // When the user clicks the button, open the modal
  btn2.onclick = function () {
    modal2.show();
  };
});