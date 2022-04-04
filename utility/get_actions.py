from bson.json_util import dumps
from bson.json_util import loads
#Script to get all logs from database
def get_actions(db):
    actions = []
    get_actions = db.actions.find({"status":"open"})
    json_actions = loads(dumps(get_actions))
    for action in json_actions:
        actions.append(action)
    return actions
