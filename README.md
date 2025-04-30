# Cloudflare DYNDNS Updater
This is a simple application to update Cloudflare DNS records with the public IP address of the internet connection you are running this application form.

Every minute the application will check if your public IP address has changed and if so it will update the Cloudflare DNS records.

Everything can be controlled from the configuration file.

## Installation

To install this application, you can choose to run it as a container, or you can run the script directly.

Whichever method you choose, you will need to create a configuration file.

## Configuration

The configuration file is in the .toml format.
By default the script will look for the config.toml file in the ~/.config/cloudflare-dyndns-updater/ folder.
The location and name can be changed by setting the SETTINGS_FILE environment variable. 

```toml
auth_email = "your@mail.com"
auth_key = "<authkey found in you cloudflare account>"

[zone_name."your-zone.com"]
records = ["record-one.your-zone.com", "record-two.your-zone.com"]

[zone_name."your-second-zone.com"]
records = ["record-one.your-second-zone.com", "record-two.your-second-zone.com"]
```

Above you see an example of the contents of the configuration file.

The `auth_email` and `auth_key` are the credentials for your Cloudflare account.

The `zone_name` is the name of the zone you want to update.
The `records` is a list of the records you want to update.

You can add multiple zones and records by adding more sections to the file.

### Script

First make sure you have [UV](https://github.com/astral-sh/uv) and [Git](https://git-scm.com) installed on your machine.

### Container



## Requirements
This script runs inside a Docker container so you will need to have Docker installed on the machine where you want to run this script on.  
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
version: '3'
services:
  cloudflare-dyndns-updater:
    image: registry.gitlab.com/codemeteor/cloudflare-dyndns-updater:latest
    container_name: cloudflare-dyndns-updater
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
   
When you want to stop the application you can do so running the following command.

```
docker-compose down
```
