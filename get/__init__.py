import logging
import os
import json
import shared.dbHelper as dbHelper

from shared.Prompt import Prompt
from shared.Player import Player
from azure.functions import HttpRequest, HttpResponse
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError

ThisCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
PlayerDB = ThisCosmos.get_database_client(os.environ['DatabaseName'])
PlayerContainer = PlayerDB.get_container_client(os.environ['PlayerContainerName'])
PromotContainer = PlayerDB.get_container_client(os.environ['PromptContainerName'])

def main(req: HttpRequest) -> HttpResponse:
    logging.info('New util get request')

    req_body = req.get_json()
    names = req_body.get('players')
    lang  = req_body.get('language')
    name = req.params.get('name')
    
    output = []
    for name in names:
        if dbHelper.player_exist(PlayerContainer, name):
            for prompt in PromotContainer.query_items(
            query=f"SELECT * FROM prompts WHERE prompts.username = '{name}'",
            enable_cross_partition_query=True):
                this_prompt = Prompt("1", "1", "1")
                this_prompt.from_dict(prompt)
                this_string = {"id": this_prompt.id, "text": this_prompt.get_text_by_lang(lang), "username": this_prompt.name}
                output.append(this_string)
                

            
            
    return HttpResponse(body=json.dumps(output), status_code=200)