# Todo description 
A simple web application to create a list of "To Do"-s. The application comes with a `login`, `create a "To Do"` and a `log-out`. Each "To Do" consist of a `title` and `text`. The aim of this exersice is to implement 3 new features:

- Add the field `“created_at”` to the "To Do" SQL database. It needs to register the date of creation of the "To Do".
- Add an api listening on `/api/search` that takes a query `param q`. The api lists all the "To Do"-s where $q is in the title as `json`.
- Each time a new "To Do" is created, send an HTTP POST request to https://postman-echo.com/post with a representation of the todo. In this version the title of the newly created "To Do" has been defined to be the representation. 
