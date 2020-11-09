
<h1>
    <p align="center">Covid by County Flask App</p>
</h1>

<h1></h1>
<a href = "https://bhyman67.github.io/Covid-by-County/">repo</a>

One function:

* pull_data()
  * makes a web request (GET) to the CSSEGISandData COVID-19 [repo](https://github.com/CSSEGISandData/COVID-19) and uses pandas read_csv funct to read in time_series_covid19_confirmed_US.csv. 
  * Some columns also get droped and renamed

Only two endpoints:

* The root url. Shows State and county drop downs along with the submit button.
  * GET: ``` / ```
* Graph endpoint accessed by the submit button. URL path is defined by what was submited in the dropdowns. 
  * GET: ``` /graph/ ```
  * This endpoint **requires** a query string with two parameters:
    * State
    * County
  * The data pull from the repo happens everytime this endpoint gets requested. Not ideal :(  

<p align="right">Back to <a href="https://bhyman67.github.io/">BHyman Analytics<a><p>