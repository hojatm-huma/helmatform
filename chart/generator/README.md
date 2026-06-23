repo: https://github.com/flux-iac/tofu-controller
reads the base helm chart and generate the final helm chart

tf-modules/s3:
```
values:
    S3:
        ...

templates:
---
apiVersion: infra.contrib.fluxcd.io/v1alpha2
kind: Terraform
metadata:
  name: s3
spec:
  path: ./modules/s3
  sourceRef:
    kind: GitRepository
    name: telm
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: s3
spec:
  target:
    name: {{ .values.common_secret_name }}
  data:
    - {{ from_created_external_secret }}
```

