from flask import Flask, request, render_template, abort, redirect, url_for
import pymongo
import datetime
import os
from bson.json_util import dumps
from bson.json_util import loads
from utility.get_logs import get_logs
from utility.get_actions import get_actions
from utility.action_dump_prep import prep_actions
from utility.log_dump_prep import prep_logs
from utility.deal_dump_prep import prep_deals
from utility.company_dump_prep import prep_company
from utility.customer_dump_prep import prep_customer
from utility.meetings_dump_prep import prep_meeting
from utility.travel_dump_prep import prep_travel
from utility.line_writer import process_line
import uuid
#
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
APP_TEMPLATE = os.path.join(APP_ROOT, 'templates')

config = {
    "username": "admin",
    "password": "siesta3",
    "server": "mongo",
}

connector = "mongodb://{}:{}@{}".format(config["username"], config["password"], config["server"])
client = pymongo.MongoClient(connector)
db = client["demo"]
'''
#-------------------------------------------------------------------------------
Deal Section
#-------------------------------------------------------------------------------
'''
@app.route("/add_deal", methods=('GET', 'POST'))
def add_deal():
    if request.method == 'POST':
        # Get count
        count = db.deals.count_documents({})
        number = count + 1
        # Generate UUID
        my_uuid = uuid.uuid4()
        my_uuid = str(my_uuid)
        entry = {
            "deal": request.form['deal'].replace("'", ""),
            "company": request.form['company'].replace("'", ""),
            "status": request.form['status'].replace("'", ""),
            "thoughts": request.form['thoughts'].replace("'", ""),
            "partner": request.form['partner'].replace("'", ""),
            "notes": request.form['notes'].replace("'", ""),
            "number": number,
            "uuid": my_uuid,
            "when": datetime.datetime.now()
        }
        if entry["company"] == "unselected":
            # Get a list of Companies
            my_companies = []
            companies = db.company.find({})
            comp = loads(dumps(companies))
            for c in comp:
                name = c['name']
                my_companies.append(name)
            message = "please select a valid company to save action"
            return render_template('add_deal.html', message=message,
                                                    partner=entry['partner'],
                                                    deal=entry['deal'],
                                                    thoughts=entry['thoughts'],
                                                    notes=entry['notes'],
                                                    my_companies=my_companies)

        res = db.deals.insert_one(entry)
        message = 'Deal information written to database'
        return render_template('message.html', message=message)

    # Get a list of Companies
    my_companies = []
    companies = db.company.find({})
    comp = loads(dumps(companies))
    for c in comp:
        name = c['name']
        my_companies.append(name)
    return render_template('add_deal.html', my_companies=my_companies)

@app.route("/list_deals", methods=('GET', 'POST'))
def list_deals():
    # Get a list of Deals
    my_deals = []
    deal = db.deals.find({})
    deals = loads(dumps(deal))
    for d in deals:
        number = d['number']
        company = d['company']
        partner = d['partner']
        status = d['status']
        deal = d['deal']
        thoughts = d['thoughts']
        notes = d['notes']
        info = [number, company, partner, deal, status, thoughts, notes]
        my_deals.append(info)
    return render_template('list_deals.html', my_deals=my_deals)

@app.route("/edit_deal", methods=('GET', 'POST'))
def edit_deal():
    if request.method == 'POST':
        deal = request.form['deal']
        if deal == "unselected":
            message = "please select a valid deal"
            # Get a list of deals
            my_deals = []
            deals = db.deals.find({})
            deal = loads(dumps(deals))
            for d in deal:
                number = d['number']
                number = str(number)
                deal = d['deal']
                dash = '-'
                deal = number+dash+deal
                my_deals.append(deal)
            return render_template('edit_deal.html', my_deals=my_deals, message=message)

        temp = deal.split('-')
        number = temp[0]
        number = int(number)
        deals = db.deals.find({"number":number})
        deal = loads(dumps(deals))
        info = [ deal[0]['partner'], deal[0]['deal'], deal[0]['status'], deal[0]['thoughts'], deal[0]['notes'], deal[0]['number'], deal[0]['notes'], deal[0]['number'] ]
        return render_template('edit_deal_complete.html', info=info)


    # Get a list of deals
    my_deals = []
    deals = db.deals.find({})
    deal = loads(dumps(deals))
    for d in deal:
        number = d['number']
        number = str(number)
        deal = d['deal']
        dash = '-'
        deal = number+dash+deal
        my_deals.append(deal)
    return render_template('edit_deal.html', my_deals=my_deals)

