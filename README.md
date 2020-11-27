# Coding Exercise

Simple webapp that wraps Gracenote API services and presists data in MySQL database.
>P.S. this needs a lot of refactoring but demonestrates the idea.


#### MySQL Dump

  - Dump.sql contains the DDL script to create the database, tables and relationships

### Prerequisites

Python , Virtualenv & MySQL.

Change USR to your database user, PWD to your database password in ```secrets.py```
Also you can change the IP and port for the web-app.


### Running the App
 - Downloading the packages.
```sh
$ cd Exercise
$ virtualenv venv
$ ./activate
$ pip install -r ../../requirements.txt
```

 - Bringing Flask web app to life.

```sh
$ python app.py
```

### API Calls

Every get data API returns json with ```status 200``` if the process is done successfuly otherwise you should recieve ```status 404```.
The API only accepts the requests as the following (you can change the values of course but keep the token as is) 


- Get data for movies playing in local theatres in US for a particular zip code and start date
```sh
http://127.0.0.1:5000/movies?startDate=2020-11-27&zip=78701&api_key=7sta9hza6u3j5b4y6uxjn2a2
asdd
```
- Get data for movies airing on TV for a particular line up and date and time
```sh
http://127.0.0.1:5000/movies?lineupId=USA-TX42500-X&startDateTime=2020-11-27&api_key=7sta9hza6u3j5b4y6uxjn2a2
```
- Top 5 Genres with the highest movie count along with the movie description (this call returns the data as JSON object)
```sh
http://127.0.0.1:5000/compute
```
### Todos

 - Write Tests
 - Refactor...






