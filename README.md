# Firebolt Query History Monitoring Dashboard

Grafana dashboard to create a tool to monitor their Firebolt instances using `information_schema.running_queries` and `information_schema.query_history`.

# Grafana

The Grafana implementation uses the Infinity Pugin - https://grafana.com/grafana/plugins/yesoreyeram-infinity-datasource/

To install using docker:-

```bash
docker run -d -p 3000:3000 --name=grafana -e "GF_INSTALL_PLUGINS=yesoreyeram-infinity-datasource" grafana/grafana-oss
```

Then connect using `localhost:3000`.  On first connection you will be prompted to login, the default username/password is `admin/admin` *strongly recommend that you change this.....*

You will then need to create a grafana service account with admin privileges and generate an API token for that service account.  The API token should be stored securely, and set as the `GRAFANA_API_KEY` environment variable when running the scripts below.

## Python setup scripts

THe following scripts allow you to setup and deploy the datasources and dashboards to your Grafana instance.

Prerequisites can be installed via `pip install -r ./grafana_monitor/datasource_config/requirements.txt`

### Datasources

The Infinity plugin allows you to easily create visuals via the api's JSON response.  To configure a data source you will need to enter the following.

* Name - whatever you wish to call the connection
* Authentication:
    * Auth Type - Bearer Token
    * Bearer Token - A valid token from the Firebolt auth api (more on this below)
    * Allowed Hosts - the engine url(s) for running queries

Optionally you can also provide the database via the `url parameters` setting as a Key: `Database`, Value: `database_name` pair.

You can provision this using [the datasource_config script](grafana_monitor/datasource_config/datasource_config.py); N.B. pass in the engine endpoint _without_ https:// (available by copying from the UI).

```bash
export FIREBOLT_USER=[your-firebolt-user]
export FIREBOLT_PASSWORD=[your-firebolt-password]
export GRAFANA_BASE_URL=[your-grafana-instance-url]
export GRAFANA_API_TOKEN=[your-grafana-service-account-token]

python grafana_monitor/datasource_config/datasource_config.py create-datasource [DATA_SOURCE_NAME] [DATABASE_NAME] [ENGINE_ENDPOINT]
```

### Updating the Bearer Token

As the data source connection is reliant on a bearer token provided by the auth api, which are valid for 12 hours, these will need to be updated periodically.  This can be done using the Grafana api; for ease a [python script](grafana_monitor/update_bearer_token/update_bearer_token.py) has been included.  In order to use, configure a Service Account in Grafana with permissions on your datasource, and then run with the following environment variabales:-

```bash
export FIREBOLT_USER=[your-firebolt-user]
export FIREBOLT_PASSWORD=[your-firebolt-password]
export GRAFANA_BASE_URL=[your-grafana-instance-url]
export GRAFANA_API_TOKEN=[your-grafana-service-account-token]

python grafana_monitor/datasource_config/datasource_config.py update-datasource-bearer-token [DATA_SOURCE_NAME] [DATABASE_NAME]
```

### Deploy the dashboard

A precreated dashboard can be configured by running the datasource_config.py script, passing in the engine name and previously configured data source.  N.B. pass in the engine endpoint _without_ https:// (available by copying from the UI).

```bash
export GRAFANA_BASE_URL=[your-grafana-instance-url]
export GRAFANA_API_TOKEN=[your-grafana-service-account-token]

python grafana_monitor/datasource_config/datasource_config.py create-dashboard [DATA_SOURCE_NAME] [ENGINE_ENDPOINT]
```

### Script Help File

The help file for the scripts can be accessed using the `--help` switch.

```
python grafana_monitor/datasource_config/datasource_config.py --help

Usage: datasource_config.py [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.

Commands:
  create-dashboard
  create-datasource
  update-datasource-bearer-token
```

```
  python grafana_monitor/datasource_config/datasource_config.py create-datasource --help

  Usage: datasource_config.py create-datasource [OPTIONS] DATASOURCE_NAME
                                              DATABASE_NAME
                                              ENGINE_ENDPOINTS...

Arguments:
  DATASOURCE_NAME      [required]
  DATABASE_NAME        [required]
  ENGINE_ENDPOINTS...  [required]

Options:
  --is-default / --no-is-default  [default: no-is-default]
  --firebolt-access-token TEXT
  --help                          Show this message and exit.
```

```
python grafana_monitor/datasource_config/datasource_config.py create-dashboard --help

Usage: datasource_config.py create-dashboard [OPTIONS] DATASOURCE_NAME
                                             ENGINE_ENDPOINT

Arguments:
  DATASOURCE_NAME  [required]
  ENGINE_ENDPOINT  [required]

Options:
  --dashboard-name TEXT  [default: Firebolt_Monitor]
  --help                 Show this message and exit.
```

```
python grafana_monitor/datasource_config/datasource_config.py update-datasource-bearer-token --help

Usage: datasource_config.py update-datasource-bearer-token
           [OPTIONS] DATASOURCE_NAME DATABASE_NAME

Arguments:
  DATASOURCE_NAME  [required]
  DATABASE_NAME    [required]

Options:
  --firebolt-access-token TEXT
  --help                        Show this message and exit.
```