@app.route("/edit_deal_complete", methods=('GET', 'POST'))
def edit_deal_complete():
    deal = request.form['deal'].replace("'", "")
    number = request.form['number'].replace("'", "")
    status = request.form['status'].replace("'", "")
    thoughts = request.form['thoughts'].replace("'", "")
    notes = request.form['notes'].replace("'", "")
    number = int(number)
    myquery = { "number": number }
    newvalues = { "$set": { "deal": deal, "status": status, "thoughts": thoughts, "notes": notes }}
    db.deals.update_one(myquery, newvalues)
    message = 'Deal information been updated in the database'
    return render_template('message.html', message=message)


@app.route("/delete_deal", methods=('GET', 'POST'))
def delete_deal():
    if request.method == 'POST':
        deal = request.form['deal']
        if deal == "unselected":
            message = "please select a valid deal"
            return render_template('delete_deal.html', message=message)

        temp = deal.split('-')
        number = temp[0]
        number = int(number)
        action = db.deals.delete_one({"number":number})
        message = "The Deal has been deleted"
        return render_template('message.html', message=message)

    # Get a list of deals
    my_deals = []
    deals = db.deals.find({})
    deal = loads(dumps(deals))
    for d in deal:
        number = d['number']
        number = str(number)
        deal = d['deal']
        dash = '-'
        deal = number+dash+deal
        my_deals.append(deal)
    return render_template('delete_deal.html', my_deals=my_deals)
'''
#-------------------------------------------------------------------------------
Login and Test Page Section
#-------------------------------------------------------------------------------
'''

@app.route("/")
def main():
    return render_template('login.html')

@app.route("/test")
def test():
    return render_template('test_table.html')

@app.route("/login", methods=('GET', 'POST'))
def login():
    return render_template('login.html')

'''
#-------------------------------------------------------------------------------
Build Creds database
#-------------------------------------------------------------------------------
'''

@app.route("/build_creds", methods=('GET', 'POST'))
def build_creds():
    username = request.form['username']
    password = request.form['password']
    passwordv = request.form['passwordv']

    # Are password the same
    if password != passwordv:
        message = "Passwords do not match"
        return render_template('creds.html', message=message)

    # Are any of the entries empty
    if username == "":
        message = "Username cannot be blank!"
        return render_template('creds.html', message=message)

    if password == "":
        message = "Password cannot be blank!"
        return render_template('creds.html', message=message)

    if passwordv == "":
        message = "Verification cannot be blank!"
        return render_template('creds.html', message=message)

    entry = {
        "username": username,
        "password": password
    }
    res = db.creds.insert_one(entry)
    message = "Credentials saved, proceed to login"
    return render_template('login.html', message=message)
'''
#-------------------------------------------------------------------------------
Home and Home_again
#-------------------------------------------------------------------------------
'''

@app.route("/home", methods=('GET', 'POST'))
def home():
    user = request.form['username']
    passwd = request.form['password']
    creds = db.creds.find({})
    creds = loads(dumps(creds))
    # Looking for creds
    if creds == []:
        return render_template('creds.html')

    if passwd == creds[0]['password']:
        my_actions = []
        my_logs = []
        deals = db.deals.count_documents({})
        logs = db.logs.count_documents({})
        actions = db.actions.count_documents({})
        company = db.company.count_documents({})
        customer = db.customer.count_documents({})
        meetings = db.meetings.count_documents({})
        travel = db.travel.count_documents({})
        stats = [deals,logs,actions,company,customer,meetings,travel]

        actions = get_actions(db)
        for a in actions:
            number = a['number']
            action = a['action']
            company = a['company']
            status = a['status']
            info = [number, company, action, status]
            my_actions.append(info)

        # return stats
        return render_template('home.html', stats=stats, my_actions=my_actions)
    else:
        error = 'Invalid Username or passsword'
        return render_template('login.html', error=error)

@app.route("/home_again", methods=('GET', 'POST'))
def home_again():
    # Check user credentials
    my_actions = []
    my_logs = []
    deals = db.deals.count_documents({})
    logs = db.logs.count_documents({})
    actions = db.actions.count_documents({})
    company = db.company.count_documents({})
    customer = db.customer.count_documents({})
    meetings = db.meetings.count_documents({})
    travel = db.travel.count_documents({})
    stats = [deals,logs,actions,company,customer,meetings,travel]


    actions = get_actions(db)
    for a in actions:
        number = a['number']
        action = a['action']
        company = a['company']
        status = a['status']
        info = [number, company, action, status]
        my_actions.append(info)

    # return stats
    return render_template('home.html', stats=stats, my_actions=my_actions)
