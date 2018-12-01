# SSOP (Safe & Secure Owner Password)

# Content of the repository

- **ssop2** : The main platform where registration and authentication process occurs.

- **voting-site** : I's a voting site we will use as a demo website to authenticate and identify users with our platform. It's a webapp where
  people can vote for a Hackathon team to win.

- **Presentación PPT y PDF** : In this folder you can encounter the presentation of the proposal we made during the first day: https://github.com/CyberWatcherOrg/SSOP/tree/master/Presentacion_Hackathon

---

# SSOP

## About

SSOP is a 2-factors authentication and identity manager platform. Any user can register in this platform to create an identity.

## Features

* 2-factors authentication (credential and a PIN sent to the user phone number)
* SSOP runs as an OpenID provider, so it can be integrated with any website to provide authentication and identity management

## Requirements

* Python >= 3.xa
* Django 1.11.8
* Some Python libraries:
  * [django-oidc-provider](https://github.com/juanifioren/django-oidc-provider) module
  * [Twilio](https://www.twilio.com/docs/) module to send SMS
  * [Django REST Framework](https://www.django-rest-framework.org) module

```bash
user@machine:$ apt install python3
user@machine:$ apt install python3-pip
user@machine:$ pip3 install twilio django-oidc-provider django-rest-framework
```

## Installation

## Usage

You must to run the site:

```bash
user@machine:$ python3 manage.py runserver
```

## Documentacion

## Thanks

## Authors

Miguel Ángel Langarita <miguel.angel.langarita@gmail.com>
Javier Manrique <jmanriquepellejero@gmail.com>
Santiago Faci <santiago.faci@gmail.com>
