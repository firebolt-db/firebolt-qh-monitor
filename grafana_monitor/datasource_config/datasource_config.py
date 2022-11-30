from httpx import get, post, put
from io import open
from json import load, loads, dumps
from os import getenv
import typer

app = typer.Typer()

def login_to_firebolt() -> str:

    login_url = 'https://api.app.firebolt.io/auth/v1/login'
    login_headers = {"content-type":"application/json;charset=UTF-8"}

    login_request = post(url=login_url,
                        json = {"username":getenv("FIREBOLT_USER"),"password":getenv("FIREBOLT_PASSWORD")},
                        headers=login_headers)

    access_token = loads(login_request.content.decode("utf-8"))["access_token"]

    return access_token

@app.command()
def update_datasource_bearer_token(datasource_name, database_name, firebolt_access_token=None):

    if not firebolt_access_token:
        firebolt_access_token = login_to_firebolt()

    grafana_header = {"authorization": f"Bearer {getenv('GRAFANA_API_TOKEN')}", "content-type":"application/json;charset=UTF-8"}
    grafana_datasource_url = f"{getenv('GRAFANA_BASE_URL')}/api/datasources/name/{datasource_name}"

    firebolt_datasource_resp = get(url=grafana_datasource_url, headers=grafana_header)
    full_datasource = loads(firebolt_datasource_resp.content.decode("utf-8"))
    firebolt_datasource_id = full_datasource["uid"]

    update_token_url = f"{getenv('GRAFANA_BASE_URL')}/api/datasources/uid/{firebolt_datasource_id}"

    new_data = {
                "id": full_datasource["id"],
                "uid": full_datasource["uid"],
                "orgId": full_datasource["orgId"],
                "name": full_datasource["name"],
                "type": full_datasource["type"],
                "access": full_datasource["access"],
                "url": full_datasource["url"],
                "user": full_datasource["user"],
                "database": full_datasource["database"],
                "basicAuth": full_datasource["basicAuth"],
                "basicAuthUser": full_datasource["basicAuthUser"],
                "withCredentials": full_datasource["withCredentials"],
                "isDefault": full_datasource["isDefault"],
                "jsonData": full_datasource["jsonData"],
                "secureJsonData": {
                        "bearerToken": firebolt_access_token,
                        "secureQueryValue1": database_name
                    }
    }

    update_bearer_token = put(url=update_token_url, data=dumps(new_data), headers=grafana_header)
    update_bearer_token.raise_for_status()

    ###add test to get a new uuid

@app.command()
def create_datasource(datasource_name, database_name, engine_endpoints: list[str], is_default: bool = False, firebolt_access_token=None):

    if not firebolt_access_token:
        firebolt_access_token = login_to_firebolt()

    grafana_header = {"authorization": f"Bearer {getenv('GRAFANA_API_TOKEN')}", "content-type":"application/json;charset=UTF-8"}
    grafana_datasource_url = f"{getenv('GRAFANA_BASE_URL')}/api/datasources"

    datasource_config = {
        "name": datasource_name,
        "type": "yesoreyeram-infinity-datasource",
        "access": "proxy",
        "url": "",
        "user": "",
        "database": "",
        "basicAuth": False,
        "basicAuthUser": '',
        "withCredentials": False,
        "isDefault": is_default,
        "jsonData": {"allowedHosts": [f"https://{engine_endpoint}" for engine_endpoint in engine_endpoints],
                    "auth_method": "bearerToken",
                    "global_queries": [],
                    "oauthPassThru": False,
                    "secureQueryName1": "database"
                    },
        "secureJsonData": {
                        "bearerToken": firebolt_access_token,
                        "secureQueryValue1": database_name
                    },
        "readOnly": False
    }

    grafana_datasource_resp = post(url=grafana_datasource_url, data=dumps(datasource_config), headers=grafana_header)
    grafana_datasource_resp.raise_for_status()

    grafana_header = {"authorization": f"Bearer {getenv('GRAFANA_API_TOKEN')}", "content-type":"application/json;charset=UTF-8"}
    grafana_datasource_url = f"{getenv('GRAFANA_BASE_URL')}/api/datasources/name/{datasource_name}"

    firebolt_datasource_resp = get(url=grafana_datasource_url, headers=grafana_header)
    full_datasource = loads(firebolt_datasource_resp.content.decode("utf-8"))
    firebolt_datasource_id = full_datasource["uid"]

    edit_datasource_url = f"{getenv('GRAFANA_BASE_URL')}/datasources/edit/{firebolt_datasource_id}"

    update_datasource = get(url=edit_datasource_url , headers=grafana_header)
    update_datasource.raise_for_status()


@app.command()
def create_dashboard(datasource_name, engine_endpoint, dashboard_name = 'Firebolt_Monitor'):

    grafana_header = {"authorization": f"Bearer {getenv('GRAFANA_API_TOKEN')}", "content-type":"application/json;charset=UTF-8"}
    grafana_datasource_url = f"{getenv('GRAFANA_BASE_URL')}/api/datasources/name/{datasource_name}"

    firebolt_datasource_resp = get(url=grafana_datasource_url, headers=grafana_header)
    full_datasource = loads(firebolt_datasource_resp.content.decode("utf-8"))
    firebolt_datasource_id = full_datasource["uid"]

    with open('./grafana_monitor/config/dashboard.json') as dashboard_f:
        dashboard_dict = load(dashboard_f)
        dashboard_dict["id"] = None
        dashboard_dict["uid"] = None
        dashboard_dict["title"] = dashboard_name
        for panel in dashboard_dict["panels"]:
            panel["datasource"]["uid"] = firebolt_datasource_id
            for target in panel["targets"]:
                target["url"] = f"https://{engine_endpoint}"
                target["datasource"]["uid"] = firebolt_datasource_id

    grafana_dashboard_url = f"{getenv('GRAFANA_BASE_URL')}/api/dashboards/db"
    grafana_dashboard_body = {"dashboard": dashboard_dict,
                              "overwrite": True}

    dashboard_create_resp = post(url=grafana_dashboard_url, data=dumps(grafana_dashboard_body), headers=grafana_header)
    dashboard_create_resp.raise_for_status()

if __name__ == '__main__':
    app()