'''
#-------------------------------------------------------------------------------
Travel Section
#-------------------------------------------------------------------------------
'''
@app.route("/add_travel", methods=('GET', 'POST'))
def add_travel():
    if request.method == 'POST':
        # Get count
        highest_record = db.travel.find({}).sort("number", pymongo.DESCENDING).limit(1)
        travel = loads(dumps(highest_record))
        if travel == []:
            number = 1
        else:
            number = travel[0]["number"] + 1
        # Generate UUID
        my_uuid = uuid.uuid4()
        my_uuid = str(my_uuid)
        entry = {
            "travel-desc": request.form['travel-desc'].replace("'", ""),
            "date-out": request.form['date-out'].replace("'", ""),
            "takeoff-out": request.form['takeoff-out'].replace("'", ""),
            "land-out": request.form['land-out'].replace("'", ""),
            "flight-out": request.form['flight-out'].replace("'", ""),
            "date-back": request.form['date-back'].replace("'", ""),
            "takeoff-back": request.form['takeoff-back'].replace("'", ""),
            "land-back": request.form['land-back'].replace("'", ""),
            "flight-back": request.form['flight-back'].replace("'", ""),
            "notes": request.form['notes'].replace("'", ""),
            "number": number,
            "uuid": my_uuid,
            "when": datetime.datetime.now()
        }
        res = db.travel.insert_one(entry)
        message = 'Travel data written to database'
        return render_template('message.html', message=message)

    # Send form
    return render_template('add_travel.html')

@app.route("/view_travel", methods=('GET', 'POST'))
def view_travel():
    if request.method == 'POST':
        travel_desc = request.form['travel-desc']
        if travel_desc == "unselected":
            my_travel = []
            travels = db.travel.find({})
            trav = loads(dumps(travels))
            for item in trav:
                travel_desc = item['travel-desc']
                my_travel.append(travel_desc)
            message = "please select a valid travel description"
            return render_template('select_travel.html', message=message, my_travel=my_travel)

        travel = db.travel.find({"travel-desc":travel_desc})
        trav = loads(dumps(travel))
        date_out = trav[0]['date-out']
        takeoff_out = trav[0]['takeoff-out']
        land_out = trav[0]['land-out']
        flight_out = trav[0]['flight-out']
        date_back = trav[0]['date-back']
        takeoff_back = trav[0]['takeoff-back']
        land_back = trav[0]['land-back']
        flight_back = trav[0]['flight-back']
        notes = trav[0]['notes']
        info = [travel_desc,date_out,takeoff_out,land_out,flight_out,date_back,takeoff_back,land_back,flight_back,notes]

        return render_template('view_travel.html', info=info)

    # Get a list of Companies
    my_travel = []
    travels = db.travel.find({})
    trav = loads(dumps(travels))
    for item in trav:
        travel_desc = item['travel-desc']
        my_travel.append(travel_desc)
    return render_template('select_travel.html', my_travel=my_travel)

@app.route("/edit_travel", methods=('GET', 'POST'))
def edit_travel():
    if request.method == 'POST':
        travel = request.form['travel']
        if travel == "unselected":
            message = "please select a valid travel record"
            # Get a list of customers
            my_travels = []
            travels = db.travel.find({})
            trav = loads(dumps(travels))
            for item in trav:
                number = item['number']
                number = str(number)
                travel_desc = item['travel-desc']
                dash = '-'
                trav = number+dash+travel_desc
                my_travels.append(trav)
            return render_template('edit_travel.html', my_travels=my_travels, message=message)

        temp = travel.split('-')
        number = temp[0]
        number = int(number)
        travels = db.travel.find({"number":number})
        trav = loads(dumps(travels))
        date_out = trav[0]['date-out']
        takeoff_out = trav[0]['takeoff-out']
        land_out = trav[0]['land-out']
        flight_out = trav[0]['flight-out']
        date_back = trav[0]['date-back']
        takeoff_back = trav[0]['takeoff-back']
        land_back = trav[0]['land-back']
        flight_back = trav[0]['flight-back']
        notes = trav[0]['notes']
        number = str(number)
        info = [temp[1],date_out,takeoff_out,land_out,flight_out,date_back,takeoff_back,land_back,flight_back,notes,number]
        return render_template('edit_travel_complete.html', info=info)

    # Get a list of customers
    my_travels = []
    travels = db.travel.find({})
    trav = loads(dumps(travels))
    for item in trav:
        number = item['number']
        number = str(number)
        travel_desc = item['travel-desc']
        dash = '-'
        trav = number+dash+travel_desc
        my_travels.append(trav)
    return render_template('edit_travel.html', my_travels=my_travels)

