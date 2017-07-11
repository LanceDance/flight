import requests
import argparse
import datetime
import json

parser = argparse.ArgumentParser(description='Kiwi weekend.')
parser.add_argument('--from', required=True)
parser.add_argument('--to', required=True)
parser.add_argument('--date', required=True)
parser.add_argument('--one-way', action='store_true')
parser.add_argument('--cheapest', action='store_true')
parser.add_argument('--shortest', action='store_true')
parser.add_argument('--return')

args = vars(parser.parse_args())


check_flight = { 'flyFrom': None, 'to': None,
                 'dateFrom': None, 'dateTo': None,
                 'daysInDestinationFrom': None,
                 'sort': None,
                 'typeFlight': None
}

days = datetime.datetime.strptime(args['date'], '%Y-%m-%d').strftime('%d/%m/%Y')
check_flight['dateFrom'] = days

check_flight['typeFlight'] = 'oneway'
check_flight['sort'] = 'price'

if args['one_way']:
    check_flight['typeFlight'] = 'oneway'


check_flight['flyFrom'] = args['from']
check_flight['to'] = args['to']



if args['shortest']:
    check_flight['sort'] = 'duration'



if args['return']:
    check_flight['typeFlight'] = 'round'


if check_flight['typeFlight'] == 'round':
    check_flight['daysInDestinationFrom'] = args['return']
    check_flight['typeFlight'] = None


r = requests.get('https://api.skypicker.com/flights', params=check_flight)
flight = r.json()['data'][0]


#booking of the flight

url = 'http://37.139.6.125:8080/booking'


information = {
  "passengers": [
    {
      "firstName": "Kaja",
      "birthday": "1901-12-12",
      "lastName": "test",
      "title": "Mr",
      "documentID": "bla bla bla bla",
      "email": "kecyprdbedary@ihatemonday.com"
    }
  ],
  "currency": "EUR",
  "booking_token": flight['booking_token'],

}

headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(information), headers=headers)

print("Hurray we found your flight! Only for " + str(flight['price']) + " EUR and remember the id of reservation "
      + str(r.json()['pnr']) + "!!!!!!!!")

