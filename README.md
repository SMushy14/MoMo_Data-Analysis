#**MoMo Dashboard** 
**MoMo Dashboard** is a web application that displays the contents of transactions that happened on a person's mobile money account. It helps the user know how much they spent on Airtime, Internet bundles, voice bundles, how much they’ve withdrawn from their account, how much was deposited, and more.

**Introduction**
An XML file was provided containing approximately 1600 SMS messages of various types from the famous Mobile Payment Service Provider in Rwanda, MTN MoMo
Links to an external site. The goal is to process the data, load it into a database, and create an interactive dashboard to analyze and display insights derived from the SMS data.

**Analysis**
To go about this project it would require skills in;
Python
Create scripts to parse/filter data in the XML file, extract important information, and make it make sense.
Create a flask script to display the information filtered and stored in a database to the MoMo Dashboard

HTML
Designing a dashboard to diplay the results in the databas.

CSS
Styling the HTML file to make it visually appealing and user-friendly. 

Regex
Script to extract and identify the important keywords in the XML file so that it can extract the required data. For example identifying the keywords for transaction ID, type of payment, etc.

Database
Store the parsed information filtered from the XML file

**Methodolody**
The parser.py file filters data from the sample_data.xml file and stores it in the parsed_data.db database. ->> The app.py file displays information from the parsed_data.db file and displays it through the index.html file(MoMo Dashboard).

[Link to the Project Report](https://docs.google.com/document/d/1A0QkqYsS9wNocVKEPHVHvcMb4saqCf1Xd0qrsIVKoDk/edit?usp=sharing )
