# HealthClub
Our web application  is built using Django,Django restframework, React, HTML, CSS, Bootstrap, JavaScript and JQuery.
Users don't have to sign up to view the GYM branches,trainers, classes and clinics. 
They will need to login to be able to subscribe to classes, apply for events and receive notificatons about our new events, classes and offers. Hope you enjoy it.

## Content
* [Setup](#setup)
* [Usage](#usage)
* [Features](#features)
* [Demo](#demo)
* [Authors](#authors)



## Setup

```bash
git clone https://github.com/ranawael1/GYM.git
```
- The project doesn't include the settings.py, but you can download it from this link.
[settings.zip](https://github.com/shahdhesham5/Django_Blog/files/8308159/settings.zip)
- Make sure to install
    -   `pip install fontawesomefree`
    -   `pip install pymysql`
    -   `python -m pip install Pillow`
    -   `pip install django-phonenumber-field[phonenumberslite]`
    -   `pip install django twilio python-dotenv`
    -   `pip install asgiref`
    -   `pip install celery==3.1.18`
    -   `pip install redis==3.2.0`
    -   `pip freeze > requirements.txt`
    -   `pip install django-celery-beat`
    -   `pip install django-celery-results`
    -   `pip install django-allauth`
    -   `pip install django-paypal`
- Create database called gymdb in MySQL(or any database engine you want), and use the USERNAME and PASSWORD for your database in settings.py.
- To be able to send emails, be sure to change email settings in settings.py which EMAIL_HOST_USER and EMAIL_HOST_PASSWORD.
- The email you will use, you must allow low security apps from its settings.
- To be able to get the payment funds to your account, be sure to change PAYPAL_RECEIVER_EMAIL in settings.py.


## Usage
Once the project is all set, activate your env, run the server, and go to url:http://127.0.0.1:8000/

## Features

For Guests:

-  View Data

For Admins they can:
-  CRUD on Users ,Branches , Offers ,Classes ,Trainers and Events.

For logged in Users they can:

- View Data
- Can Login with their Google Accounts 
- Edit their own profile 
- Receive Notification about any New Event, offers, classes and Trainers.
- Subscribe/Unsubscribe to any Class and add it to Favorites.
- Reserve a place in an event
- Make Payment



## Demo



## Authors

- Created by 
    - [@ranawael1](https://github.com/ranawael1)
    - [@shahdhesham5](https://github.com/shahdhesham5 ) 
    - [@sohila-mo](https://github.com/sohila-mo) 
    - [@shadybassily](https://github.com/shadybassily)
    - [@sohybnaim](https://github.com/sohybnaim)