@app.route("/edit_travel_complete", methods=('GET', 'POST'))
def edit_travel_complete():
    travel = {}
    travel['travel_desc'] = request.form['travel-desc'].replace("'", "")
    travel['date-out'] = request.form['date-out'].replace("'", "")
    travel['takeoff-out'] = request.form['takeoff-out'].replace("'", "")
    travel['land-out'] = request.form['land-out'].replace("'", "")
    travel['flight-out'] = request.form['flight-out'].replace("'", "")
    travel['date-back'] = request.form['date-back'].replace("'", "")
    travel['takeoff-back'] = request.form['takeoff-back'].replace("'", "")
    travel['land-back'] = request.form['land-back'].replace("'", "")
    travel['flight-back'] = request.form['flight-back'].replace("'", "")
    travel['notes'] = request.form['notes'].replace("'", "")
    number = request.form['number'].replace("'", "")
    number = int(number)
    myquery = { "number": number }
    newvalues = { "$set": travel }
    db.travel.update_one(myquery, newvalues)
    message = 'Travel information been updated in the database'
    return render_template('message.html', message=message)

@app.route("/delete_travel", methods=('GET', 'POST'))
def delete_travel():
    if request.method == 'POST':
        travel = request.form['travel']
        if travel == "unselected":
            my_travels = []
            travs = db.travel.find({})
            trav = loads(dumps(travs))
            for item in trav:
                number = item['number']
                number = str(number)
                travel_desc = item['travel-desc']
                dash = '-'
                travel = number+dash+travel_desc
                my_travels.append(travel)
            message = "please select a valid meeting"
            return render_template('delete_travel.html', message=message, my_travels=my_travels)

        temp = travel.split('-')
        number = temp[0]
        number = int(number)
        meet = db.travel.delete_one({"number":number})
        message = "Travel entry has been deleted"
        return render_template('message.html', message=message)

    # Get a list of logs
    my_travels = []
    travs = db.travel.find({})
    trav = loads(dumps(travs))
    for item in trav:
        number = item['number']
        number = str(number)
        travel_desc = item['travel-desc']
        dash = '-'
        travel = number+dash+travel_desc
        my_travels.append(travel)
    return render_template('delete_travel.html', my_travels=my_travels)

'''
#-------------------------------------------------------------------------------
Log Section
#-------------------------------------------------------------------------------
'''

@app.route("/add_log", methods=('GET', 'POST'))
def add_log():
    if request.method == 'POST':
        # Get count
        highest_record = db.logs.find({}).sort("number", pymongo.DESCENDING).limit(1)
        log = loads(dumps(highest_record))
        if log == []:
            number = 1
        else:
            number = log[0]["number"] + 1
        # Generate UUID
        my_uuid = uuid.uuid4()
        my_uuid = str(my_uuid)
        entry = {
            "log_info": request.form['log_info'].replace("'", ""),
            "number": number,
            "uuid": my_uuid,
            "when": datetime.datetime.now()
        }
        res = db.logs.insert_one(entry)
        message = 'Log data written to database'
        return render_template('message.html', message=message)

    # Check user credentials
    return render_template('add_log.html')

@app.route("/list_log", methods=('GET', 'POST'))
def list_log():
    # Get a list of Actions
    my_logs = []
    log = db.logs.find({})
    logs = loads(dumps(log))
    for log in logs:
        number = log['number']
        log_entry = log['log_info']
        info = [number, log_entry]
        my_logs.append(info)

    # Check user credentials
    return render_template('list_logs.html', my_logs=my_logs)

@app.route("/edit_log", methods=('GET', 'POST'))
def edit_log():
    if request.method == 'POST':
        log_info = request.form['log_info']
        if log_info == "unselected":
            message = "please select a valid log"
            # Get a list of prep_logs
            my_logs = []
            logs = db.logs.find({})
            log = loads(dumps(logs))
            for item in log:
                number = item['number']
                number = str(number)
                log_info = item['log_info']
                dash = '-'
                log = number+dash+log_info
                my_logs.append(log)
            return render_template('edit_log.html', my_logs=my_logs, message=message)

        temp = log_info.split('-')
        number = temp[0]
        number = int(number)
        logs = db.logs.find({"number":number})
        log = loads(dumps(logs))
        log_info = log[0]['log_info']
        return render_template('edit_log_complete.html', log_info=log_info, number=number)

    # Get a list of prep_logs
    my_logs = []
    logs = db.logs.find({})
    log = loads(dumps(logs))
    for item in log:
        number = item['number']
        number = str(number)
        log_info = item['log_info']
        dash = '-'
        log = number+dash+log_info
        my_logs.append(log)
    return render_template('edit_log.html', my_logs=my_logs)

