import requests
import urllib2

def get_geo_location(address):
	# some weird stuff is going on with the certificate
	requests.packages.urllib3.disable_warnings()

	r = requests.get('https://marmot.ripe.net/openipmap/ipmeta.json?ip=%s' % address, verify=False)
	json_result = r.json()
	rv = {'lat': None, 'lon': None, 'city': None}
	print json_result
	if len( json_result['crowdsourced'] ) > 0:
            loc = json_result['crowdsourced'][0]
            if 'lat' in loc and 'lon' in loc:
               rv['lat'] = loc['lat']
               rv['lon'] = loc['lon']
            if 'canonical_georesult' in loc:
               rv['city'] = loc['canonical_georesult']
	print rv

# Test the code / How to use
#get_geo_location('194.68.123.238')