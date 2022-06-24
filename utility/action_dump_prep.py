from bson.json_util import dumps
from bson.json_util import loads
import json
#Script to get all logs from database
def prep_actions(db):
    header = '@-actions'
    cr = '\n'
    f = open("/da5id_data.txt", "w")
    f.write(header)
    f.write(cr)
    # Get actions
    get_actions = db.actions.find({},{"action":1, "company":1, "status":1 ,"_id":0})
    #Conver mongo curson to json
    json_actions = loads(dumps(get_actions))
    for item in json_actions:
        item = str(item)
        item = item.replace("\'", "\"")
        f.write(item)
        f.write(cr)
    f.close()
    return json_actions
