from datetime import datetime, timezone


def AV_handler(results, mode=None, keylist=None):
    output_av = []
    avlist = {}
    for av_name, av_attributes in results.items():
        # Replace spaces with underscores in the AV name
        new_av_name = av_name.replace(" ", "_")
        avlist[new_av_name] = av_attributes

    if "category" in mode or "all" in mode:
        output_av.append(1)
    else:
        for av_name, av_attributes in avlist.items():
            if "antivirus" in mode:
                if av_name in keylist:
                    output_av.append(av_name)
            elif "avmethod" in mode:
                if av_attributes.get("method") in keylist:
                    output_av.append(av_name)
            elif "avcategory" in mode:
                if av_attributes.get("category") in keylist:
                    output_av.append(av_name)
            elif "avengine" in mode:
                if av_attributes.get("engine_name") in keylist:
                    output_av.append(av_name)
            elif "avresult" in mode:
                if av_attributes.get("result") in keylist:
                    output_av.append(av_name)

    av_results = []
    if output_av:
        total_av = 0
        for av_name, av_attributes in avlist.items():
            if av_name in output_av or output_av[0] == 1:
                result = av_attributes.get("result", "Unknown Result")
                method = av_attributes.get("method", "Unknown Method")
                category = av_attributes.get("category", "Unknown Category")
                engine_name = av_attributes.get("engine_name", "Unknown Engine Name")
                if "file" in mode:
                    engine_version = av_attributes.get("engine_version")
                    engine_update = av_attributes.get("engine_update")
                    engine_name = f"{engine_name} {engine_version}v {engine_update}"
                av_results.append(av_name)
                av_results.append(f"Result: {result}, Method: {method}")
                av_results.append(f"Category: {category}, Engine Name: {engine_name}\n")
                total_av += 1
        av_results.append(f"** Total: {total_av}")

    else:
        return "No result found"

    return "\n".join(av_results)

    # Iterate through each AV in the results
    # for av_name, av_attributes in avlist.items():
    #     # Check if the result is 'clean'
    #     if av_attributes.get("result") == "clean":
    #         # Print the AV name and its attributes
    #         print(f"AV Name: {av_name}")
    #         for attr, value in av_attributes.items():
    #             print(f"  {attr}: {value}")
    #         print()  # Print a newline for better readability


def convert_json_to_text(json_data, mode, keylist=None):
    # Extract necessary information from the JSON

    data = json_data.get("data", {})
    attributes = data.get("attributes", {})
    meta = json_data.get("meta", {})
    date_unix = attributes.get("date")
    # date = datetime.utcfromtimestamp(date_unix).strftime('%Y-%m-%d %H:%M:%S') if date_unix else "Unknown Date"

    date = (
        datetime.fromtimestamp(date_unix, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        if date_unix
        else "Unknown Date"
    )

    analysis_id = data.get("id", "Unknown ID")
    stats = attributes.get("stats", {})
    results = attributes.get("results", {})

    file_meta = ["File Info: "]
    url = None
    if "file" in mode:
        file_info = meta.get("file_info", {})
        for file_attr, file_val in file_info.items():
            file_meta.append(f"{file_attr} : {file_val}")
        file_meta.append("")
    else:
        url_info = meta.get("url_info", {})
        url = url_info.get("url", {})

    # Format the output
    output = []

    if "file" in mode:
        output.append(f"Analysis File \n")
        output.append(f"Info :")
        output.append(f"ID Analysis: {analysis_id}")
        output.append(f"Date Analysis: {date}\n")
        output.extend(file_meta)
    else:
        output.append(f"Analysis URL [{url}]\n")
        output.append(f"Info :")
        output.append(f"ID Analysis: {analysis_id}")
        output.append(f"Date Analysis: {date}\n")

    # Statistics
    if ("category" in mode and "S" in keylist) or "all" in mode:
        total_av = 0
        stats_type = []

        for key, value in stats.items():
            stats_type.append(f"{key.capitalize()}: {value}")
            total_av += int(value)
        output.append(f"Result Statistics [Total AV: {total_av}]")
        output.append(", ".join(stats_type))

    if "av" in mode or "all" in mode:
        output.append("\nAV Results:")
        result_av = AV_handler(results, mode, keylist)
        output.append(result_av)

    # Join all parts and return the final string
    return "\n".join(output)


def get_url_result(data, mode, keylist=None):
    text_output = convert_json_to_text(data, mode, keylist)
    return text_output
