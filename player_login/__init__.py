import logging
import os
from shared_code.Player import Player
import shared_code.dbHelper as dbHelper
import json

from azure.functions import HttpRequest, HttpResponse
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError

ThisCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
PlayerDB = ThisCosmos.get_database_client(os.environ['Database'])
PlayerContainer = PlayerDB.get_container_client(os.environ['PlayerContainer'])

def main(req: HttpRequest) -> HttpResponse:
    logging.info('New login request. %s', req.get_json())
    req_body = req.get_json()
    name = req_body.get('username')
    passwd = req_body.get('password')

    try:
        player = dbHelper.get_player(PlayerContainer, name)
        if player.passwd == passwd:
            body=json.dumps({"result" : True, "msg": "OK" })
        else:
            body=json.dumps({"result" : False, "msg": "Username or password incorrect" })
    
    except CosmosHttpResponseError as err:
        body=json.dumps({"result" : False, "msg": "Username or password incorrect" })
    except dbHelper.PlayerNotFoundException as err:
        body=json.dumps({"result" : False, "msg": "Username or password incorrect" })
        
    return HttpResponse(body = body, mimetype="application/json")