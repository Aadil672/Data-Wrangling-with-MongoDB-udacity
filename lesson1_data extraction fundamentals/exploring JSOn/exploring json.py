"""
To experiment with this code freely you will have to run this code locally.
Take a look at the main() function for an example of how to use the code. We
have provided example json output in the other code editor tabs for you to look
at, but you will not be able to run any queries through our UI.
"""
import json
import requests

BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"


# query parameters are given to the requests.get function as a dictionary; this
# variable contains some starter parameters.
query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    """
    This is the main function for making queries to the musicbrainz API. The
    query should return a json document.
    """
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    """
    This adds an artist name to the query parameters before making an API call
    to the function above.
    """
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    """
    After we get our output, we can use this function to format it to be more
    readable.
    """
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():

	results = query_by_name(ARTIST_URL, query_type["simple"], "First Aid Kit")
    count= 0

    for artist in results["artists"]:
        if artist["name"] == "First Aid Kit":
            count+= 1
	print count
	
    # Begin_area name for Queen?
	queen = query_by_name(ARTIST_URL, query_type["simple"], "QUEEN")
	print [str(artist['begin-area']['name']) for artist in queen['artists'] if
	artist['name'] == 'Queen' and 'begin-area' in artist and 'name' in artist['begin-area']]
	
	#spanish alias for beatles 
	beatles = query_by_name(ARTIST_URL, query_type["simple"], "BEATLES")
	for artist in beatles['artists']:
		if 'aliases' in artist:
			for alias in artist['aliases']:
				if alias['locale']=='es':
					print alias['locale']
					print str(alias['name'])
		
	
    # Query for releases from that band using the artist_id
	nirvana = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
	for artist in nirvana['artists']:
		if 'disambiguation' in artist :
			print str(artist['disambiguation'])
			
	# where was one direction formed
	onedirection = query_by_name(ARTIST_URL, query_type["simple"], "one direction")
	#pretty_print(onedirection)
	for artist in onedirection['artists']:
		if artist['name']=='One Direction':
			print str(artist['life-span'])
			

if __name__ == '__main__':
    main()