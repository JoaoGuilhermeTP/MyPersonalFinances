# My Personal Finances
#### Video Demo:  <URL HERE>
#### Description:

This is a basic application intended to help people organize and keep track of their personal finances. It allows users to register with a username and password, so that they can have access to their own finance data, and manage it the way they like.

If you want to try out this web application, you can access it through the following link: http://joaotasca.pythonanywhere.com/

### Features

The application allows users to do three main things:

1. Manage transactions (Transactions tab):
   - View transactions
     - The "Transactions" tab will by default show every transaction the user has already added previously. This can make it difficult to concentrate and focus when you are looking for something specific. That's why the user can also use the "Filter Transactions" form to filter the table. They can filter by multiple criteria, by filling the form and clicking "Filter". To clear all filters, simply click "Clear Filters".
     - Another thing users can do while viewing their transactions is ordering the table by column, in ascending or descending order, by clicking the column's headers.
   - Add transactions
     - The user can add each transaction they make by using the form titled as "Add Transactions" that is in the "Transactions" tab. They will be required to inform the date of the transactions, as well as the bank, category and value.
   - Delete transactions
     - The user can also delete individual transactions by clicking the button "Del" that will be accompaning every transaction in the table, or delete every transaction at once by clicking the red button "Delete all transactions".

2. Manage budgets (Budget tab):
    - The "Budget" tab will by default show the user's budget for the current month. The budgets table consists of three columns: "CATEGORY", which will contain every transaction category; "Planned", which will allow the user to type how much they think wll be transacted in that category, and "Actual", which will show how much was in fact transacted.
    - To save the budget with any modifications, click the "Save Budget" button.
    - It's also possible to view any other month, by using the form and inform the desired month and year, then clicking the "See Budget" button.

3. See yearly reports (Reports tab):
    - Here the user can see the total planned and transacted for any given year, by category. To see any specific year, type it in the form and click "See year report".

### Tecnologies used in this project

This project is using the following technologies:

Front-end:
* HTML
* CSS
* JAVASCRIPT
* BOOTSTRAP

Back-end:
* PYTHON
* FLASK
* SQL

## HTML Files

There are a few different files, applying different technologies, that are part of this project, each with it's own role. Let's understand what these files are and what they are doing:

Every HTML file in this project other than login.html and register.html, is divided into three main parts: Explanation (where there is a brief text describing what the user can do on that page), Left-Item (Contains the forms that the user will interact with. When the screen is large enough, they will be on the left side of the screen), and Right-Item (Contains the tables displaying the data to the user. When the screen is large enough, it will be on the right side of the screen).

Every HTML file in this project is using JINJA syntax to allow them do be dinnamically rendered according to variables and conditionals.

 ### **layout.html**

 This file serves as a template, containing parts of HTML that are reused throughout different pages of this application, like the meta tags, the title, bootstrap link, link to CSS file and the navigation bar.

  ### **login.html**

This file contains simply a form that will be used by the user to log into their account.

  ### **register.html**

This file contains a form that allows the user to register themselves so that they can log into their account.

### **transactions.html**

This is the main page that the user sees after they log in. It contains two forms, here referenced by their ID's:
     - add_transaction: This form sends the data that the user inputs via POST method to the "add_transaction" route, to be processed in the back-end.
     - filter_transactions: This form is also sending data via POST to the back-end, to the route "/".
     -  It also contains a **table** presenting the user with all the transactions they have added previously, each with a button to delete that transaction.
     - There is also a button, after both forms, that allows the user to delete all transactions at once.
     - Bootstrap is being applied to several styles in this HTML file.

### **budget.html**

This HTML file contains the table showing the budgets for each transaction category for any given month (the user will select the month through the form that is also in this HTML file).

### **reports.html**

This HTML file contains the table showing the total budget and total actually transacted for each category for any given year (the user can select the year using the form contained in this HTML file).

### **apology.html**

This HTML file contains an image tag that will display a text everytime the user does something that is not allowed or incorrect in the app.


## CSS files

### **layout.css**

This CSS is the style being applied to every HTML in this project, alongside with those from Bootstrap.

## JavaScript files

### **transactions.js**

This JavaScript file contains the function that allows the user to sort the transactions table by clicking the column headers.

## Python files

### **app.py**

This python file contains the main functions underpinning this project. It contains every route that is used for processing the data sent by the user through every form.

It contains the following functions:

1. login()
   - This functions manages the steps required to log the user into their account. It is executed when the route "/login" is accessed, either by POST method as well as by GET method. If the method is GET, the function will simply return the HTML page with the login form. If the method is POST, it means that the user filled the login form and submited. The function will validate the information entered by the user and either log them in or show an error message.

   - Obs.: In order to validate the login, this function is using the function **check_login()** contained in another python file (see **custom.py** down bellow)

