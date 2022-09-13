# blindspot_technical_interview

This Program takes a given address and a distance in kilometers and display a of all Starbucks locations within the radius.
For a list of modules please see requirements.txt
Flow:
1.FLASK web application with a simple html form.
2.Taking the variables from the form after POST request.
3.Convert csv file with locations to dataframe using Pandas.
4.Loop through the data frame to calculate distance from each location using Geopy library(Address to coordinates and distance) and collect the indexes in which the distance is inside the radius.
5.Create new Dataframe with the locations and convert it to html using Pandas.
6.POST the html on the web page using Jinja2
