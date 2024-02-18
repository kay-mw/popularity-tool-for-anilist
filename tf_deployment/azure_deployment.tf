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

resource "azurerm_resource_group" "project-grp" {
  name     = "kiran-projects-grp"
  location = "West Europe"
}

resource "azurerm_storage_account" "anilistproject" {
  name                     = "anilistproject"
  resource_group_name      = azurerm_resource_group.project-grp.name
  location                 = azurerm_resource_group.project-grp.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_mssql_server" "anilist-sqlserver" {
  name                         = "anilist-sqlserver"
  resource_group_name          = azurerm_resource_group.project-grp.name
  location                     = azurerm_resource_group.project-grp.location
  version                      = "12.0"
  administrator_login          = var.administrator_login
  administrator_login_password = var.administrator_login_password
}

resource "azurerm_mssql_database" "anilist-db" {
  name           = "anilist-db"
  server_id      = azurerm_mssql_server.anilist-sqlserver.id
  max_size_gb    = 4
}