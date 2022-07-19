function uploadRecord(html_file){

    var forms = document.getElementById("forms");


    if(confirm("Are you sure you want to upload this record?")){
        console.log("Uploaded");
        forms.action = html_file;
        // We can put validation if there is any missing fields after they confirm it or not.
    } else{
        console.log("Cancelled");
        console.log(len(forms));
        // This will simply hide the pop up and remain in the page with the values
    }

}