import azure.functions as func
import logging
from azure.identity import DefaultAzureCredential, ClientSecretCredential
import requests
import json


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


# Define your credentials and set up the authorization header
def get_azure_credentials():

# if using a service principal, provide the client_id, tenant_id, and client_secret
    # client_id = ""
    # tenant_id = ""
    # client_secret = ""
    # credential = ClientSecretCredential(tenant_id, client_id, client_secret)
    
# if using managed identity, use the DefaultAzureCredential
    credential = DefaultAzureCredential()

    scope = "https://management.azure.com/.default"
    token = credential.get_token(scope)
    return {
        "Authorization": f"Bearer {token.token}",
        "Content-Type": "application/json",
    }


# Azure Function to handle HTTP requests
@app.route(route="apimApiDetails")
def apim_api_details(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    # Extract query parameters - Required parameters
    subscription_id = req.params.get("subscriptionId")
    resource_group_name = req.params.get("resourceGroupName")
    service_name = req.params.get("serviceName")
    api_name = req.params.get("apiName")  # Optional parameter to filter by API name

    # Validate required parameters
    if not all([subscription_id, resource_group_name, service_name]):
        missing_params = ", ".join(
            [
                param
                for param in ["subscriptionId", "resourceGroupName", "serviceName"]
                if not req.params.get(param.lower())
            ]
        )
        return func.HttpResponse(
            f"Missing required query parameters: {missing_params}. Please include them in the request.",
            status_code=400,
        )

    # Build the request URL
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.ApiManagement/service/{service_name}/apis?api-version=2022-08-01"

    # Get headers with Azure credentials
    headers = get_azure_credentials()

    # Make the API request to Azure
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return func.HttpResponse(
            f"Failed to fetch data from Azure API Management: {response.reason}",
            status_code=response.status_code,
        )

    # Process the response to filter the results
    apis = response.json().get("value", [])
    filtered_apis = [
        {
            "id": api["id"],
            "name": api["name"],
            "displayName": api["properties"]["displayName"],
            "serviceUrl": api["properties"]["serviceUrl"],
            "subscriptionKeyParameterNames": api["properties"][
                "subscriptionKeyParameterNames"
            ],
        }
        for api in apis
        if not api_name or api["name"] == api_name
    ]

    if not filtered_apis:
        return func.HttpResponse(
            "No API found matching the provided criteria.", status_code=404
        )

    # Return the filtered APIs as a JSON response
    return func.HttpResponse(
        json.dumps(filtered_apis, indent=2),
        headers={"Content-Type": "application/json"},
        status_code=200,
    )


# To test or deploy, ensure you set up the required environment variables or configurations.
