# Azure AI Foundry: Web App for Realtime Speech Transalation

This repo demonstrates how to use the **gpt-realtime-translate** model in Microsoft Foundry with server-side *WebSocket* Python proxy and secure *Entra ID* authentication.

## 📑 Table of Contents:
- [Part 1: Configuring Solution Environment](#part-1-configuring-solution-environment)
- [Part 2: Backend Implementation]()
- [Part 3: Frontend UI]()
- [Part 4: Running the Demo]()

## Part 1: Configuring Solution Environment

### 1.1 Foundry Setup
Ensure you have a **gpt-realtime-translate** model deployed in your Microsoft Foundry resource. Take a note of your Foundry's resource name and your model's deployment name.

### 1.2 Authentication & Role Assignment
The demo utilises passwordless *Microsoft Entra ID* authentication via the `DefaultAzureCredential` provider.

Ensure the identity executing this code (your local *Azure CLI* login, *Service Principal* or *Managed Identity*) has been granted at least the Foundry User on your Azure AI resource, as described [here](https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry?tabs=owner%2Cfoundry#minimum-role-assignments-to-get-started).

Before running the server locally, log in to your environment using:

``` PowerShell
az login
```

1.3 Environment VariablesConfigure the following environment variables in your terminal:Environment VariableDescriptionFOUNDRY_RESOURCE_NAMEThe sub-domain name of your Azure OpenAI/Foundry resource.FOUNDRY_DEPLOYMENT_NAMEThe exact name of your gpt-realtime-translate deployment.1.4 InstallationInstall the necessary asynchronous web server and Azure identity libraries:Code snippetpip install fastapi uvicorn websockets azure-identity
