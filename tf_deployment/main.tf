terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>2.0"
    }
  }
}

provider "azurerm" {
  features {}

  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
  subscription_id = var.subscription_id
}

resource "azurerm_resource_group" "projects-grp" {
  name     = "projects-grp"
  location = "West Europe"
}

resource "azurerm_mssql_server" "projects-sqlserver" {
  name                         = "projects-sqlserver"
  resource_group_name          = azurerm_resource_group.projects-grp.name
  location                     = azurerm_resource_group.projects-grp.location
  version                      = "12.0"
  administrator_login          = var.administrator_login
  administrator_login_password = var.administrator_login_password
  minimum_tls_version          = "1.0"
}

resource "azurerm_sql_database" "anilist-db" {
  name                = "anilist-db"
  server_name         = azurerm_mssql_server.projects-sqlserver.name
  resource_group_name = azurerm_resource_group.projects-grp.name
  location            = azurerm_resource_group.projects-grp.location
  edition             = "Free"
}
