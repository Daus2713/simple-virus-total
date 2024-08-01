import sys
import requests
import time

from source.result import get_url_result


def write_analysis(text, output_name):
    file_path = f'saved/{output_name}.txt'
    with open(file_path, 'w') as file:
        file.write(text)

    return file_path


def get_analysis(analysis_api, analysis_id, myapi_key, mode, keylist=None, output_name=None):
    # Access the 'api-link' key from the dictionary
    url_analyses = analysis_api.get("api-link") + analysis_id
    print(url_analyses)

    # Get headers and add the API key
    headers = analysis_api.get("headers", {})
    headers["x-apikey"] = myapi_key

    wait_count = 0
    while True:
        # Get the analysis results

        response_analysis = requests.get(url_analyses, headers=headers)
        response_analysis_data = response_analysis.json()

        if response_analysis_data.get("data", {}).get("attributes", {}).get("status", {}) == "completed":
            if wait_count > 0:
                print("")
            break
        else:
            if wait_count == 0:
                print("Waiting Analysis Results", end="")
            else:
                print(".", end="")
        sys.stdout.flush()
        time.sleep(1)
        wait_count += 1

    print("URL Analysis Completed")
    results = get_url_result(response_analysis_data, mode, keylist)

    if output_name:
        file_path = write_analysis(results, output_name)
        print(f"Result saved in {file_path}")
        return

    return results
