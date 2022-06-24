from bson.json_util import dumps
from bson.json_util import loads
import json
#Script to get all logs from database
def prep_logs(db):
    header = '@-logs'
    cr = '\n'
    # Set filehandle
    f = open("/da5id_data.txt", "a")
    f.write(header)
    f.write(cr)
    # Get actions
    get_logs = db.logs.find({},{"log_info":1,"_id":0})
    json_logs = loads(dumps(get_logs))
    for item in json_logs:
        item = str(item)
        item = item.replace("\'", "\"")
        f.write(item)
        f.write(cr)
    f.close()
    return json_logs
