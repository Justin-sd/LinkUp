class BulmaModal {
	constructor(selector) {
		this.elem = document.querySelector(selector)
		this.close_data()
	}

	show() {
		this.elem.classList.toggle('is-active')
		this.on_show()
	}

	close() {
		this.elem.classList.toggle('is-active')
		this.on_close()
	}

	close_data() {
		var modalClose = this.elem.querySelectorAll("[data-bulma-modal='close'], .modal-background")
		var that = this
		modalClose.forEach(function(e) {
			e.addEventListener("click", function() {

				that.elem.classList.toggle('is-active')

				var event = new Event('modal:close')

				that.elem.dispatchEvent(event);
			})
		})
	}

	on_show() {
		var event = new Event('modal:show')

		this.elem.dispatchEvent(event);
	}

	on_close() {
		var event = new Event('modal:close')

		this.elem.dispatchEvent(event);
	}

	addEventListener(event, callback) {
		this.elem.addEventListener(event, callback)
	}
}

var createEventBtns = document.querySelectorAll("#createEvent")
var mdl = new BulmaModal("#createModal")

createEventBtns.forEach(function(btns) {
    btns.addEventListener("click", function() {
        mdl.show()
    });
});


mdl.addEventListener('modal:show', function() {
	console.log("opened")
})

mdl.addEventListener("modal:close", function() {
	console.log("closed")
})

var logoutBtns = document.querySelectorAll("#logout")
var logoutMdl = new BulmaModal("#logoutModal")

logoutBtns.forEach(function(btns) {
    btns.addEventListener("click", function() {
        logoutMdl.show()
    });
});


logoutMdl.addEventListener('modal:show', function() {
	console.log("opened")
})

logoutMdl.addEventListener("modal:close", function() {
	console.log("closed")
})

var deleteBtns = document.querySelectorAll("#deleteBtn")
var deleteMdl = new BulmaModal("#deleteModal")

deleteBtns.forEach(function(btns) {
    btns.addEventListener("click", function() {
        deleteMdl.show()
    });
});


deleteMdl.addEventListener('modal:show', function() {
	console.log("opened")
})

deleteMdl.addEventListener("modal:close", function() {
	console.log("closed")
})

var deleteMemberBtns = document.querySelectorAll("#deleteMemberBtn")
var deleteMemberMdl = new BulmaModal("#deleteMemberModal")

deleteMemberBtns.forEach(function(btns) {
    btns.addEventListener("click", function() {
    	document.getElementById("areyousure").innerText = "Are you sure you want to remove " +$(this).text()+ "?";
        deleteMemberMdl.show()
    });
});


deleteMemberMdl.addEventListener('modal:show', function() {
	console.log("opened")
})

deleteMemberMdl.addEventListener("modal:close", function() {
	console.log("closed")
})
