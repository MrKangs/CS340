

function createUpdate(){
    let selectedItems = [];

    if(document.getElementById("row_selection").checked == true){
        var checks = document.getElementById("row_selection");
        var num_of_checks = checks.length;
        console.log(num_of_checks);
        console.log("Update");

        // Append the selected row items to the selectedItems array
        for (var i = 0; i < num_of_checks; i++) {
            if (checks[i].checked == true) {
                selectedItems.push(checks[i].value);
            }
        }
        // 1. Search the value that the user is selected only 1
        if (selectedItems.length > 1) {
            alert("Please select only 1 record to update");
        } else if (selectedItems.length == 0) {
            alert("Please select at least one record to update");
        }  else if (selectedItems.length == 1) {
            // 2. If the user is selected only 1, then redirect to the update page
            window.location.href = "update.html?id=" + selectedItems[0];
        }
            // 3. Search the value that the user is selected 0
        // 2. If there is more than 1, then show an error message
        // 3. If there is only 1, then show the update form from search

    }
    else{
        console.log("Create New Record");
    }
}


function deleteConfirmation(){

    if(document.getElementById("row_selection").checked == true){
        if (confirm("Are you sure you want to delete this Selection?")) {
            console.log("Deleted");
        } else {
            console.log("Cancelled");
        }
    }
    else{
        alert("Please select at least one record to delete");
    }
}