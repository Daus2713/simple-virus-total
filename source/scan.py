import json
import mimetypes

import requests

from source import analysis


def url_scan(target, myapi_key, nscan_api, mode=None):
    link = nscan_api.get("api-link")
    headers = nscan_api.get("headers", {})
    headers["x-apikey"] = myapi_key

    # For file scan
    if "file" in mode:
        mime_type, _ = mimetypes.guess_type(target)

        if mime_type is None:
            mime_type = "application/octet-stream"  # Default MIME type if detection fails

        target_scan = {"file": (target, open(target, "rb"), mime_type)}
        response_scan = requests.post(link, files=target_scan, headers=headers)
        print(response_scan)
    else:
        target_scan = {"url": target}
        # Send URL for scanning
        response_scan = requests.post(link, headers=headers, data=target_scan)

    try:
        response_data = response_scan.json()
    except json.JSONDecodeError:
        print("Error decoding JSON response:", response_scan.text)
        return

    analysis_id = None
    if response_scan.status_code == 200:
        analysis_id = response_data.get('data', {}).get('id')
        if analysis_id:
            print("Scan request successful. Analysis ID:", analysis_id)
        else:
            print("Analysis ID not found in response:", response_data)
    else:
        print("Failed to scan URL:", response_data)

    return analysis_id


def start_url(target, mode, keylist=None, output_name=None):
    try:
        # Reading the API key
        with open('myapikey.txt', 'r') as file:
            myapi_key = file.read().strip()

        # Reading the JSON configuration
        with open('source/VTAPI.json', 'r') as file:
            apijson = json.load(file)
            if "file" in mode:
                filejson = apijson.get("files", {})
            else:
                urljson = apijson.get("url", {})
            analysisjson = apijson.get("analysis_file_url", {})

    except FileNotFoundError as e:
        print(f"The file was not found: {e.filename}")
        return
    except json.JSONDecodeError:
        print("Error decoding JSON.")
        return

    results = None
    if "scan" in mode:
        if "file" in mode:
            nscan_api = filejson.get("scan-file", {})
        else:
            nscan_api = urljson.get("scan-url", {})
        analysis_id = url_scan(target, myapi_key, nscan_api, mode)
        analysis_api = analysisjson.get("analysis", {})

        if "output" in mode:
            results = analysis.get_analysis(analysis_api, analysis_id, myapi_key, mode, keylist, output_name)

        elif "normal" in mode:
            results = analysis.get_analysis(analysis_api, analysis_id, myapi_key, mode, keylist)
            print(results)

    return results
