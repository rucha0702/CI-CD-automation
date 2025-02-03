import requests
import json
import os

# Fetch SonarQube issues with pagination
def fetch_sonarqube_issues():
    sonarqube_url = os.getenv('SONARQUBE_URL','http://54.160.99.203:9000/api/issues/search')
    component_key = os.getenv('SONARQUBE_COMPONENT_KEY','webgoat')
    all_issues = []
    page = 1
    page_size = 500  # Max allowed by SonarQube

    while True:
        params = {
            "componentKeys": component_key,
            "resolved": "false",
            "ps": 100,
            "p": 1
        }
        response = requests.get(sonarqube_url, params=params)
        #response.raise_for_status()  # Raise HTTP errors
        data = response.json()
        issues = data.get('issues', [])
        all_issues.extend(issues)
        
        # Break if no more pages
        if len(issues) < page_size:
            break
        page += 1

    return all_issues

# Upload to DefectDojo
def upload_to_defectdojo(issues):
    defectdojo_url = os.getenv('DEFECT_DOJO_URL','https://demo.defectdojo.org/api/v2/import-scan/') 
    api_key = os.getenv('548afd6fab3bea9794a41b31da0e9404f733e222')
    engagement_id = os.getenv('14')

    headers = {"Authorization": f"Token {api_key}"}
    data = {
        "engagement": engagement_id,
        "scan_type": "SonarQube Scan",
        "minimum_severity": "Info"
    }
    files = {'file': ('sonarqube_issues.json', json.dumps(issues), 'application/json')}
    response = requests.post(defectdojo_url, headers=headers, data=data, files=files)
    response.raise_for_status()
    return response

if __name__ == "__main__":
    issues = fetch_sonarqube_issues()
    upload_response = upload_to_defectdojo(issues)
    print(f"Upload successful: {upload_response.status_code}")
