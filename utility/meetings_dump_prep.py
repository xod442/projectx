from bson.json_util import dumps
from bson.json_util import loads
import json
from pathlib import Path

data_folder = Path()

file_to_open = data_folder / "da5id_data.txt"
#Script to get all logs from database
def prep_meeting(db):
    header = '@-meetings'
    cr = '\n'
    # Set filehandle
    f = open(file_to_open, "a")
    f.write(header)
    f.write(cr)
    # Get deals
    get_meetings = db.meetings.find({},{"_id":0,"company":1,"title":1,"notes":1})
    json_meetings = loads(dumps(get_meetings))
    for item in json_meetings:
        item = str(item)
        item = item.replace("\'", "\"")
        f.write(item)
        f.write(cr)
    f.close()
    return json_meetings
