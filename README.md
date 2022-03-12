# Gym 
Our web application  is built using Django, Bootstrap, and JavaScript.
Users don't have to sign up to view the gym branches,trainers, classes and clinics. they will need to login to be able to subscribe to classes and have notificatons about our new events , classes and offers . hope you enjoy it.

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
[settings.zip]()
- Make sure to install
    -   `pip install fontawesomefree`
    -   `pip install pymysql`
    -    `python -m pip install Pillow`
    -    `pip install django twilio python-dotenv`
    -    `pip install channels`
    -    `pip install channels-redis`
    -    `pip install asgiref`
    -    `pip install celery`
    -    `pip install django-celery-beat`
    -    `pip install -U django-celery-results`
    -    `pip install django-celery-results`
    -    `pip install django-allauth`
- Create database called gymdb in MySQL, and use the USERNAME and PASSWORD for your database in settings.py.
- To be able to send emails, make sure to change email settings in settings.py which EMAIL_HOST_USER and EMAIL_HOST_PASSWORD.
- The email you will use, you must allow low security apps from its settings.


## Usage
Once the project is all set, activate your env, run the server, and go to url:http://127.0.0.1:8000/

## Features

For Admins they can:
-  CRUD on Branches , Offers ,Classes ,Trainers and Events.
-  Send  Notifications To all Users about New Branches , Offers , Classes ,Trainers and Events.

For logged in Users they can:
- Can Login with their Google Accounts 
- Edit their own profile 
- See the Notification about any New Event, offers, classes and Trainers.
- Subscribe/Unsubscribe to any Class and add it to Favorites.



## Demo



## Authors

- Created by 
    - [@ranawael1](https://github.com/ranawael1)
    - [@shahdhesham5](https://github.com/shahdhesham5 ) 
    - [@sohila-mo](https://github.com/sohila-mo) 
    - [@shadybassily](https://github.com/shadybassily)
    - [@sohybnaim](https://github.com/sohybnaim)



