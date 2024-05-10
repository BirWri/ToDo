# Todo description 
A simple web application to create a list of "To Do"-s. The application comes with a `login`, `create a "To Do"` and a `log-out`. Each "To Do" consist of a `title` and `text`. The aim of this exersice is to implement 3 new features:

- Add the field `“created_at”` to the "To Do" SQL database. It needs to register the date of creation of the "To Do".
- Add an api listening on `/api/search` that takes a query `param q`. The api lists all the "To Do"-s where $q is in the title as `json`.
- Each time a new "To Do" is created, send an HTTP POST request to https://postman-echo.com/post with a representation of the todo. In this version the title of the newly created "To Do" has been defined to be the representation. 

# Flask Official Tutorial
Flaskr, from the official tutorial of Flask documentation. Unlike the example found in Flask sources, it does not make use of Blueprint that are not introduced in the tutorial). http://flask.pocoo.org/docs/0.12/tutorial/folders/#tutorial-folders Like the tutorial, user name is `admin` and password is `default`.

# Running the server 
## Development mode 
### The flask tutorial way (not IDE friendly) 
Creates and activate your virtual environment, then: 
```text env\Scripts\activate.bat pip install --editable . set FLASK_APP=flaskr set FLASK_DEBUG=true flask initdb flask run ```

### IDE friendly way
Runs the `manage.py` script from your IDE as if it was the flask command above. This script invokes the flask command after setting the environment variable. So, for example in PyCharm, set: - `Script` to the full path of `manage.py` - `Script parameters` to `run` (or `initdb` to initialize the database)

 ## Production mode
 See http://flask.pocoo.org/docs/0.12/deploying/#deployment # ToDo