@app.route("/edit_log_complete", methods=('GET', 'POST'))
def edit_log_complete():
        number = request.form['number'].replace("'", "")
        log_info = request.form['log_info'].replace("'", "")
        number = int(number)
        myquery = { "number": number }
        newvalues = { "$set": { "log_info": log_info }}
        db.logs.update_one(myquery, newvalues)
        message = 'Log information been updated in the database'
        return render_template('message.html', message=message)

@app.route("/delete_log", methods=('GET', 'POST'))
def delete_log():
    if request.method == 'POST':
        log = request.form['log_info']
        if log == "unselected":
            message = "please select a valid action"
            return render_template('delete_log.html', message=message)

        temp = log.split('-')
        number = temp[0]
        number = int(number)
        log = db.logs.delete_one({"number":number})
        message = "Log entry has been deleted"
        return render_template('message.html', message=message)

    # Get a list of logs
    my_logs = []
    logs = db.logs.find({})
    log = loads(dumps(logs))
    for l in log:
        number = l['number']
        number = str(number)
        log_info = l['log_info']
        dash = '-'
        log = number+dash+log_info
        my_logs.append(log)
    return render_template('delete_log.html', my_logs=my_logs)
'''
#-------------------------------------------------------------------------------
Action Item Section
#-------------------------------------------------------------------------------
'''

@app.route("/add_action", methods=('GET', 'POST'))
def add_action():

    if request.method == 'POST':
        # Get count
        highest_record = db.actions.find({}).sort("number", pymongo.DESCENDING).limit(1)
        action = loads(dumps(highest_record))
        if action == []:
            number = 1
        else:
            number = action[0]["number"] + 1
        # Generate UUID
        my_uuid = uuid.uuid4()
        my_uuid = str(my_uuid)
        entry = {
            "action": request.form['action'].replace("'", ""),
            "company": request.form['company'].replace("'", ""),
            "number": number,
            "uuid": my_uuid,
            "status": "open",
            "when": datetime.datetime.now()
        }
        if entry["company"] == "unselected":
            # Get a list of Companies
            my_companies = []
            companies = db.company.find({})
            comp = loads(dumps(companies))
            for c in comp:
                name = c['name']
                my_companies.append(name)
            message = "please select a valid company"
            return render_template('add_action.html', message=message, action=entry['action'], my_companies=my_companies)

        res = db.actions.insert_one(entry)
        message = 'Action Item information written to database'
        return render_template('message.html', message=message)

    # Get a list of Companies
    my_companies = []
    companies = db.company.find({})
    comp = loads(dumps(companies))
    for c in comp:
        name = c['name']
        my_companies.append(name)

    return render_template('add_action.html', my_companies=my_companies)

@app.route("/list_action", methods=('GET', 'POST'))
def list_action():
    # Get a list of Actions
    my_actions = []
    act = db.actions.find({})
    action = loads(dumps(act))
    for a in action:
        number = a['number']
        action = a['action']
        company = a['company']
        status = a['status']
        info = [number, company, action, status]
        my_actions.append(info)

    return render_template('list_actions.html', my_actions=my_actions)

@app.route("/edit_action", methods=('GET', 'POST'))
def edit_action():
    if request.method == 'POST':
        action = request.form['action']
        if action == "unselected":
            message = "please select a valid action"
            # Get a list of actions
            my_actions = []
            actions = db.actions.find({})
            act = loads(dumps(actions))
            for a in act:
                number = a['number']
                number = str(number)
                action = a['action']
                dash = '-'
                action = number+dash+action
                my_actions.append(action)
            return render_template('edit_action.html', my_actions=my_actions, message=message)

        temp = action.split('-')
        number = temp[0]
        number = int(number)
        action = db.actions.find({"number":number})
        act = loads(dumps(action))
        action = act[0]['action']
        return render_template('edit_action_complete.html', action=action, number=number)

    # Get a list of actions
    my_actions = []
    actions = db.actions.find({})
    act = loads(dumps(actions))
    for a in act:
        number = a['number']
        number = str(number)
        action = a['action']
        dash = '-'
        action = number+dash+action
        my_actions.append(action)
    return render_template('edit_action.html', my_actions=my_actions)

@app.route("/edit_action_complete", methods=('GET', 'POST'))
def edit_action_complete():
    action = request.form['action'].replace("'", "")
    number = request.form['number'].replace("'", "")
    status = request.form['status'].replace("'", "")
    number = int(number)
    myquery = { "number": number }
    newvalues = { "$set": { "action": action, "status": status }}
    db.actions.update_one(myquery, newvalues)
    message = 'Action Item information been updated in the database'
    return render_template('message.html', message=message)

