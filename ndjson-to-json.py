#!/usr/bin/python3

import json

input_filepath="messages.ndjson"
output_filepath="messages.json"

with open(output_filepath, 'w') as f_out:
    with open(input_filepath, 'r') as f_in:
        ndjson_content = f_in.read()
        for ndjson_line in ndjson_content.splitlines():
            if not ndjson_line.strip():
                continue  # ignore empty lines
            json_line = json.loads(ndjson_line)
            json.dump(json_line, f_out)
