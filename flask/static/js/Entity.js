var length_of_data = document.getElementById("length").innerHTML;
var checkbox_list = document.getElementsByClassName("checkbox");
for (let i = 0; i < length_of_data; i++){
    var checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.name = "select";
    checkbox.id = "checkbox-" + i;
    checkbox.value = i;
    checkbox_list[i].appendChild(checkbox);
}

const html_pairs = {
    "/userAccountsEntity.html":"/userAccountsForm.html"
}

function onUpdate(){
    var checkbox_list = document.getElementsByClassName("checkbox");
    var isSelected = false;
    var selectedCheckbox;

    for (let i = 0; i < checkbox_list.length; i++){
        var id_name = "checkbox-"+i;
        var checkbox = document.getElementById(id_name);
        if(checkbox.checked && isSelected == false){
            isSelected = true;
            selectedCheckbox = checkbox;
        }
        else{
            alert("Please select only one record for update!");
            return 0;
        }
    }
    var html_location = window.location.pathname;
    console.log(html_location);
    var value = selectedCheckbox.value;
    console.log(value);
    html_location = html_pairs[html_location];
    console.log(html_location);
    const request = new XMLHttpRequest();
    request.open('POST', `${html_location}/${value}`);
    request.send();
    return 1;
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