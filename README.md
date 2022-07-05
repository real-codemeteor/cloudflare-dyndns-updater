# Cloudflare DYNDNS Updater
This is a simple script to update one or more DNS records on Cloudflare with the public IP of the internet connection you are running this script on.

## Requirements
This script runs inside a Docker container so you will need to have Doekcer installed on the machine where you want to run this script on.  
It's also recomended that you use Docker Compose for running the script.

## Installation
Start by creating two folder. One folder will contain the configuration file, and another one will contain the log files.

```
mkdir /Appdata/cloudflare-dyndns-updater/config
mkdir /Appdata/cloudflare-dyndns-updater/logs
```
Now that we have our folders we can create our settings file.  
In the config folder create a file called `settings.yaml` and give it the following contents.
```
auth_email: your@mail.com
auth_key: <authkey fount in you cloudflare account>
zone_name: your-zone.com
records:
  - record-one.your-zone.com
  - record-two.your-zone.com
```
Make sure that you replace the values with the aproiate once.  
You can add and remove as much records as you like.

Next thing is for you to create a Docker Compose file.  
Choose location where you want to store your Docker Compose file and create a new file called `docker-compose.yml`.  
Give your Docker Compose file the following content.
```
services:
  cloudflare-dnydns-updater:
    image: registry.gitlab.com/codemeteor/cloudflare-dyndns-updater:latest
    container_name: cloudflare-dnydns-updater
    volumes:
      - /Appdata/cloudflare-dyndns-updater/config:/app/config
      - /Appdata/cloudflare-dyndns-updater/logs:/app/logs
    restart: unless-stopped
```
Make sure that you change the paths in the Docker Compose file to the config and logs folders to the paths you created.  
  
Lastly we can start the container usuing the following command, ran from the location where you have your Docker Compose file is located.
```
docker-compose up -d
```
## Usage
This a simple case of "install and forget".  
The application will run in the background every minute. When a change in the public IP address is detected it will update the records.  
   
When you want to stop the application you can do so running the following command from the location where the Docker Compose file is located.

```
docker-compose down -d
```