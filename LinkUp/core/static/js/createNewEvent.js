function createNewEvent() {
      const title = document.getElementById("event_title").value;
      const description = document.getElementById("event_description").value;
      const duration = document.getElementById("event_duration").value;
      const start = document.getElementById("event_potential_start"); //trigger link
      const end = document.getElementById("event_potential_end").value;
      const createEvent = document.getElementById("createEvent").value;
      createEvent.action = "/eventcreation/"+title+"/"+description+"/"+duration+"/"+start+"/"+end; //+"/"+H+"/"+M;
}