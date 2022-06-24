from bson.json_util import dumps
from bson.json_util import loads
import json
#Script to get all logs from database
def prep_customer(db):
    header = '@-customer'
    cr = '\n'
    # Set filehandle
    f = open("/da5id_data.txt", "a")
    f.write(header)
    f.write(cr)
    # Get actions
    get_customer = db.customer.find({},{"_id":0, "company":1, "name":1, "phone":1, "email":1})
    json_customer = loads(dumps(get_customer))
    for item in json_customer:
        item = str(item)
        item = item.replace("\'", "\"")
        f.write(item)
        f.write(cr)
    f.close()
    return json_customer
