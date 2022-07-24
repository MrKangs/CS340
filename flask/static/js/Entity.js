var length_of_data = document.getElementById("length").innerHTML;
var checkbox_list = document.getElementsByClassName("checkbox");
for (let i = 0; i < length_of_data; i++){
    var checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.name = "select";
    checkbox.value = i;
    checkbox_list[i].appendChild(checkbox);
}


// Execute the function when the user presses the return button to search for a
// database record.
function didPressReturn(event) {
    if (event && event.keyCode == 13) {
        console.log("triggered");
        return false;

        // Here we need to search for the record and dynamically change the
        // state of the entity table to display the results.

        // If we enter backspace in the search box, we need to dynamically
        // change the state of the entity table to display the entire data set.
    }
}