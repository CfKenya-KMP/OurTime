from flask import (Flask, g, request, session, redirect,
        url_for, render_template, jsonify)
from flask_script import Manager
import redis, os
from normality import slugify
from OurTime2Eat.otte import config as config_file

app = Flask(__name__,
        template_folder=os.getenv('OTTE_TEMPLATES'),
        static_folder=os.getenv('OTTE_STATIC'))
app.config.from_object(config_file)

def get_db():
    if not hasattr(g, 'redis'):
        g.redis = redis.StrictRedis(**app.config['REDIS'])
    return g.redis


def todigit(number=""):
    '''
    returns number in digits

    currently supports numbers in the format:
    'xx million'  ,  'xx billion' , 'xx thousand' , 'xx hundred'
    '''
    notations = dict(million="000000", billion="000000000", thousand="000", hundred="00")
    if str(number).isdigit():
        return int(float(number))
    else:
        try:
            num, notation = number.split(' ')
        except ValueError:
            print "ERROR: Unknown number format"
            return 0
        if notation not in notations.keys():
            print "ERROR: Unknown notation"
            return 0
        else:
            try:
                whole, fraction = num.split('.')
            except ValueError:
                whole = num
                fraction = 0

            whole_num = "%s%s" % (whole, notations[notation])
            fract_num = float("0.%s" % fraction) * int("1%s" % notations[notation])
            number_dig = int(whole_num) + int(fract_num)
            return number_dig


def get_county_data(county):
    '''
    '''
    rds = get_db()
    resp = eval(rds.get(slugify(county)))
    travel_budget = todigit(resp['travel']['budget'] + ' million')
    hospitality_budget = todigit(resp.get('hospitality_budget', 0))
    total_budget = todigit(resp.get('total_budget', 0))
    gov = resp['governance']

    hospitality_ratio = (hospitality_budget / total_budget) * 100.0
    travel_ratio = (float(travel_budget) / float(total_budget)) * 100.0
    ratio = (hospitality_budget + travel_budget) / float(total_budget) * 100

    # ranking
    rank = 0
    county_payload = dict(
            county=county,
            county_str=county.capitalize(),
            governor=gov['governor'],
            governor_img=resp['governor_image'],
            rank=rank,
            ratio=ratio,
            hospitality=hospitality_budget,
            hospitality_remainder=total_budget - hospitality_budget,
            travel=travel_budget,
            travel_remainder=total_budget - travel_budget,
            hospitality_str=resp.get('hospitality_budget', 0),
            travel_str=resp['travel']['budget'] + ' million'
            )
    
    return county_payload


def sort_list_by_key(list_, key):
    '''
    @list_ :  a list of <dict> objects with a `key` key
    @key   :  a key in all <dict> objects in `list_`. Value of `key` must be an <int>
    '''
    try:
        return sorted(list_, key=lambda k: k[key])
    except Exception, err:
        print "ERROR: Failed to sort list -- %s" % str(err)
        return list_


### VIEWS

@app.route('/')
def home():
    '''
    index.html
    '''
    # get the data
    county_data = []
    for county in app.config['COUNTIES']:
        if not county in app.config['NODATA']:
            county_payload = get_county_data(county)
            county_data.append(county_payload)
            print "Added %s to final list" % (county)
    
    sorted_resp = sort_list_by_key(county_data, 'ratio')
    sorted_data = []
    rank = 1
    for each in sorted_resp:
        each['rank'] = rank
        sorted_data.append(each)
        rank += 1

    reverse_sorted = []
    for idx in range(0, len(sorted_data)):
        reverse_sorted.append(sorted_data.pop())
    
    section_one = reverse_sorted[0]
    section_two = reverse_sorted[1:11]
    section_three = reverse_sorted[11:len(reverse_sorted)-1]

    print sorted_data
    
    return render_template('index.html',
            section_one=section_one,
            section_two=section_two,
            section_three=section_three)


@app.route('/subpage.html')
def subpage():
    '''
    '''
    args = request.args.copy()
    _county = args['county']

    # all county data
    county_data = []
    for county in app.config['COUNTIES']:
        if not county in app.config['NODATA']:
            county_payload = get_county_data(county)
            county_data.append(county_payload)
    sorted_data = []
    rank = 1
    for each in sort_list_by_key(county_data, 'ratio'):
        each['rank'] = rank
        sorted_data.append(each)
        rank += 1

        if each['county'] == _county: # hook to isolate the `_county`
            _county_data = each
    return render_template('subpage.html', this_county=_county_data, county_payload=sorted_data)



### END OF VIEWS

manager = Manager(app)

if __name__ == "__main__":
    manager.run()
