# DIARY and NOTE website

#### Video Demo: <URL HERE>

#### Description:

- First of all, I'm sorry because my English is not good enough to write in English according to everyone's standards. I have to ask for help from Google Translate.

- We start with layout.html. Here I use Bootstrap to design the title bar and navigation bar. The navigation bar includes the home page for writing a diary, for special people, My notes and the history of notes and log and I use this file to inherit into other files through the user's login session or use it for login or registration. Next we come to the components:

  - first is index.html which inherits from layout.html after the user logs in to the correct account specified by the app.py file we display the date and then we have a box to enter that day's log After entering, the user clicks save today's diary, that diary page will be saved in the database, specifically the diary_time table.

  - The section for special people is written in the foryou.html file, which is the same as the index .html file, but this file adds one more box to save the name of the person you want to write after clicking save diary today. That person's name is also saved in the database. data with column as "for".

  - Next, go to the My Notes section. This section is written from the mynote.html file, this file is the same as the index.html file, but when you click save, the content will be saved into a new table in the database. This table is called "notes".

  - Go to the note history section. This section is written from the note_history.html file. This section displays the notes we have previously recorded and has an additional delete function when the note is no longer used, the delete function. will delete a row in the database when the user clicks delete.

  - Go to the note history section. This section is written from the note_history.html file. This section displays the notes we have previously recorded and has an additional delete function when the note is no longer used, the delete function. will delete a row in the database when the user clicks delete.

  - Finally, there is the diary history page where we can see and read what we wrote on the home page and the page for special people. On this page there will be 3 columns including: diary, date and time, for you. This page does not have the function to delete diary entries because when we write a diary it will be very boring if we can delete it because it is a part of memories. This page is also inherited from the layout.html file.

- We go to the login and registration section. These 2 pages are also inherited from the layout.html file. When there is no login session, if the user accesses any page using the address bar, they will be taken to the login page. If the user does not have an account, he or she can register via the registration page to register a username. new.

- The app.py file is used to perform all functions and routes to the specified page.

- user.db file to save the database during the login session. This file has 3 tables:

  - The users table is used to store the login name and the results returned after hashing the password using the hash function.
  - The diary_time table is used to store the user's diary. This table can store the name of the person the user wants to write.
  - The notes table is used to store user notes.

- in the static folder is used to save the icons and images I use in this website and style.css to save customizations of my HTML pages with css language.
