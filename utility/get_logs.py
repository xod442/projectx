from bson.json_util import dumps
from bson.json_util import loads
#Script to get all logs from database
def get_logs(db):
    logs = []
    get_logs = db.logs.find({})
    json_logs = loads(dumps(get_logs))
    for log in json_logs:
        logs.append(log)
    return logs
