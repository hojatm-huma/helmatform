## Helmatform: your platform defined using Helm

I was thinking about how we could put all the dependencies of a project in a single YAML file. This way, anyone looking at the file can understand how the project works, end to end.

There are already many interesting tools that let you define a project's dependencies using a YAML file, like Render or Heroku. But they are too general, so companies still end up building their own platform on top. How can we have a base for a custom platform instead?

We're already doing some kind of customization with Helm, right? So let's take it further and use Helm to build the whole infrastructure.

## Be more specific? Why Helmatform?

- **Every dependency of the project is defined in a single YAML file:** From cloud resources to monitoring dashboards, everything is defined in one YAML file, customized for the company.
- **Low learning curve for platform developers:** New joiners only need to learn Helm, Flux, and Terraform. No new system, no new programming language.
- **Low learning curve for users:** Users of the platform only need to learn the YAML interface, customized for the company's resources.
- **Already provisioned resources are importable:** Just create the Terraform module and import the state file into the Tofu state, and your existing resources become manageable by Helmatform.
- **Import provisioned resources into your local machine:** Easily import provisioned resources into your local Terraform code and start debugging right away.
- **It's almost headless:** Helmatform doesn't run any bespoke service. It relies on open source software that is well maintained and proven in production.
- **Clear separation between customization and standards:** The infra team writes Terraform modules that handle company standards and set defaults in the base values file for services to build on.

## How to run the project?

1. Set up Kubernetes

```bash
cd app-k8s/k8s-tf
terraform init
terraform apply
```

2. Set up Flux for Kubernetes

```bash
cd app-k8s/fluxcd-tf
terraform init
terraform apply
```

3. Create the `aws-creds` secret in the applications namespace

```bash
cd app-k8s/aws-secrets-tf
terraform init
terraform apply
```

That's it! You should now have the S3 bucket created and `sample-app` deployed. Check its logs to see a successful connection.

## Next Steps

- [ ] Use the pod identity agent instead of long-lived AWS tokens