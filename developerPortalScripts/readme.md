# Developer Portal Customizations CICD

## Overview
This project includes scripts and workflows for extracting and publishing Azure API Management Developer Portal content.

## GitHub Workflows

### Extract Workflow
The [extract workflow](../.github/workflows/extract.yml) is triggered manually from the GitHub Actions UI. It extracts the Azure API Management Developer Portal content and commits the changes to a new branch. The workflow uses the `extractDeveloperPortal.ps1` PowerShell script.

### Publish Workflow
The [publish workflow](../.github/workflows/publish.yml) is triggered on a push to the `main` branch. It copies the extracted content to a publish directory and then publishes the content using the `publishDeveloperPortal.ps1` PowerShell script.

## PowerShell Scripts

### extractDeveloperPortal.ps1
This script is used to extract the Azure API Management Developer Portal content. It takes several parameters including the resource group name, API Management name, and export folder. The extracted content is saved to the specified export folder. You can find this script in the [developerPortalScripts](../developerPortalScripts/) directory.

### publishDeveloperPortal.ps1
This script is used to publish the Azure API Management Developer Portal content. It takes several parameters including the resource group name, API Management name, and import folder. The content to be published should be in the specified import folder. You can find this script in the [developerPortalScripts](../developerPortalScripts/) directory.

## Getting Started
To get started with this project, you'll need to have PowerShell installed. You can then run the PowerShell scripts from your local machine. For the GitHub workflows, you'll need to have a GitHub account and a repository where you can add these workflows.

## Contributing
Contributions are welcome! Please read our contributing guidelines before getting started.

## License
This project is licensed under the terms of the MIT license.