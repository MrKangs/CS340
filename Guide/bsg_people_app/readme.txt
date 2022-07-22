IMPORTANT: Don't forget to fill in the database connection information the port number in app.py

Core functionality:
-Rendered '/people' page where user can view a bsg_people table with all entries and accompanying attributes visible
-User can edit or delete bsg_people entries directly from the table by selecting edit/delete on the desired table row
-User can add a new person to bsg_people by clicking 'Add new', filling out the 'Add Person' form, and clicking the 'Add Person' button
-Edit Person form on the people page is just to showcase what the form looks like, real edit form will pop up when a user selects 'Edit'
-User can click on either 'Cancel' button to hide the forms

General Development Steps/Notes:
1) Started by importing bsg_universe.sql via phpmyadmin UI (https://classmysql.engr.oregonstate.edu/index.php) into the school provided database
2) Imported required modules (see Step 0 instructions)
3) Set up Database connection info in app.py
4) Created routes for '/', '/people', '/delete_people', '/edit_people'
5) Redirect '/' route to '/people' for quality of life purposes for this particular app (since we don't have a home page)
6) Start with people route and work down from there, comments in app.py should serve as a step by step from here on out
7) Don't forget to change the port number at the bottom if hosting on the flip servers

HTML tidbit:
-HTML should be reasonably self-explanatory, can be as creative as you desire with HTML, certain key elements explained through comments
-Warning my HTML is very basic (probably a tad messy and could be formatted better), but it gets the job done, again HTML will vary from person to person and group to group depending on how creative you want to get
