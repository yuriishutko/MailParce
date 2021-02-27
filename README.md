# MailParce

This is a simple project that give some information about preparing new epmployees and send it to telegram bot using information from mailbox.
This sample can be useful for system administrators or helpdesk administrators.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


### Prerequisites

You need [docker](https://docs.docker.com/engine/install/ubuntu/) and [docker-compose](https://docs.docker.com/compose/install/) to be installed on your PC


### Installing

Using docker containers
In this case we use [docker-compose.yml](https://github.com/YuriiShutko/MailParce/blob/master/docker-compose.yml) file that will help us to combine our main container with telegram bot that will be built from /app/Dockerfile and mysql database from dockerhub (in my case this is mysql:8.0.1).
First of all we need to clone this repository locally:
```
git clone https://github.com/YuriiShutko/MailParce.git
```
Create .env file near docker-compose.yml using sample file named example.env.

Then we use only one command to make our bot running:
```
docker-compose up -d --build
```

## Authors

* **Yurii Shutko** - *Initial work* - [YuriiShutko](https://github.com/YuriiShutko)


## License

This project is licensed under the MIT License.


