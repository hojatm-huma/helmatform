terraform {
  required_version = "~> 1.5"
  required_providers {
    flux = {
      source  = "fluxcd/flux"
      version = "~> 1.8.0"
    }
  }
}

provider "flux" {
  kubernetes = {
    config_path = "helmatform-k8s-config"
  }
  git = {
    url = "https://github.com/hojatm-huma/helmatform.git"
    http = {
      username = "git" # This can be any string when using a personal access token
      password = var.github_token
    }
  }
}
