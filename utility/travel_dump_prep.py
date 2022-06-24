from bson.json_util import dumps
from bson.json_util import loads
import json
#Script to get all logs from database
def prep_travel(db):
    header = '@-travel'
    cr = '\n'
    # Set filehandle
    f = open("/da5id_data.txt", "a")
    f.write(header)
    f.write(cr)
    # Get deals
    get_travel = db.travel.find({},{"_id":0,
                                    "travel-desc":1,
                                    "date-out":1,
                                    "takeoff-out":1,
                                    "land-out":1,
                                    "flight-out":1,
                                    "date-back":1,
                                    "takeoff-back":1,
                                    "land-back":1,
                                    "flight-back":1,
                                    "notes":1})
    json_travel = loads(dumps(get_travel))
    for item in json_travel:
        item = str(item)
        item = item.replace("\'", "\"")
        f.write(item)
        f.write(cr)
    f.close()
    return json_travel
