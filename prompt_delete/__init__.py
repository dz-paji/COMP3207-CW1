import logging
import os
import json

from shared.Prompt import Prompt

import azure.functions as func
from azure.functions import HttpRequest, HttpResponse
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError

ThisCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
PlayerDB = ThisCosmos.get_database_client(os.environ['DatabaseName'])
PlayerContainer = PlayerDB.get_container_client(os.environ['PlayerContainerName'])
PromotContainer = PlayerDB.get_container_client(os.environ['PromptContainerName'])
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('New prompt delete request')
    req_body = req.get_json()
    
    if "player" in req_body:
        name = req_body.get("player")
        i = 0;
        for prompt in PromotContainer.query_items(
            query=f"SELECT * FROM prompts WHERE prompts.username = '{name}'",
            enable_cross_partition_query=True
        ):
            PromotContainer.delete_item(prompt, partition_key='username')
            i = i + 1
            
        body = ({"result": True, "msg": " %s prompts deleted"}, i)
        
    elif "word" in req_body:
        word = req_body.get("word")
        i = 0;
        
        for prompt in PromotContainer.query_items(
            query=f"SELECT * FROM prompts WHERE ARRAY_CONTAINS(prompts.texts, {{'text': '{word}'}}, true)",
            enable_cross_partition_query=True
        ):
            print(prompt)
        
    else:
        return func.HttpResponse(
             "Unexpected content",
             status_code=401
        )
    
    return func.HttpResponse(body=json.dumps(body), status_code=200)