2. register()
   - This function is executed when the route "/register" is accessed, by POST or GET method, and is responsible for managing users registration. It simply returns the registration page it the route is accessed via GET method. Otherwise, if the method is POST, then the user filled the registration form and submited. The function will validate the information entered by the user and either register them or show an error message if the validation is not successfull.

   - Obs.: In order to validate the login, this function is using the function **check_registration()** contained in another python file (see **custom.py** down bellow)

3. index()
   - This function is executed when the route "/" is accessed and the user is logged in. It will get from the database all the information about the transactions added by the current user, as well as information about every bank and transaction category. This information will be used to display to the user their transactions in the HTML page.

   - This functions also manages the filtering of transactions that the user can perform. When it is executed, it also checks wether the user has chosen to filter their transactions, so that the table can be shown accordingly.

4. add_transaction()
   - Executed when the route "/add_transaction" is accessed via POST method (meaning the user is trying to add a new transaction), this function will get the information entered by the user in the form and validate it. If it passes the validation, it will add the transaction info to the database and redirect the user to the route "/". Otherwise, it will show an error message.

5. deleteAll()
   - This simple function is executed whenever the user clicks the red button "Delete All Transactions", accessing the route "/deleteAll" via POST method. What it does is simply delete from the database every transaction made by this user, then it redirects to the route "/".

6. delete_transaction()
   - This function deletes an individual transaction chosen by the user to be deleted. It gets the id number of that transaction via FORM, and then deletes it from the database, redirecting the user to the route "/" afterwards.

6. budget()
   - When the user clicks the "Budgets" tab, they are redirected to the "/budget" route, triggering this function. Since the user can view their budget for any month of any year, the function needs to have the information about the period that the user is interested in viewing. By default, when the route is accessed via GET method, the function takes the current month and year as the time period to be displaied, unless the user has already chosen any different period. If the request method is POST, the function by default will get the time information given by the user.
   - The function will then get the dates for the first and last days of that month, and then query the database for every transaction made by the user that is in between those dates.
   - After that, for every transaction category, the function will calculate the total transacted in that month for that category.
   - Then the function will query the database for the budget information related to that period of time for that user.
   - Then, the function will return the page with all the information about the user's budget for that specific month.

7. addBudget()
   - Whenever the user makes any change to their budget information, this is the function responsible for updating that information. It gets the information given by the user, and then updates that information in the database, redirecting to the route "/budget" afterwards.

8. reports()
   - In order for the user to be able to see the total transacted for each category in any given month, this function is executed when they click the "Reports" tab, therefore accessing the "/reports" route.
   - If the request method is GET, meaning the user didn't send any information, it will display the report for the current year;
   - If the request method is POST, meaning the user have chosen some year via form and sent that information, the function will get the information for that year and render the page with the appropriate information.

9. logout()
   - This function simply clear the session from any information about the user that was logged before, and redirects to the login page.

10. deleteAccount()
    - This function allows the user to delete their account from the system, along with any information associated with them.

### **custom.py**

This python file contains the three functions used to validate user's registration and login, and also to get the last date of any month. These functions are:

1. check_registration()
   - This function takes four parameters to work: the database with users information, the username chosen by the user, the password, and the confirmation.
   - If the validation is successful, it will simply return the string "OK" in a variable called response. It is set as "OK", from the start, changing if any validation step is not successful.
   - First it is checked wheter the user has filled every fild from the registration form. Then, if the password and confirmation match. Finaly, it checks wheter this username is unique. If the three cases are true, it will return "OK", meaning the validaton was successful. Otherwise, it will return an apropriate response informing the user why the validation was not successful.

2. check_login()
   - This function takes three parameters to work: the database with users information, the username and the password.
   - This function returns a tuple of the following format: (boolean, string).
   - If the validation is successful, it will return with the first item of the tuple being True, and the second being the user's ID. Otherwise, the fist item will be False, and the second will be a string containing an error message to be displaied to the user.
   - First it is checked wheter the user has filled every fild from the login form. Then, if that username really exists and if the password hash matches that in the database.

3. get_last_day_of_month()
   - This function takes two parameters to work: the year, and a month name as a string.
   - It will return the last date from any given month or year given as parameters.

### **helpers.py**

This file contains two helping functions. Let's go through them:

1. apology()
   - This function assists the main python file generating the error messages for different scenarios, rendering the apology.html file with the image gotten from an URL and the error message.

2. login_required()
   - This function ensures that the routes that can only be accessed when there is a user logged in will not be accesssed otherwise, redirecting to the login page in that case.

## SQL files

There is one SQLite3 file in this project, containing multiple tables for different but related information. This database is accessed multiple times during the usage of this web application. The tables contained in this database are:

1. transactions
   - This table contains information about every transaction from every user.

2. categories
   - Each transacton category used in this application is stored in this table.

3. users
   - This table contains the information about every user registered.

4. budgets
   - This table contains the information entered by every user about their budgets.

5. banks
   - Here is where the information about the banks avaliable for the users are stored.