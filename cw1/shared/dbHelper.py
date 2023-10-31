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
    params = f"SELECT * FROM players WHERE players.username = '{username}'"
    result = query(container, params)
    if len(result) == 0:
        raise PlayerNotFoundException
    else:
        return result[0]
    
def player_exist(container, username):
    try:
        player = get_player(container, username)
    except PlayerNotFoundException:
        return False
    
    return True