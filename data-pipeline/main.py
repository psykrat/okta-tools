import os
import requests
from google.cloud import bigquery
from flask import request

OKTA_BASE_URL = os.environ["OKTA_BASE_URL"]
OKTA_API_TOKEN = os.environ["OKTA_API_TOKEN"]

BIGQUERY_PROJECT_ID = os.environ["BIGQUERY_PROJECT_ID"]
BIGQUERY_DATASET = os.environ["BIGQUERY_DATASET"]
BIGQUERY_TABLE = os.environ["BIGQUERY_TABLE"]

bigquery_client = bigquery.Client()

def get_app_details(app_id):
    url = f"{OKTA_BASE_URL}/api/v1/apps/{app_id}"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'SSWS {OKTA_API_TOKEN}'
    }
    response = requests.get(url, headers=headers)

    if not response.ok:
        print(f"Error fetching app details for app_id {app_id}: {response.text}")
        return None

    return response.json()

def get_okta_group_info(group_id):
    url = f"{OKTA_BASE_URL}/api/v1/groups/{group_id}"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'SSWS {OKTA_API_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_okta_app_groups(app_id):
    url = f"{OKTA_BASE_URL}/api/v1/apps/{app_id}/groups"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'SSWS {OKTA_API_TOKEN}'
    }
    response = requests.get(url, headers=headers)

    if not response.ok:
        print(f"Error fetching app groups for app_id {app_id}: {response.text}")
        return []

    data = response.json()

    if not isinstance(data, list):
        print(f"Unexpected response format for app_id {app_id}: {data}")
        return []

    group_ids = [group['id'] for group in data]

    # Retrieve group information for each group ID
    group_infos = [get_okta_group_info(group_id) for group_id in group_ids]
    return group_infos

def upload_to_bigquery(rows):
    table_ref = bigquery_client.dataset(BIGQUERY_DATASET).table(BIGQUERY_TABLE)
    table = bigquery_client.get_table(table_ref)

    # Insert new rows
    errors = bigquery_client.insert_rows_json(table, rows)
    if errors:
        raise Exception(f"Error uploading rows to BigQuery: {errors}")

def okta_apps_groups_to_bigquery(request):
    # Get app_id from the request JSON body
    data = request.get_json()
    app_id = data.get('app_id')

    if not app_id:
        return "Missing app_id in the request body", 400

    app = get_app_details(app_id)
    if not app:
        return f"No app found with id: {app_id}", 404

    app_name = app['name']
    app_label = app['label']
    groups = get_okta_app_groups(app_id)

    results = []
    for group in groups:
        result = {
            'app_id': app_id,
            'app_name': app_name,
            'app_label': app_label,
            'group_id': group['id'],
            'group_name': group['profile']['name'],
            'group_description': group['profile'].get('description', '')
        }
        results.append(result)

    upload_to_bigquery(results)

    return f"Successfully uploaded Okta app {app_id} and groups data to BigQuery", 200
