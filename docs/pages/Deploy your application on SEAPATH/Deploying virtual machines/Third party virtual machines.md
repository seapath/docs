[Deploy your application on SEAPATH](../../Deploy%20your%20application%20on%20SEAPATH.md) > [Deploying virtual machines](../Deploying%20virtual%20machines.md)

# Third party virtual machines

This page lists third-party virtual machine (VM) integrations with deployment information for SEAPATH. A listing documents an integration, it does not mean that SEAPATH has certified the product, tested it with every SEAPATH release, or guarantees its ongoing compatibility.

## Deploying a listed VM

Follow the integration page and linked vendor documentation for product-specific requirements and deployment instructions.

For general information about VM deployment on SEAPATH, see [Virtual machines deployment](Virtual%20machines%20deployment.md).

## Contributing an integration

Vendors may contribute integration material to the [SEAPATH Ansible repository](https://github.com/seapath/ansible), such as an Ansible inventory and any required VM configuration.

Use SEAPATH’s existing `guest.xml.j2` template when it meets the VM’s requirements. If it does not, the integration may provide a vendor-specific template or configuration.

The vendor is responsible for creating, maintaining, and testing its integration. The vendor should identify which SEAPATH release or releases it has tested the integration with and update that information as it tests newer releases. SEAPATH does not test every third-party integration with every release. Integrations that are no longer maintained or known to work may be marked as outdated or unmaintained, or archived.

Vendors are responsible for their detailed product documentation. An integration page may include a concise overview and links to vendor documentation; it should not duplicate the vendor’s full documentation.

## Listed integrations

- [ABB - SSC600 SW](Third%20party%20virtual%20machines/ABB%20-%20SSC600%20SW.md)
