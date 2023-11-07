import logging
import os
import json

from shared_code.Prompt import Prompt

from azure.functions import HttpRequest, HttpResponse
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError

ThisCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
PlayerDB = ThisCosmos.get_database_client(os.environ['Database'])
PlayerContainer = PlayerDB.get_container_client(os.environ['PlayerContainer'])
PromotContainer = PlayerDB.get_container_client(os.environ['PromptContainer'])
def main(req: HttpRequest) -> HttpResponse:
    logging.info('New prompt delete request')
    req_body = req.get_json()
    
    if "player" in req_body:
        name = req_body.get("player")
        i = 0;
        for prompt in PromotContainer.query_items(
            query=f"SELECT * FROM prompts WHERE prompts.username = '{name}'",
            enable_cross_partition_query=True
        ):
            print(prompt.get("id"))
            PromotContainer.delete_item(prompt.get("id"), partition_key=prompt.get("username"))
            i = i + 1
            
        msg = (f"{i} prompts deleted")
        body = ({"result": True, "msg": msg})
    elif "word" in req_body:
        word = req_body.get("word")
        i = 0;
        
        for prompt in PromotContainer.query_items(
            query=f"SELECT * FROM prompts",
            enable_cross_partition_query=True
        ):
            prompt_obj = Prompt("1", "1", "1")
            prompt_obj.from_dict(prompt)
            for x in prompt_obj.get_en():
                print(x)
                if x.lower() == word.lower():
                    PromotContainer.delete_item(prompt_obj.id, partition_key=prompt_obj.name)
                    i = i + 1
                    break

        
        msg = (f"{i} prompts deleted")
        body = ({"result": True, "msg": msg})
    else:
        return HttpResponse(
             "Unexpected content",
             status_code=401
        )
    
    return HttpResponse(body=json.dumps(body), status_code=200)
