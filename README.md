# Typo : A typing test

### Description:
This is my CS50x final project. It is a simple typing test web application named Typo. Typo allows you to take typing tests to see your typing speed i.e. WPM(words per minute) and accuracy. Typo allows you to take typing tests with and without signing up. Taking tests by loging in allows you to see your stats and track your progress. You can see your average and best speed and accuracy and also the speed and accuracy of the latest test. This web application keeps track of your progress to help you in your journey to become a fast, accurate and confident typist.

### Tech Used:
- Python(Flask)
- SQlite
- JavaScript
- HTML, CSS
- Bootstrap

### Implementation:
#### How it works?:
The main idea behind it is simple. When the user opens the website, they directly land on the page where they can take the typing test. Without signing up or loging in the user can easily take the test to see their typing speed and accuracy. But the user also has the option to sign up and log in to track their stats.\
\
When the user requests the signup route via "POST" the username and password hash is stored in the database and also a separate row to store the users stats is created in the database.
The user can then log in user the username and password that they signed up with. After loging in, the user can access the stats page where they can view their best, last and average WPM(words per minute) and Accuracy.\
\
Each time the user takes a test the results are updated to the database via the updatestats route. During the calculation the test results are rounded down to the nearest integer value. You can press the reload button to take another test or to render a new quote before taking the test.

#### Main files:
- app.py - contains all the implementation of all the necessary processes like login, logout, signup, communication with the database.
- typing.db - this database contains two tables, one that stores the required users login info and the other that stores their stats.
- index.html - this html file contains the main template for the typing test.
- index.js - this javascript file contains all the main functionality like fetching the quote from API, rendering new quote and calculating the speed and accuracy.

#### Other files:
- styles.css - this file contains all the styling apart from bootstrap that are used in the project.
- layout.html - this file contains the basic layout of the web application that is used across all the web pages.
- logreg.html - this file contains the html for the login and register portal of the web application.
- stats.html - this contains html template for displaying the scores and stats of the user.

### Credits:
- [Quotable API](https://api.quotable.io) - this project uses the quotable API to generate random quotes of specified length for the user to type.
- [Memegen API](https://api.memegen.link) - memegen API is used in this project to generate apology messages when some error occur like incorrect password.
- [icons8](https://icons8.com/) - Icons for the web app are taken from this website.
- [Bootstrap](https://getbootstrap.com/) - Bootstrap framework is used to make this web application.
