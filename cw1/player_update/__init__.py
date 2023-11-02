import logging
import os
import shared.dbHelper as dbHelper
import json

from azure.functions import HttpRequest, HttpResponse
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError

ThisCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
PlayerDB = ThisCosmos.get_database_client(os.environ['DatabaseName'])
PlayerContainer = PlayerDB.get_container_client(os.environ['PlayerContainerName'])

def main(req: HttpRequest) -> HttpResponse:
    req_body = req.get_json()
    logging.info('New player update request %s', req_body)
    name = req_body.get('username')
    add_game_played = req_body.get('add_to_games_played')
    add_score = req_body.get('add_to_score')

    if (dbHelper.player_exist(PlayerContainer, name) == False):
        body = json.dumps({"result": False, "msg": "Username does not exist" })
        return HttpResponse(body=body, mimetype="application/json")
    
    player = dbHelper.get_player(PlayerContainer, name)
    player.games_played += add_game_played
    player.score += add_score
    dbHelper.update_player(PlayerContainer, player)
    body = json.dumps({"result": True , "msg" : "OK"})
    return HttpResponse(body=body, mimetype="application/json")