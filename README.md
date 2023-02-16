# code-challenge


# Code Challenge Template

Problem 1 - Data Modeling
-------------------------
Choose a database to use for this coding exercise (SQLite, Postgres, etc.). Design a data model to represent the weather data records. If you use an ORM, your answer should be in the form of that ORM's data definition format. If you use pure SQL, your answer should be in the form of DDL statements.

>>>>>>>>>
Answer:

Postgres Database is used.
Django framework is used to design the model where there are three classes: station, weatherData,weatherSummary
Django ORM is used to work with data and in analysis.




Problem 2 - Ingestion
---------------------
Write code to ingest the weather data from the raw text files supplied into your database, using the model you designed. Check for duplicates: if your code is run twice, you should not end up with multiple rows with the same data in your database. Your code should also produce log output indicating start and end times and number of records ingested.

>>>>>>>>>
Answer:

Importing data from raw files, Django management command is used so that the command import_data and import_from_multiple_files can import the data from txt file to postgres database.It also checks the duplicate of records and also log output is stored in logs folder and each station is provided with separate log file.




Problem 3 - Data Analysis
-------------------------
For every year, for every weather station, calculate:

* Average maximum temperature (in degrees Celsius)
* Average minimum temperature (in degrees Celsius)
* Total accumulated precipitation (in centimeters)

Ignore missing data when calculating these statistics.

Design a new data model to store the results. Use NULL for statistics that cannot be calculated.

Your answer should include the new model definition as well as the code used to calculate the new values and store them in the database.

>>>>>>>>>
Answer:

Pandas is used to do analysis. I have also implied pandas feature so that it can skipt the missing values i.e. -9999. And the analysis is stored in separate table weathersummary and it can be acheived with management command python manage.py analysis. 
There is also use of unit tests which check for the records present in weather data or not and also do analysis properly skipping -9999 value.





Problem 4 - REST API
--------------------
Choose a web framework (e.g. Flask, Django REST Framework). Create a REST API with the following GET endpoints:

/api/weather
/api/weather/stats

Both endpoints should return a JSON-formatted response with a representation of the ingested/calculated data in your database. Allow clients to filter the response by date and station ID (where present) using the query string. Data should be paginated.

Include a Swagger/OpenAPI endpoint that provides automatic documentation of your API.

Your answer should include all files necessary to run your API locally, along with any unit tests.


>>>>>>>>>
Answer:

I have used /api/weather and /api/stats as endpoints to return json formated outcome. I have used Django Rest Framework for the creation of api. The page is also paginated and evern data filter can be performed in according to name of station, date, date year.
I have also input Swagger/OpenAPI in the urls which provide automatic documentation of the above api.



Extra Credit - Deployment
-------------------------
(Optional.) Assume you are asked to get your code running in the cloud using AWS. What tools and AWS services would you use to deploy the API, database, and a scheduled version of your data ingestion code? Write up a description of your approach.



>>>>>>>>>

for this deployment I have writeen my approach in aws.txt file.
