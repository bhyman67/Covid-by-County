# parameterized endpoints
from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd 
import numpy as np
import requests
import plotly
import json
import os 
import io

def pull_data():

    url = (
        "https://raw.githubusercontent.com"
        "/CSSEGISandData/COVID-19/master"
        "/csse_covid_19_data/csse_covid_19_time_series"
        "/time_series_covid19_confirmed_US.csv")
    download = requests.get(url).content
    df = pd.read_csv(io.StringIO(download.decode('utf-8')))

    return df

app = Flask(__name__)

@app.route("/", methods = ["GET","POST"])
def home():

    # Read in the data (should only have to read in the data once, but we'll 
    # figure that out l8er...)
    df = pull_data() 
    df.drop(columns=["UID","iso2","iso3","code3","FIPS","Country_Region","Lat","Long_"], inplace=True)
    df.rename(columns = {"Admin2":"County","Province_State":"State"}, inplace = True)

    # List all locations
    locations = df["Combined_Key"].to_list()
    states = list(df["State"].unique())

    # This is for determining whether or not a county has been selected to graph
    # that won't be the case for when the html gets pulled up for the first time.
    if "county" in request.form:
        if request.form["county"] != "":
            graphData = True
    else:
        graphData = False

    if graphData:

        # Filter
        county = request.form["county"]
        state = request.form["state"]
        df = df[(df["County"] == county) & (df["State"] == state)]

        # Extract out the time series
        df.drop(columns = ["County","State"],inplace = True)
        df = df.T
        new_header = df.iloc[0] #grab the first row for the header
        df = df[1:] #take the data less the header row
        df.columns = new_header #set the header row as the df header
        stateCountryData = df.iloc[:,0].diff(1)

        # fig = px.line(stateCountryData, x="", y="", title='')
        fig = px.line(stateCountryData)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        # Return template and data
        return render_template("index.html", list=locations, states = states, graphJSON=graphJSON)
    
    else:

        return render_template("index.html", states = states, list=locations)

if __name__ == "__main__":

    app.run(debug=True)