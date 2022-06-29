from bson.json_util import dumps
from bson.json_util import loads
import json
from pathlib import Path

data_folder = Path()

file_to_open = data_folder / "da5id_data.txt"
#Script to get all logs from database
def prep_deals(db):
    header = '@-deals'
    cr = '\n'
    # Set filehandle
    f = open(file_to_open, "a")
    f.write(header)
    f.write(cr)
    # Get deals
    get_deals = db.deals.find({},{"_id":0,"deal":1,"company":1,"status":1,"thoughts":1,"partner":1,"notes":1,"customer":1,"ope":1,"price":1})
    json_deals = loads(dumps(get_deals))
    for item in json_deals:
        item = str(item)
        item = item.replace("\'", "\"")
        f.write(item)
        f.write(cr)
    f.close()
    return json_deals
