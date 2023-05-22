# Okta to BigQuery Data Pipeline

This script provides an API endpoint that fetches data from Okta, specifically about apps and groups, and stores this data in Google BigQuery. It has been designed to be deployed as a Flask application. The request to this endpoint should contain the Okta app_id in the JSON body.

## Requirements

- Python 3.7 or higher
- Google Cloud SDK
- Okta API token with necessary permissions
- Flask
- Google Cloud BigQuery
- Okta
- Requests

You can install the necessary Python dependencies with pip:

```
pip install flask google-cloud-bigquery requests
```

## Environment Variables

This script requires the following environment variables:

- `OKTA_BASE_URL`: The base URL of your Okta instance.
- `OKTA_API_TOKEN`: The API token for Okta with necessary permissions.
- `BIGQUERY_PROJECT_ID`: The ID of your Google Cloud project.
- `BIGQUERY_DATASET`: The ID of your dataset in BigQuery.
- `BIGQUERY_TABLE`: The ID of your table in BigQuery.

## Functions

This script contains several functions:

- `get_app_details(app_id)`: Fetches details about a specific app from Okta.
- `get_okta_group_info(group_id)`: Fetches information about a specific group from Okta.
- `get_okta_app_groups(app_id)`: Fetches all groups related to a specific app in Okta.
- `upload_to_bigquery(rows)`: Uploads a list of rows to a specific table in BigQuery.
- `okta_apps_groups_to_bigquery(request)`: The main function that orchestrates the fetching of data from Okta and uploading it to BigQuery. This is set up to handle a POST request in a Flask application.

## API Endpoint

This script exposes one API endpoint:

- `POST /okta_apps_groups_to_bigquery`

The request body should be a JSON object with the following structure:

```json
{
  "app_id": "your-app-id"
}
```

The response will be a message indicating whether the operation was successful and a HTTP status code.

## Running the Script

To run this script as a Flask application, you would typically create a `app.py` file in the same directory as this script, with the following content:

```python
from flask import Flask, request
from your_script import okta_apps_groups_to_bigquery

app = Flask(__name__)

@app.route('/okta_apps_groups_to_bigquery', methods=['POST'])
def handle_request():
    return okta_apps_groups_to_bigquery(request)
```

You can then run your Flask app with:

```
export FLASK_APP=app.py
flask run
```

## Error Handling

This script has basic error handling for failed API requests and failed uploads to BigQuery. It prints errors to the console and, in case of the main function, returns a HTTP 400 or 404 status code for specific errors.
