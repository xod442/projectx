from bson.json_util import dumps
from bson.json_util import loads
import json
from pathlib import Path

data_folder = Path()

file_to_open = data_folder / "da5id_data.txt"
#Script to get all logs from database
def prep_logs(db):
    header = '@-logs'
    cr = '\n'
    # Set filehandle
    f = open(file_to_open, "a")
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
