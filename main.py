# use flask to enter in parameters and display chart
# use plotly for the line chart 
# deploy the app in heroku
from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd 
import numpy as np
import plotly
import json
import os 

app = Flask(__name__)

@app.route("/", methods = ["GET","POST"])
def home():

    # Read in the data (should only have to read in the data once, but we'll 
    # figure that out l8er...)
    df = pd.read_csv('data/time_series_covid19_confirmed_US.csv')
    df.drop(columns=["UID","iso2","iso3","code3","FIPS","Country_Region","Lat","Long_"], inplace=True)
    df.rename(columns = {"Admin2":"County","Province_State":"State"}, inplace = True)

    # I think what i want to do instead is list all states and counties

    # list all locations
    locations = df["Combined_Key"].to_list()

    if "locations" in request.form:
        if request.form["locations"] != "":
            graphData = True
    else:
        graphData = False

    if graphData:
        # Next step depends on whether the breakdown is by state or county
        breakDownByCounty = True
        if breakDownByCounty:

            # Filter
            county = request.form["locations"].split(",")[0] #"Jefferson"
            state = request.form["locations"].split(",")[1].strip() #"Colorado"
            df = df[(df["County"] == county) & (df["State"] == state)]

            # Extract out the time series
            df.drop(columns = ["County","State"],inplace = True)
            df = df.T
            new_header = df.iloc[0] #grab the first row for the header
            df = df[1:] #take the data less the header row
            df.columns = new_header #set the header row as the df header

            # The time series
            stateCountryData = df.iloc[:,0].diff(1)

        else:

            # group by state and date, sum the date???
            # State #s need to be calculated per day

            # Grab the list of all dates

            print()

        # fig = px.line(stateCountryData, x="", y="", title='')
        fig = px.line(stateCountryData)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Return template and data
        return render_template("index.html", list=locations, graphJSON=graphJSON)
    
    else:
        return render_template("index.html", list=locations)

if __name__ == "__main__":

    app.run(debug=True)