@app.route("/delete_action", methods=('GET', 'POST'))
def delete_action():
    if request.method == 'POST':
        action = request.form['action']
        if action == "unselected":
            message = "please select a valid action"
            return render_template('delete_action.html', message=message)

        temp = action.split('-')
        number = temp[0]
        number = int(number)
        action = db.actions.delete_one({"number":number})
        message = "Action item has been deleted"
        return render_template('message.html', message=message)

    # Get a list of actions
    my_actions = []
    actions = db.actions.find({})
    act = loads(dumps(actions))
    for a in act:
        number = a['number']
        number = str(number)
        action = a['action']
        dash = '-'
        action = number+dash+action
        my_actions.append(action)
    return render_template('delete_action.html', my_actions=my_actions)
'''
#-------------------------------------------------------------------------------
Company Section
#-------------------------------------------------------------------------------
'''

@app.route("/add_company", methods=('GET', 'POST'))
def add_company():
    if request.method == 'POST':
        # Generate UUID
        my_uuid = uuid.uuid4()
        my_uuid = str(my_uuid)
        highest_record = db.company.find({}).sort("number", pymongo.DESCENDING).limit(1)
        company = loads(dumps(highest_record))
        if company == []:
            number = 1
        else:
            number = company[0]["number"] + 1

        entry = {
            "name": request.form['company'].replace("'", ""),
            "uuid": my_uuid,
            "number": number,
            "when": datetime.datetime.now()
        }

        res = db.company.insert_one(entry)
        message = 'Company information written to database'
        return render_template('message.html', message=message)
    # Check user credentials
    return render_template('add_company.html')



@app.route("/list_company", methods=('GET', 'POST'))
def list_company():
    # Get a list of Companies
    my_companies = []
    companies = db.company.find({})
    company = loads(dumps(companies))
    for c in company:
        name = c['name']
        number = c['number']
        info = [number, name]
        my_companies.append(info)

    return render_template('list_company.html', my_companies=my_companies)

@app.route("/delete_company", methods=('GET', 'POST'))
def delete_company():
    if request.method == 'POST':
        comp = request.form['company']
        if comp == "unselected":
            message = "please select a valid company"
            return render_template('delete_company.html', message=message)

        temp = comp.split('-')
        number = temp[0]
        number = int(number)
        meet = db.company.delete_one({"number":number})
        message = "Company entry has been deleted"
        return render_template('message.html', message=message)
    # Get a list of logs
    my_companies = []
    comps = db.company.find({})
    comp = loads(dumps(comps))
    for item in comp:
        number = item['number']
        number = str(number)
        name = item['name']
        dash = '-'
        company = number+dash+name
        my_companies.append(company)
    return render_template('delete_company.html', my_companies=my_companies)
'''
#-------------------------------------------------------------------------------
Contact Section
#-------------------------------------------------------------------------------
'''

@app.route("/add_customer", methods=('GET', 'POST'))
def add_customer():
    if request.method == 'POST':
        # Generate UUID
        my_uuid = uuid.uuid4()
        my_uuid = str(my_uuid)
        highest_record = db.customer.find({}).sort("number", pymongo.DESCENDING).limit(1)
        customer = loads(dumps(highest_record))
        if customer == []:
            number = 1
        else:
            number = customer[0]["number"] + 1

        entry = {
            "company": request.form['company'].replace("'", ""),
            "name": request.form['name'].replace("'", ""),
            "phone": request.form['phone'].replace("'", ""),
            "email": request.form['email'].replace("'", ""),
            "uuid": my_uuid,
            "number": number,
            "when": datetime.datetime.now()
        }
        if entry["company"] == "unselected":
            # Get a list of Companies
            my_companies = []
            companies = db.company.find({})
            comp = loads(dumps(companies))
            for c in comp:
                name = c['name']
                my_companies.append(name)
            message = "please select a valid company"
            return render_template('add_customer.html', message=message, my_companies=my_companies)

        res = db.customer.insert_one(entry)
        message = 'Customer information written to database'
        return render_template('message.html', message=message)

    # Get a list of Companies
    my_companies = []
    companies = db.company.find({})
    comp = loads(dumps(companies))
    for c in comp:
        name = c['name']
        my_companies.append(name)
    # Check user credentials
    return render_template('add_customer.html', my_companies=my_companies)

@app.route("/list_customer", methods=('GET', 'POST'))
def list_customer():
    my_customers = []
    cust = db.customer.find({})
    customer = loads(dumps(cust))
    for c in customer:
        number = c['number']
        name = c['name']
        phone = c['phone']
        email = c['email']
        company = c['company']
        info = [number, name, phone, email, company]
        my_customers.append(info)
    # Check user credentials
    return render_template('list_customer.html', my_customers=my_customers)

