# Cloudflare DYNDNS Updater
This is a simple application to update Cloudflare DNS records with the public IP address of the internet connection you are running this application form.

Every minute the application will check if your public IP address has changed and if so it will update the Cloudflare DNS records.

Everything can be controlled from the configuration file.

## Installation

To install this application, you can choose to run it as a container, or you can run the script directly.

Whichever method you choose, you will need to create a configuration file first.

### Configuration

The configuration file is in the `.toml` format.
By default the script will look for the `config.toml` file in the `~/.config/cloudflare-dyndns-updater/` folder.
The location and name can be changed by setting the `SETTINGS_FILE` environment variable. 

```toml
account_id = "your_account_id"
api_token = "<your api_token>"

[zone_name."your-zone.com"]
records = ["record-one.your-zone.com", "record-two.your-zone.com"]

[zone_name."your-second-zone.com"]
records = ["record-one.your-second-zone.com", "record-two.your-second-zone.com"]
```

Above you see an example of the contents of the configuration file.

The `account_id` and `api_token` are used to authenticate to use the Cloudflare api with your account.
You will need to create an api token in the CloudFlare settings ```Manage account -> Account API tokens```

The `zone_name` is the name of the zone you want to update.  
`records` is a list of records you want to update.

You can add multiple zones and records by adding more sections to the file.

### Script

First make sure you have [UV](https://github.com/astral-sh/uv) and [Git](https://git-scm.com) installed on your machine, and you create the configuration file.

Next clone the repository.

```bash
git clone https://github.com/real-codemeteor/cloudflare-dyndns-updater.git
```

Navigate into the directory in which you cloned the repository.
```bash
cd cloudflare-dyndns-updater
```

Execute the following command, to create the vritual environment and install the dependencies.
```bash
uv sync
```

Execute the following command, to run the application.
```bash
uv run src/cloudflare_dyndns_updater/main.py
```

The application will keep on running until you stop it by pressing `CTRL+C`.

### Container

Cloudflare DYNDNS Updater is also available as a container image on Docker Hub.

For this example we use Docker, but you can use any container runtime you like.

Starting the container is as easy as running the following command from the folder where you have your ```config.toml``` file stored.

```bash
docker run -v ./config.toml:/config.toml realcodemeteor/cloudflare-dyndns-updater:1.1.1
```

The container will keep on running until you stop it by pressing `CTRL+C`.

## Support

If you like what I am doing and want to support me, you can donate via [PayPal](https://paypal.me/codemeteor).
