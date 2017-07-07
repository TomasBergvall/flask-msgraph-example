# flask-msgraph-example

This is an example app using Microsoft Graph API to sign in users and a database repository to store information about the users. The database is also used to authorize users to the app.

Prerequisites
1. Visual Studio (developed using VS 2017 Pro)
2. Python Tools for Visual Studio (installed using the Visual Studio installer)
3. Anaconda 4.3.0 (but should work with any Python 3.x installation)
4. Setup app at <https://apps.dev.microsoft.com>, the important parts are
4.1 generate a new password
4.2 set redirect url to http://localhost:5000/login/authorized and the next line to http://localhost
4.3 Add User.Read to delegated graph properties

Create a file called config.py at /FlaskWebProject1/config.py with the following content

```python
import urllib.parse
class Config(object):
    DEBUG = True
    DEVELOPMENT = True
    APPLICATION_NAME = 'flask-msgraph-example'

    MS_CLIENT_ID = 'YOUR_APPLICATION_ID'
    MS_CLIENT_SECRET = 'YOUR_APPLICATION_PASSWORD'

    SECRET_KEY = 'super secret key'

    # Automatically recognized by flask_sqlalchemy to connect to the database
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc:///?odbc_connect={}'.format(urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};SERVER=YOUR_SERVER_NAME;DATABASE=YOUR_DATABASE;UID=YOUR_DATABASE_USER;PWD=YOUR_DATABASE_USER_PASSWORD")) 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```
Replace these values
- YOUR_APPLICATION_ID
- YOUR_APPLICATION_PASSWORD
- YOUR_SERVER_NAME
- YOUR_DATABASE
- YOUR_DATABASE_USER
- YOUR_DATABASE_USER_PASSWORD
 
 Create a database with the same name as you replaced YOUR_DATABASE. Create a user (YOUR_DATABASE_USER) that can log into the database with the password YOUR_DATABASE_USER_PASSWORD. Make sure that the user has admin rights on the database
 
 Run models.py to set up the tables in the database
 NOTE: to allow users access to the application they need to be linked to the application in the AccessControl table. This currently needs to be done manually after the users has been created in the UserProfile table, which happens after the first login attempt. 

```sql
insert into dbo.access_control
(user_id, web_application_id)
select up.id, wa.web_application_id
from dbo.user_profile up 
cross join dbo.web_application wa 
where up.email = 'john.doe@example.com'
  and wa.web_application_name = 'flask-msgraph-example'
```
 