@app.route("/edit_customer", methods=('GET', 'POST'))
def edit_customer():
    if request.method == 'POST':
        log_info = request.form['customer']
        if log_info == "unselected":
            message = "please select a valid customer"
            # Get a list of customers
            my_customers = []
            customer = db.customer.find({})
            cust = loads(dumps(customer))
            for item in cust:
                number = item['number']
                number = str(number)
                name = item['name']
                dash = '-'
                cust = number+dash+name
                my_customers.append(cust)
            return render_template('edit_customer.html', my_customers=my_customers, message=message)

        temp = log_info.split('-')
        number = temp[0]
        number = int(number)
        customer = db.customer.find({"number":number})
        cust = loads(dumps(customer))
        name = cust[0]['name']
        phone = cust[0]['phone']
        email = cust[0]['email']
        return render_template('edit_customer_complete.html', name=name, phone=phone, email=email, number=number)

    # Get a list of customers
    my_customers = []
    customer = db.customer.find({})
    cust = loads(dumps(customer))
    for item in cust:
        number = item['number']
        number = str(number)
        name = item['name']
        dash = '-'
        cust = number+dash+name
        my_customers.append(cust)
    return render_template('edit_customer.html', my_customers=my_customers)

@app.route("/edit_customer_complete", methods=('GET', 'POST'))
def edit_customer_complete():
    name = request.form['name'].replace("'", "")
    number = request.form['number'].replace("'", "")
    phone = request.form['phone'].replace("'", "")
    email = request.form['email'].replace("'", "")
    number = int(number)
    myquery = { "number": number }
    newvalues = { "$set": { "name": name, "phone": phone, "email": email }}
    db.customer.update_one(myquery, newvalues)
    message = 'Customer information been updated in the database'
    return render_template('message.html', message=message)

@app.route("/delete_customer", methods=('GET', 'POST'))
def delete_customer():
    if request.method == 'POST':
        cust = request.form['customer']
        if cust == "unselected":
            message = "please select a valid customer"
            return render_template('delete_customer.html', message=message)

        temp = cust.split('-')
        number = temp[0]
        number = int(number)
        meet = db.customer.delete_one({"number":number})
        message = "Customer entry has been deleted"
        return render_template('message.html', message=message)
    # Get a list of logs
    my_customer = []
    cust = db.customer.find({})
    cust = loads(dumps(cust))
    for item in cust:
        number = item['number']
        number = str(number)
        name = item['name']
        dash = '-'
        customer = number+dash+name
        my_customer.append(customer)
    return render_template('delete_customer.html', my_customer=my_customer)
'''
#-------------------------------------------------------------------------------
Magic 8 Ball
#-------------------------------------------------------------------------------
'''


@app.route("/magic", methods=('GET', 'POST'))
def magic():
    # Check user credentials
    return render_template('magic.html')
'''
#-------------------------------------------------------------------------------
Load and Database Section
#-------------------------------------------------------------------------------
'''

@app.route("/load_warn", methods=('GET', 'POST'))
def load_warn():
    return render_template('load_warn.html')

@app.route("/load", methods=('GET', 'POST'))
def load():
    # open the file for reading
    f = open("da5id_data.txt", "r")
    while True:
        # read a single line
        line = f.readline()
        line = line.rstrip()
        if not line:
            break
        if line[0] == "@":
            junk, dbname = line.split('-')
            line = f.readline()
            line = line.rstrip()
        process = process_line(db,dbname,line)
    # close the pointer to that file
    f.close()
    message = "database has been loaded"
    return render_template('message.html', message=message)

@app.route("/dump", methods=('GET', 'POST'))
def dump():
    # Get db records and dump them to a file
    actions = prep_actions(db)
    logs = prep_logs(db)
    deal = prep_deals(db)
    company = prep_company(db)
    customer = prep_customer(db)
    meetings = prep_meeting(db)
    travel = prep_travel(db)
    message = "database has been written to da5id_data.txt"
    return render_template('message.html', message=message)
'''
#-------------------------------------------------------------------------------
Logout
#-------------------------------------------------------------------------------
'''

@app.route("/logout", methods=('GET', 'POST'))
def logout():
    # Check user credentials
    return render_template('logout.html')
'''
#-------------------------------------------------------------------------------
Meeting Section
#-------------------------------------------------------------------------------
'''

