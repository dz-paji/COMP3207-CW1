import logging
from shared_code.Player import Player

class PlayerNotFoundException(Exception):
    pass

def query(container, query):
    result = list(
        container.query_items(
            query=query,
            enable_cross_partition_query=True
        )
    )
    return result

def get_player(container, username):
    ''' Get player by their user name
    '''
    params = f"SELECT * FROM players WHERE players.username = '{username}'"
    result = query(container, params)
    player = Player("a","b")
    if len(result) == 0:
        raise PlayerNotFoundException
    else:
        player.from_dict(result[0])
        return player
    
def player_exist(container, username):
    ''' return true if player exists
    '''
    try:
        get_player(container, username)
    except PlayerNotFoundException:
        return False
    
    return True

def update_player(container, player):
    ''' update player
    '''
    logging.info(f"Updating player {player.to_dict()}")
    resp = container.upsert_item(player.to_dict())
    resp_player = Player("a","b")
    return resp_player.from_dict(resp)