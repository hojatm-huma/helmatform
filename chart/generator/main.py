import os
import hcl2
import yaml

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../..")
)
BASE_CHART_DIR = os.path.join(BASE_DIR, "base-chart")
TF_MODULE_DIR = os.path.join(BASE_DIR, "tf-modules")
NEW_CHART_DIR = os.path.join(BASE_DIR, "helmatform-chart")


def list_tf_modules() -> list[str]:
    """
    List all Terraform modules in the tf-modules directory.
    """
    return [
        name
        for name in os.listdir(TF_MODULE_DIR)
        if os.path.isdir(os.path.join(TF_MODULE_DIR, name))
    ]


def load_tf_module_variables(module_name: str) -> dict:
    """
    Load the variables from a Terraform module's variables.tf file.
    """

    module_path = os.path.join(TF_MODULE_DIR, module_name)
    variables_file = os.path.join(module_path, "variables.tf")

    if not os.path.exists(variables_file):
        raise FileNotFoundError(f"variables.tf not found for module {module_name}")

    variables = {}
    with open(variables_file, "r") as f:
        for var in hcl2.load(f)["variable"]:
            for key, value in var.items():
                key = key.strip('"')
                default_value = value.get("default", "").strip('"')
                variables[key] = default_value
        return variables


def load_base_chart_values() -> dict:
    """
    Load the values from the base-chart's values.yaml file.
    """
    values_file = os.path.join(BASE_CHART_DIR, "values.yaml")

    if not os.path.exists(values_file):
        raise FileNotFoundError("values.yaml not found in base-chart")

    with open(values_file, "r") as f:
        return yaml.safe_load(f)


def generate_input_configmap_name(module_name: str) -> str:
    """
    Generate a ConfigMap name for a given Terraform module.
    """
    return '{{printf "%s-%s" "' + module_name + '" $.Release.Name}}'


def generate_output_secret_name(module_name: str) -> str:
    """
    Generate a Secret name for a given Terraform module's outputs.
    """
    return '{{printf "%s-%s-outputs" "' + module_name + '" $.Release.Name}}'


def generate_configmap(module_name: str, variables: dict) -> dict:
    """
    Generate a ConfigMap Dictionary for a given Terraform module and its variables.
    """
    data = {}
    for key in variables.keys():
        data[key] = f"{{{{.{key}}}}}"

    configmap = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": generate_input_configmap_name(module_name),
        },
        "data": data,
    }
    return configmap


def generate_terraform(module_name: str) -> dict:
    """
    Generate a Terraform Dictionary for a given Terraform module and its variables.
    """
    terraform = {
        "apiVersion": "infra.contrib.fluxcd.io/v1alpha2",
        "kind": "Terraform",
        "metadata": {
            "name": '{{printf "%s-%s" "' + module_name + '" $.Release.Name}}',
        },
        "spec": {
            "interval": "5s",
            "approvePlan": "auto",
            "path": f"./tf-modules/{module_name}",
            "sourceRef": {
                "kind": "GitRepository",
                "name": "helmatform",
                "namespace": "flux-system",
            },
            "varsFrom": [
                {
                    "kind": "ConfigMap",
                    "name": generate_input_configmap_name(module_name),
                }
            ],
            "writeOutputsToSecret": {"name": generate_output_secret_name(module_name)},
            "runnerPodTemplate": {
                "spec": {"envFrom": [{"secretRef": {"name": "aws-creds"}}]}
            },
        },
    }
    return terraform


def bump_chart_version(chart_dir: str, new_version: str):
    # TODO how should we handle the version bumping?
    # How should we figure out the new version?
    pass


def copy_base_chart_to_new_chart():
    """
    Copy the base-chart directory to a new chart directory.
    """
    if os.path.exists(NEW_CHART_DIR):
        raise FileExistsError(
            f"{NEW_CHART_DIR} already exists. Please remove it before running this script."
        )
    os.system(f"cp -r {BASE_CHART_DIR} {NEW_CHART_DIR}")


def write_env_from_secret_to_deployment_yaml(module_name: str):
    """
    Write the envFrom secret to the deployment.yaml file in the new chart.
    """
    # TODO maybe use jinja2 to render the deployment.yaml file instead of doing string replacement
    deployment_yaml_path = os.path.join(NEW_CHART_DIR, "templates", "deployment.yaml")
    with open(deployment_yaml_path, "r") as f:
        deployment_yaml = f.read()

    ENV_FROM_SECRET = """
          {{{{with .Values.{module_name}}}}}
          envFrom:
            - secretRef:
                name: {{{{ printf "%s-%s-outputs" "{module_name}" $.Release.Name }}}}
          {{{{end}}}}
    """.format(module_name=module_name)
    deployment_yaml = deployment_yaml.replace(
        "<ENV_FROM_SECRET>",
        ENV_FROM_SECRET,
    )

    with open(deployment_yaml_path, "w") as f:
        f.write(deployment_yaml)


def rename_chart_name_in_chart_yaml(new_chart_dir: str, new_chart_name: str):
    """
    Rename the chart name in the Chart.yaml file of the new chart.
    """
    chart_yaml_path = os.path.join(new_chart_dir, "Chart.yaml")
    with open(chart_yaml_path, "r") as f:
        chart_yaml = yaml.safe_load(f)

    chart_yaml["name"] = new_chart_name

    with open(chart_yaml_path, "w") as f:
        yaml.dump(chart_yaml, f)


if __name__ == "__main__":
    tf_modules = list_tf_modules()
    base_chart_values = load_base_chart_values()

    copy_base_chart_to_new_chart()

    for module in list_tf_modules():
        base_chart_values[module] = {}
    with open(os.path.join(NEW_CHART_DIR, "values.yaml"), "w") as f:
        yaml.dump(base_chart_values, f)

    for module in tf_modules:
        write_env_from_secret_to_deployment_yaml(module)
        templates_dir = os.path.join(NEW_CHART_DIR, "templates")
        with open(os.path.join(templates_dir, f"terraform-{module}.yaml"), "w") as f:
            f.write("{{ with .Values." + module + " }}\n")
            terraform_template = []
            variables = load_tf_module_variables(module)
            configmap = generate_configmap(module, variables)
            terraform = generate_terraform(module)
            terraform_template.append(configmap)
            terraform_template.append(terraform)
            yaml.dump_all(terraform_template, f)
            f.write("{{ end }}\n")

    rename_chart_name_in_chart_yaml(NEW_CHART_DIR, "helmatform-chart")