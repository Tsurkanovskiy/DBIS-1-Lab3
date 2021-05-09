function open_edit_field(event){
	new_entry_button = document.getElementById("create");
	new_entry_button.style.display = "none";
	new_entry_button.removeEventListener("click", show_hidden);
	const hidden_elem = document.getElementById("entry_form");
	hidden_elem.style.display = "block";


	hidden_elem.action = "./update"
	const entry_id = document.getElementById("edit_id");
	entry_id.value = event.currentTarget.parentNode.value;
}

function show_hidden(event){
	var e = event.currentTarget;
	e.style.display = "none";
	const hidden_elem = document.getElementById("entry_form");
	hidden_elem.style.display = "block";
}

window.addEventListener("load", function(){
	const edit_buttons = document.getElementsByClassName("edit_button");
	for (var i = edit_buttons.length - 1; i >= 0; i--) {
		edit_buttons[i].addEventListener("click", open_edit_field);
	}
	document.getElementById("create").addEventListener("click", show_hidden);
});