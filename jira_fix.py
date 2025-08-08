# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import os

# Validate environment variables
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

if not JIRA_USERNAME or not JIRA_API_TOKEN:
    print("Error: JIRA_USERNAME and JIRA_API_TOKEN environment variables must be set")
    exit(1)

issueIdOrKey = "OPS-1987224"

url = f"https://criteo.atlassian.net/rest/api/2/issue/{issueIdOrKey}"

auth = HTTPBasicAuth(JIRA_USERNAME, JIRA_API_TOKEN)

headers = {
    "Accept": "application/json"
}

try:
    # Use GET request instead of POST for retrieving issue data
    response = requests.get(
        url,
        headers=headers,
        auth=auth
    )
    
    # Check if the request was successful
    response.raise_for_status()
    
    print(f"Status Code: {response.status_code}")
    print(json.dumps(response.json(), sort_keys=True, indent=4, separators=(",", ": ")))
    
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response content: {response.text}")
except requests.exceptions.RequestException as req_err:
    print(f"Request error occurred: {req_err}")
except json.JSONDecodeError as json_err:
    print(f"JSON decode error: {json_err}")
    print(f"Raw response: {response.text}")
except Exception as err:
    print(f"An unexpected error occurred: {err}")