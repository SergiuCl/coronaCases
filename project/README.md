# **Coronavirus Project**
<br/>

## **Summary**
* [Installation](#installation)
* [Run Program](#run-program)
* [Introduction](#introduction)
* [Description](#description)
* [Technologies](#technologies)
* [Sources](#sources)

<br/>

## **Installation**

* Use the package manager pip to install the requirements. Write the following in your terminal:
```bash
pip install -r requirements.txt
```
<br/>

## **Run Program**

* Write the following in your terminal to start the program:

    * Linux/macOS
    ```bash
    python3 -m flask run
    ```
    * Windows
    ```bash
    python -m flask run
    ```

<br/>

## **Introduction**

* Coronavirus Project is a web application developed in Flask. The web application contains regularly updated information about the new Coronavirus situation around the world with focus on Austria, the country where I currently live.

<br/>

## **Description**

* The main page displays the latest news in Austria via an API from *https://newsapi.org/*. All of them are displayed in an HTML table and each news contains an image, title, a short description and a link that redirects the user to  another HTML page when clicked. This page shows the image, title, content and a frame with Corona Cases in Austria. The news are updated every 10 minutes using a Background Scheduler.

* The next page is called "*Cases In Austria*". An HTML table is displayed on this page that stores the latest Corona cases in Austria (active cases, new cases, new deaths, total cases, total deaths and total recovered), which were received from an API called "*COVID-19 Tracking*" from *https://rapidapi.com/*. The cell with the name of the country from the HTML table contains a link that redirects the user to another HTML page when clicked. The page is called "*history/(name of country)*" and pictures some charts with the daily Corona Cases evolution in Austria: New Cases, New Deaths and Active Cases. The number of daily cases is stored in the database "*coronaDatabase*" in a table called "*history*".

* The next page is called "*Check by country*" and is very similar to "*Cases In Austria*". The difference is that this page displays all countries worldwide. Every single cell with the name of the country contains a link that redirects the user to the page "*history/(name of country)*", which pictures the charts with the daily Corona cases evolution in that country. Using the Background Scheduler, the program checks every 10 minutes whether there are any updates in the API. If so, the SQL table "*casesWorld*" from the database "*coronaDatabase*" is updated and the new number of cases is inserted into the table "history" for the current day.

* The next page is called "*Subscribe*". This page pictures a HTML form where the user can enter his email address and name and select a country from which he would like to get updates from. When the user sends the information to the server by clicking the Submit button, the program checks whether the user already exists. If so, he will be notified, otherwise the information will be inserted into the table "*subscribers*" from the "*coronaDatabase*". There is also the option to unsubscribe. If the user selects the unsubscribe check box, the program will check whether the user exists in the database. If the user exists, he will be removed and notified, otherwise he will be informed that the specified email does not exist. The users will receive an email via SendGrid with new and active cases every time the selected country will update.

* The next and the last page is called "*Subscribers Panel*". This page requires the users to be logged in when they click the link. After the user signs in, an HTML table appears on the page "*usersTable*" with the name, email address, country and edit and delete buttons for each user. If the user has an admin role, he can edit and delete the existing subscribers and also create new subscribers. If the user has read-only role, the edit, delete and create buttons are disabled.

<br/>

## **Technologies**

* The web application is created with:

    * Flask
    * SQLite3
    * HTML
    * CSS
    * JavaScript

<br/>

## Sources

* The following sources were used to create the web application:

    * https://newsapi.org/
    * https://rapidapi.com/
    * https://sendgrid.com/
    * https://www.highcharts.com/