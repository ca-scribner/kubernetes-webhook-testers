import copy
from pprint import pprint

from pathlib import Path
import json
import jsonpatch
import requests
import yaml
import base64
import typer


admission_review_template = {
    "kind": "AdmissionReview",
    "apiVersion": "admission.k8s.io/v1beta1",
    "request": {
        "kind":
            {
                "group": "",
                "version": "v1",
                "kind": "Pod"
            },
        "resource":
            {
                "group": "",
                "version": "v1",
                "resource": "pods"
            },
        "namespace": "kubeflow",
        "operation": "CREATE",
        "object": {},
    },
}


def main(input_filename: str, output_filename: str, webhook_url: str = "https://localhost:8443/mutate"):

    # Load initial pod spec
    payload = yaml.safe_load(Path(input_filename).read_text())
    # payload = yaml.safe_load(Path("./example_pod_simple.yaml").read_text())
    print(f"loaded payload from {input_filename} of: {payload}")

    # Dump a JSON version of initial pod spec
    with open(f"{input_filename}.json", 'w') as f:
        json.dump(payload, f)

    # Build the admission review request
    admission_review = copy.deepcopy(admission_review_template)
    admission_review["request"]["object"] = payload

    response = requests.post(webhook_url, json=admission_review, verify=False)
    print(f"response = {response}")

    response_json = response.json()
    encoded_patch = response_json['response']['patch'].encode('ascii')
    patch_str = base64.b64decode(encoded_patch).decode('ascii')
    patch_json = json.loads(patch_str)
    print(f"patch_str (as dict) = ")
    pprint(patch_json)

    # patch_json[1]["path"] += "/-"
    # patch_json[0]["path"] += "/-"

    patch = jsonpatch.JsonPatch.from_string(json.dumps(patch_json))
    print(f"patch = {patch}")

    result = patch.apply(payload)
    with open(output_filename, 'w') as f:
        yaml.dump(result, f)


if __name__ == "__main__":
    typer.run(main)
