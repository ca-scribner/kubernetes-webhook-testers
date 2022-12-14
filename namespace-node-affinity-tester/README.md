## Summary

This was a tool written when debugging the [namespace node affinity](https://github.com/idgenchev/namespace-node-affinity) tool in [this fork](https://github.com/ca-scribner/namespace-node-affinity).  It lets you read in a kubernetes yaml file (such as the included `example_pod_simple.yaml`) and it will send that object as an AdmissionReview to a provided URL (which could either be a local instance of the webhook's pod, or a port-forwarded pod/service from a live kubernetes cluster).  

## Usage examples

Executed on a local instance of the tool, which is running on port 8443

```bash
python main.py example_pod_simple.yaml patched.yaml --webhook-url https://localhost:8443/mutate 
```

Or, if you have the webhook pod running in a cluster already: 
```bash
kubectl port-forward svc/namespace-node-affinity-pod-webhook 8443:443
python main.py example_pod_simple.yaml patched.yaml --webhook-url https://localhost:8443/mutate 
```
