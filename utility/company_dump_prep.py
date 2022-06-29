from bson.json_util import dumps
from bson.json_util import loads
import json
from pathlib import Path

data_folder = Path()

file_to_open = data_folder / "da5id_data.txt"
#Script to get all logs from database
def prep_company(db):
    header = '@-company'
    cr = '\n'
    # Set filehandle
    f = open(file_to_open, "a")
    f.write(header)
    f.write(cr)
    # Get actions
    get_company = db.company.find({},{"_id":0, "name":1})
    json_company = loads(dumps(get_company))
    for item in json_company:
        item = str(item)
        item = item.replace("\'", "\"")
        f.write(item)
        f.write(cr)
    f.close()
    return json_company
