'''                               ,----,.
                             ,'   ,' |
    ,---,                  ,'   .'   |
  .'  .' `\              ,----.'    .'  ,--,         ,---,
,---.'     \             |    |   .'  ,--.'|       ,---.'|
|   |  .`\  |            :    :  |--, |  |,        |   | :
:   : |  '  |  ,--.--.   :    |  ;.' \`--'_        |   | |
|   ' '  ;  : /       \  |    |      |,' ,'|     ,--.__| |
'   | ;  .  |.--.  .-. | `----'.'\   ;'  | |    /   ,'   |
|   | :  |  ' \__\/: . .   __  \  .  ||  | :   .   '  /  |
'   : | /  ;  ," .--.; | /   /\/  /  :'  : |__ '   ; |:  |
|   | '` ,/  /  /  ,.  |/ ,,/  ',-   .|  | '.'||   | '/  '
;   :  .'   ;  :   .'   \ ''\       ; ;  :    ;|   :    :|
|   ,.'     |  ,     .-./\   \    .'  |  ,   /  \   \  /
'---'        `--`---'     `--`-,-'     ---`-'    `----'



2022 wookieware.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0.

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


__author__ = "@netwookie"
__credits__ = ["Rick Kauffman"]
__license__ = "Apache2"
__version__ = "0.1.1"
__maintainer__ = "Rick Kauffman"
__email__ = "rick@rickkauffman.com"
__status__ = "Alpha"

'''
#
import json
import uuid
import datetime

def process_line(db,dbname,line):
    line = json.loads(line)
    my_uuid = uuid.uuid4()
    my_uuid = str(my_uuid)
    if dbname == 'actions':
        count = db.actions.count_documents({})
        number = count + 1
        entry = {
            "action": line['action'],
            "company": line['company'],
            "number": number,
            "uuid": my_uuid,
            "status": line['status'],
            "when": datetime.datetime.now()
        }
        res = db.actions.insert_one(entry)
    if dbname == 'logs':
        count = db.logs.count_documents({})
        number = count + 1
        entry = {
            "log_info": line['log_info'],
            "number": number,
            "uuid": my_uuid,
            "when": datetime.datetime.now()
        }
        res = db.logs.insert_one(entry)
    if dbname == 'deals':
        count = db.deals.count_documents({})
        number = count + 1
        entry = {
            "deal": line['deal'],
            "company": line['company'],
            "customer": line['customer'],
            "ope": line['ope'],
            "price": line['price'],
            "status": line['status'],
            "thoughts": line['thoughts'],
            "partner": line['partner'],
            "notes": line['notes'],
            "number": number,
            "uuid": my_uuid,
            "when": datetime.datetime.now()
        }
        res = db.deals.insert_one(entry)
    if dbname == 'company':
        count = db.company.count_documents({})
        number = count + 1
        entry = {
            "name": line['name'],
            "uuid": my_uuid,
            "number": number,
            "when": datetime.datetime.now()
        }
        res = db.company.insert_one(entry)
    if dbname == 'customer':
        count = db.customer.count_documents({})
        number = count + 1

        entry = {
            "company": line['company'],
            "name": line['name'],
            "phone": line['phone'],
            "email": line['email'],
            "uuid": my_uuid,
            "number": number,
            "when": datetime.datetime.now()
        }
        res = db.customer.insert_one(entry)
    if dbname == 'meetings':
        count = db.meetings.count_documents({})
        number = count + 1
        entry = {
            "company": line['company'],
            "title": line['title'],
            "notes": line['notes'],
            "uuid": my_uuid,
            "number": number,
            "when": datetime.datetime.now()
        }
        res = db.meetings.insert_one(entry)
    if dbname == 'travel':
        count = db.travel.count_documents({})
        number = count + 1
        entry = {
            "travel-desc": line['travel-desc'],
            "date-out": line['date-out'],
            "takeoff-out": line['takeoff-out'],
            "land-out": line['land-out'],
            "flight-out": line['flight-out'],
            "date-back": line['date-back'],
            "takeoff-back": line['takeoff-back'],
            "land-back": line['land-back'],
            "flight-back": line['flight-back'],
            "notes": line['notes'],
            "uuid": my_uuid,
            "number": number,
            "when": datetime.datetime.now()
        }
        res = db.travel.insert_one(entry)

    return
