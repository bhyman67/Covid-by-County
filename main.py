
# Two things, can't pull up by path and data pull happens everytime

# Standard Library Imports
import json
import os 
import io

# Needed Libraries
from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd 
import numpy as np
import requests
import plotly

def pull_data():

    url = (
        "https://raw.githubusercontent.com"
        "/CSSEGISandData/COVID-19/master"
        "/csse_covid_19_data/csse_covid_19_time_series"
        "/time_series_covid19_confirmed_US.csv")
    download = requests.get(url).content
    df = pd.read_csv(io.StringIO(download.decode('utf-8')))

    df.drop(columns=["UID","iso2","iso3","code3","FIPS","Country_Region","Lat","Long_"], inplace=True)
    df.rename(columns = {"Admin2":"County","Province_State":"State"}, inplace = True)

    return df

app = Flask(__name__)

@app.route("/", methods = ["GET","POST"])
def home():

    # Pull the data
    df = pull_data()

    # List all locations
    locations = df["Combined_Key"].to_list()
    states = list(df["State"].unique())

    return render_template("index.html", states = states, list=locations)

@app.route("/<state>/<county>", methods = ["GET","POST"])
def county_graph(state, county):

    # Pull the data
    df = pull_data()

    # List all locations
    locations = df["Combined_Key"].to_list()
    states = list(df["State"].unique())

    # Filter
    if "county" in request.form:
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

if __name__ == "__main__":

    app.run(debug=True)