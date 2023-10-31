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
    logging.info('New login request. %s', req.get_json())
    req_body = req.get_json()
    name = req_body.get('username')
    passwd = req_body.get('password')

    try:
        player = dbHelper.get_player(PlayerContainer, name)

        if player == None:
            return HttpResponse(body=json.dumps({"result" : False, "msg": "Username or password incorrect" }), mimetype="application/json")

        if player['password'] == passwd:
            return HttpResponse(body=json.dumps({"result" : True, "msg": "OK" }), mimetype="application/json")
        else:
            return HttpResponse(body=json.dumps({"result" : False, "msg": "Username or password incorrect" }), mimetype="application/json")
    except CosmosHttpResponseError as err:
        return HttpResponse(body=json.dumps({"result" : False, "msg": "Username or password incorrect" }), mimetype="application/json")