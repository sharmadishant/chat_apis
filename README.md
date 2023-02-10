
# CHat_APIs 

To complete this assignment, you will need to use the Django Rest Framework (DRF) for building the web services and SQLite as the database. Here is a high-level overview of the steps you can follow:

Set up a Django project and install DRF
Create a model for User, which will store the user's details such as username, password, etc.
Implement authentication APIs for login and logout.
Create a model for Group and another for GroupMessage to store the groups and messages respectively.
Create API views for managing users (create, edit) that can only be accessed by an admin user.
Create API views for managing groups (create, delete, search, add members, etc) and sending messages in a group that can be accessed by any user.
Add a "like" feature to messages, allowing users to like messages.
Test the APIs using a tool such as Postman.
Note: This is just a high-level overview, and you will need to implement various details and optimizations while building the application.

Requirement
aiohttp==3.8.3
aiosignal==1.3.1
asgiref==3.6.0
async-timeout==4.0.2
attrs==22.2.0

certifi==2022.12.7
charset-normalizer==2.1.1
Django==4.1.5
django-cors-headers==3.13.0
django-utils-six==2.0
djangorestframework==3.14.0
djangorestframework-simplejwt==5.2.2
djongo==1.3.6
dnspython==2.3.0
frozenlist==1.3.3
idna==3.4
mongoengine==0.26.0
multidict==6.0.4
openai==0.26.1
Pillow==9.4.0
PyJWT==2.6.0
pymongo==3.12.3
pytz==2022.7.1
requests==2.28.2
sqlparse==0.2.4
tqdm==4.64.1
urllib3==1.26.14
yarl==1.8.2