@app.route("/add_meeting", methods=('GET', 'POST'))
def add_meeting():
    if request.method == 'POST':
        # Generate UUID
        my_uuid = uuid.uuid4()
        my_uuid = str(my_uuid)
        highest_record = db.meetings.find({}).sort("number", pymongo.DESCENDING).limit(1)
        meeting = loads(dumps(highest_record))
        if meeting == []:
            number = 1
        else:
            number = meeting[0]["number"] + 1
        entry = {
            "company": request.form['company'].replace("'", ""),
            "title": request.form['title'].replace("'", ""),
            "notes": request.form['notes'].replace("'", ""),
            "uuid": my_uuid,
            "number": number,
            "when": datetime.datetime.now()
        }
        if entry["company"] == "unselected":
            # Get a list of Companies
            my_companies = []
            companies = db.company.find({})
            comp = loads(dumps(companies))
            for c in comp:
                name = c['name']
                my_companies.append(name)
            message = "please select a valid company"
            return render_template('add_meeting.html', message=message, my_companies=my_companies, notes=entry['notes'])

        res = db.meetings.insert_one(entry)
        message = 'Meeting notes have been written to database'
        return render_template('message.html', message=message)

    # Get a list of Companies
    my_companies = []
    companies = db.company.find({})
    comp = loads(dumps(companies))
    for c in comp:
        name = c['name']
        my_companies.append(name)
    # Check user credentials
    return render_template('add_meeting.html', my_companies=my_companies)

@app.route("/view_meeting", methods=('GET', 'POST'))
def view_meeting():
    if request.method == 'POST':
        title = request.form['title']
        if title == "unselected":
            my_meetings = []
            meetings = db.meetings.find({})
            meet = loads(dumps(meetings))
            for m in meet:
                title = m['title']
                my_meetings.append(title)
            message = "please select a valid meeting title"
            return render_template('select_meeting.html', message=message, my_meetings=my_meetings)

        meeting = db.meetings.find({"title":title})
        meet = loads(dumps(meeting))
        title = meet[0]['title']
        notes = meet[0]['notes']
        company = meet[0]['company']
        return render_template('view_meeting.html', company=company, title=title, notes=notes)

    # Get a list of Companies
    my_meetings = []
    meetings = db.meetings.find({})
    meet = loads(dumps(meetings))
    for m in meet:
        title = m['title']
        my_meetings.append(title)
    return render_template('select_meeting.html', my_meetings=my_meetings)

@app.route("/edit_meeting", methods=('GET', 'POST'))
def edit_meeting():
    if request.method == 'POST':
        meeting = request.form['meeting']
        if meeting == "unselected":
            message = "please select a valid meeting"
            # Get a list of meetings
            my_meetings = []
            meetings = db.meetings.find({})
            meet = loads(dumps(meetings))
            for item in meet:
                number = item['number']
                number = str(number)
                title = item['title']
                company = item['company']
                dash = '-'
                meet = number+dash+title+company
                my_meetings.append(meet)
            return render_template('edit_meeting.html',my_meetings=my_meetings, message=message)

        temp = meeting.split('-')
        number = temp[0]
        number = int(number)
        meeting = db.meetings.find({"number":number})
        meet = loads(dumps(meeting))
        title = meet[0]['title']
        notes = meet[0]['notes']
        company = meet[0]['company']
        return render_template('edit_meeting_complete.html', title=title, notes=notes, company=company, number=number)

    # Get a list of meetings
    my_meetings = []
    meetings = db.meetings.find({})
    meet = loads(dumps(meetings))
    for item in meet:
        number = item['number']
        number = str(number)
        title = item['title']
        company = item['company']
        dash = '-'
        meet = number+dash+title+company
        my_meetings.append(meet)
    return render_template('edit_meeting.html', my_meetings=my_meetings)

@app.route("/edit_meeting_complete", methods=('GET', 'POST'))
def edit_meeting_complete():
    title = request.form['title'].replace("'", "")
    number = request.form['number'].replace("'", "")
    notes = request.form['notes'].replace("'", "")
    number = int(number)
    myquery = { "number": number }
    newvalues = { "$set": { "notes": notes }}
    db.meetings.update_one(myquery, newvalues)
    message = 'Meeitng notes have been updated in the database'
    return render_template('message.html', message=message)

@app.route("/delete_meeting", methods=('GET', 'POST'))
def delete_meeting():
    if request.method == 'POST':
        meet = request.form['meeting']
        if meet == "unselected":
            message = "please select a valid meeting"
            return render_template('delete_meeting.html', message=message)

        temp = meet.split('-')
        number = temp[0]
        number = int(number)
        meet = db.meetings.delete_one({"number":number})
        message = "Meeting entry has been deleted"
        return render_template('message.html', message=message)
    # Get a list of logs
    my_meetings = []
    meets = db.meetings.find({})
    meet = loads(dumps(meets))
    for m in meet:
        number = m['number']
        number = str(number)
        title = m['title']
        company = m['company']
        dash = '-'
        meet = number+dash+title+dash+company
        my_meetings.append(meet)
    return render_template('delete_meeting.html', my_meetings=my_meetings)
