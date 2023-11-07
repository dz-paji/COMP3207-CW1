import logging
import os
import json

from azure.functions import HttpRequest, HttpResponse
from shared.Prompt import Prompt
from shared.Player import Player
from azure.functions import HttpRequest, HttpResponse
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceExistsError, CosmosResourceNotFoundError

ThisCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
PlayerDB = ThisCosmos.get_database_client(os.environ['DatabaseName'])
PlayerContainer = PlayerDB.get_container_client(os.environ['PlayerContainerName'])



def main(req: HttpRequest) -> HttpResponse:
    logging.info('New leaderboard request')
    req_body = req.get_json()
    k = req_body.get('top')
    output = []
    
    for player in PlayerContainer.query_items(
        query=f"SELECT * FROM player ORDER BY player.total_score DESC, player.games_played ASC, player.username ASC OFFSET 0 LIMIT {k}",
        enable_cross_partition_query=True):
        player_obj = Player("1", "1")
        player_obj.from_dict(player)
        
        this_line = {"username": player_obj.name, "games_played": player_obj.games_played, "total_score": player_obj.score}        
        output.append(this_line)
        
    return HttpResponse(body=json.dumps(output), status_code=200)
