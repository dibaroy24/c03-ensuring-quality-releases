resource "azurerm_virtual_network" "eqrvnet" {
  name                 = "${var.application_type}-${var.resource_type}"
  address_space        = var.address_space
  location             = var.location
  resource_group_name  = var.resource_group
}
resource "azurerm_subnet" "eqrsubnet" {
  name                 = "${var.application_type}-SUB${var.resource_type}"
  resource_group_name  = var.resource_group
  virtual_network_name = azurerm_virtual_network.test.name
  address_prefixes     = [ var.address_prefix_test ]
}
