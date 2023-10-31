import logging
import os
from shared.Player import Player
import shared.dbHelper as dbHelper
import json

from azure.functions import HttpRequest, HttpResponse
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError

ThisCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
PlayerDB = ThisCosmos.get_database_client(os.environ['DatabaseName'])
PlayerContainer = PlayerDB.get_container_client(os.environ['PlayerContainerName'])


def main(req: HttpRequest) -> HttpResponse:
    logging.info('New register request. %s', req.get_json())
    req_body = req.get_json()
    name = req_body.get('username')
    passwd = req_body.get('password')
    player = Player(name = name, passwd = passwd)
    flag = player.validation()

    match flag:
        case 0:
            try:
                player = dbHelper.get_player(PlayerContainer, name)
                if player != None:
                    return HttpResponse(body=json.dumps({"result": False, "msg": "Username already exists" }))
                logging.info('Creating new player %s', player.to_dict())
                PlayerContainer.create_item(player.to_dict(), enable_automatic_id_generation=True)
                return HttpResponse(body=json.dumps({"result" : True, "msg": "OK" }), mimetype="application/json")
            except CosmosHttpResponseError as err:
                body=json.dumps({"result": False, "msg": "Username already exists" })
        case 1:
            body = json.dumps({"result": False, "msg": "Username less than 4 characters or more than 14 characters"  } )
            return HttpResponse(body=body, mimetype="application/json")
        case 2:
            body = json.dumps({"result": False, "msg": "Password less than 10 characters or more than 20 characters"  } )
            return HttpResponse(body=body, mimetype="application/json")