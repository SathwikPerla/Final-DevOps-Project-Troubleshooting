# Kubernetes Troubleshooting Lab (OpsPulse)

This module provides two real-world failure scenarios to practice diagnosing and resolving production Kubernetes incidents.

---

## Lab 1: ImagePullBackOff / Broken Image

### 1. Trigger the Failure
```bash
kubectl apply -f troubleshooting/broken-image.yaml
```

### 2. Observe the Status
```bash
kubectl get pods -n opspulse -l app=opspulse-broken-image
```
*Observed State:* `ImagePullBackOff` or `ErrImagePull`.

### 3. Diagnose the Root Cause
```bash
kubectl describe pod -n opspulse -l app=opspulse-broken-image
kubectl get events -n opspulse --sort-by=.lastTimestamp
```
*Diagnostic Finding:* The Kubelet fails pulling `devopscapstoneproject-backend:v999-broken-tag-does-not-exist` because the image tag does not exist in the container registry.

### 4. Resolution
Update the image to a verified, published image tag or SHA digest:
```bash
kubectl set image deployment/opspulse-broken-image app=devopscapstoneproject-backend:latest -n opspulse
```
Then clean up:
```bash
kubectl delete -f troubleshooting/broken-image.yaml
```

---

## Lab 2: Service Selector Mismatch / Empty Endpoints

### 1. Trigger the Failure
```bash
kubectl apply -f troubleshooting/broken-service.yaml
```

### 2. Check Service and Endpoints
```bash
kubectl get svc opspulse-broken-service -n opspulse
kubectl get endpoints opspulse-broken-service -n opspulse
```
*Observed State:* `ENDPOINTS: <none>`. No traffic can reach any pod.

### 3. Diagnose Selector
```bash
kubectl get svc opspulse-broken-service -n opspulse -o yaml | grep -A 2 selector
kubectl get pods -n opspulse --show-labels
```
*Diagnostic Finding:* The Service selector is searching for `app: wrong-nonexistent-selector-label`, while the backend pods carry the label `app: opspulse-backend`.

### 4. Resolution
Edit the Service to match the correct pod label `app: opspulse-backend`.
```bash
kubectl delete -f troubleshooting/broken-service.yaml
```
