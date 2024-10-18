Campus Club Activity Management System
====

### Table of Contents
* Background
* Introduction
* Directory
* Install
* Usage
* Maintainers
* Contributing
* License


### Background
This project is a homework assignment for three freshmen students in China.


### Introduction
Our project is a system that mimics an automatic teller machine (ATM), developed using the Flask framework in PythonWeb, with data stored in MySQL and accessed via a web interface.  
The system can be broadly divided into seven parts: login function, homepage menu, balance inquiry, transfer business, financial management channel, recharge and payment, and cash withdrawal service.  
**NOTICE: We have only simulated the functions of the ATM machine, and there is no real money involved. This is purely a virtual feature.**


### Directory
In the project main folder, there are three subfolders:
1. The "static" folder stores static files.
2. The "templates" folder stores all the .html files.
3. The "views" folder stores all the .py files. (Each .py file corresponds to a .html file.)

### Install
1. Install Dependencies  
Flask==2.3.2  
Flask-Migrate==4.0.4  
Flask-SQLAlchemy==3.0.3

2. Database
Create a local MySQL database first.  
In the "sql.py" file and "setting.py" file, there are related settings for connecting to the database. You can modify them according to your own local database name and account password.  
Before using the system, you need to run the code for creating tables and writing initial data in "sql.py" (currently commented out). You need to delete the triple quotes and run it once, and then comment it out again.  
The login module in the system does not have the registration function.  
Users can only log in with existing data in the database. You can modify the content of creating tables in "sql.py" to add users.  

3. Run the Main File
Start the MySQL service and run the "manager.py" file to get the website URL

4. Open the Website to Use
Click the URL to enter and use the system. 
If you have installed successfully, you will see a login page.


### Usage
You can check out the small project we have created using Flask framework, and we will appriciated if you could give us some practical suggestions.



### Maintainers
@studyingWAWAYU  
@ZIE  
@mm-ss-dd  


### Contributing
Feel free to dive in Open an issue or submit PRs.  
flask-ATM-Simulator follows the Contributor Covenant Code of Conduct.
### License
 MIT License

