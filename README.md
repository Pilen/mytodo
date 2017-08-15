# mytodo
A very simple todo site

# Assignment: Simple to-do list
Create a simple to-do list using the latest Django version.
Use Bootstrap CSS to make it look nice.
(Nice-to) Use AJAX to be able to create and check tasks without changing browser page.

OR

Create a simple to-do list using AngularJS (v.2) and Flask for the backend.
You can chose your own storage/database engine.

User functionalities
- Add a task
- List tasks
- Check a task (mark as solved)

Links:
- https://www.djangoproject.com
- http://getbootstrap.com
- http://jquery.com

## My choice
I decided to go with a Django backend, even though I have no prior experience with the framework.
This project is thus a showcase of how i came to terms with a "new" technology.
The backend is build as a mix of views returning html and json.
The frontend is build using jQuery and uses AJAX to work with todos on the server.

My notes from the delvelopment phase can be found in the textfile notes.org

# Setup
    This project is hardly meant for production use, to set it up locally do the following.

```
git clone "https://github.com/Pilen/mytodo.git"
cd mytodo
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py test
python3 manage.py runserver 8000
```
Then you can visit `localhost:8000` in your browser.

**IMPORTANT!**
If you intend to run the server publically or in any way use this project, then you have to create a new `SECRET_KEY` in mytodo/settings.py and disable `DEBUG` mode.
