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
    "/entities/userAccountsEntity.html":"/forms/userAccountsForm.html",
    "/entities/fiatWalletsEntity.html":"/forms/fiatWalletsForm.html",
    "/entities/dogecoinWalletsEntity.html":"/forms/dogecoinWalletsForm.html",
    "/entities/dogecoinTransactionsEntity.html":"/forms/dogecoinTransactionsForm.html",
    "/entities/exchangeOrdersEntity.html":"/forms/exchangeOrdersForm.html"

}

function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);
}

function onUpdate(){
    var checkbox_list = document.getElementsByClassName("checkbox");
    var isSelected = false;
    var selectedCheckbox;
    var html_location = window.location.pathname;

    for (let i = 0; i < checkbox_list.length; i++){
        var id_name = "checkbox-"+i;
        var checkbox = document.getElementById(id_name);
        if (checkbox.checked && isSelected == true){
            alert("Please select only one record for update!");
            return html_location;
        }
        if(checkbox.checked && isSelected == false){
            isSelected = true;
            selectedCheckbox = checkbox;
        }
    }
    if(isSelected == false){
        alert("Please select one record for update!");
        return html_location;
    }
    var selectedPK = document.getElementsByClassName("data")[selectedCheckbox.value].cells.item(1).textContent;
    var html_location = window.location.pathname.split("%")[0];
    console.log(html_location);
    html_location = html_pairs[html_location];
    const request = new XMLHttpRequest();
    request.open('POST', `${html_location}/${selectedPK}`, true);
    request.send();
    return `${html_location}/${selectedPK}`;
}

function onDelete() {
    var checkboxes = document.getElementsByClassName("checkbox");
    var isSelected = false;
    var selectedCheckbox;
    var html_location = window.location.pathname;

    for (let i = 0; i < checkboxes.length; i++) {
        var checkboxID = "checkbox-" + i;
        var currCheckbox = document.getElementById(checkboxID);
        // if (currCheckbox.checked && isSelected == true){
        //     alert("Please select only one record to delete!");
        //     return html_location;
        // }
        if (currCheckbox.checked && isSelected == false) {
            isSelected = true;
            selectedCheckbox = checkbox;
        }
    }

    // Alert the user if they haven't selected a record to delete.
    if (isSelected == false) {
        alert("Please select one record to delete!");
        return html_location;
    }
    
    let selectedPKs = getSelectedPKs();

    // var selectedPK =
    // document.getElementsByClassName("data")[selectedCheckbox.value].cells.item(1).textContent;
    
    var html_location = window.location.pathname.split("%")[0];
    console.log(html_location);
    const request = new XMLHttpRequest();
    request.open('POST', `${html_location}/${selectedPKs}/delete`, true);
    request.send();
    sleep(checkboxes.length*10);
    return window.location

}

function getSelectedPKs() {
    var checkboxes = document.getElementsByClassName("checkbox");
    var selectedPKs = "";
    for (let i = 0; i < checkboxes.length; i++) {
        var checkboxID = "checkbox-" + i;
        var currCheckbox = document.getElementById(checkboxID);

        // Add a checked checkbox to the selectedPKs string.
        if (currCheckbox.checked) {
            selectedPKs += document.getElementsByClassName("data")[i].cells.item(1).textContent;
            selectedPKs += ",";
        }
    }
    return selectedPKs;
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