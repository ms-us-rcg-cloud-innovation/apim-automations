import azure.functions as func
import logging
from azure.identity import DefaultAzureCredential
import requests
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="apimSubscriptionRequest")
def apimSubscriptionRequest(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get the system-assigned managed identity token
    credential = DefaultAzureCredential()
    token = credential.get_token('https://management.azure.com')
    headers = {'Authorization': 'Bearer ' + token.token}

    # Make the GET request
    url = 'https://management.azure.com/subscriptions/SUBIDHERE/resourceGroups/APIMRESOURCEGROUPHERE/providers/Microsoft.ApiManagement/service/APIMNAMEHERE/apis?api-version=2022-08-01'
    response = requests.get(url, headers=headers)

    # Parse the response JSON
    data = response.json()

    # Extract only the fields we're interested in and make the additional API call for each ID
    filtered_data = []
    for item in data['value']:
        api_info = {
            'id': item['id'],
            'name': item['name'],
            'serviceUrl': item['properties']['serviceUrl'],
            'path': item['properties']['path']
        }

        # Make the additional API call
        api_id = item['id'].split('/')[-1]
        url = f'https://management.azure.com/subscriptions/SUBIDHERE/resourceGroups/APIMRESOURCEGROUPHERE/providers/Microsoft.ApiManagement/service/APIMNAMEHERE/apis/{api_id}/operations?api-version=2022-08-01'
        response = requests.get(url, headers=headers)

        # Add the response from the additional API call to the API info
        api_info['operations'] = response.json()

        filtered_data.append(api_info)

    # Return the filtered data as the HTTP response
    return func.HttpResponse(json.dumps(filtered_data), status_code=response.status_code)



@app.route(route="apimEvents", auth_level=func.AuthLevel.ANONYMOUS)
def apimEvents(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    return func.HttpResponse(status_code=200)


@app.route(route="triggerTest2", auth_level=func.AuthLevel.ANONYMOUS)
def triggerTest2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
        


@app.event_grid_trigger(arg_name="azeventgrid")
def eventTrigger(azeventgrid: func.EventGridEvent):
    logging.info('Python EventGrid trigger processed an event')
    
