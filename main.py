 #!/usr/bin/python3 

import config as cfg
import APIKeys as keys
import urllib3
import json

from collections import OrderedDict
from flask import Flask
from flask import jsonify
from flask import request
app = Flask(__name__)

@app.route("/",methods=['GET'])

def main():
#Build up input url
	theMeasures = request.args.get('theMeasures')
	dateParam = request.args.get('dateParam')
	print (request.args)
	if cfg.testResponse != '':
		Soutput = parseJsonWunderground(cfg.testResponse)
	else:
		Surl = cfg.weatherHistory['url'] + keys.APIKeys['WundergroundKey'] + cfg.weatherHistory['url2'] + dateParam + cfg.weatherHistory['url3']
		http = urllib3.PoolManager()
		print(Surl)
		r = http.request('GET',Surl)
		j = json.loads(r.data.decode('utf-8'))
		return parseJsonWunderground(j,theMeasures)
		

# {
#   "graph" : {
#     "title": "Body measurements",
#     "datasequences" : [
#       {
#         "title" : "Chest Measurements",
#         "datapoints" : [
#           { "title" : "1-3-2012", "value" : 45.5 },
#           { "title" : "1-10-2012", "value" : 45.5 },
#           { "title" : "1-17-2012" },
#           { "title" : "1-24-2012", "value" : 44.5 }
#         ]
#       },
#       {
#         "title" : "Narrowest waist point",
#         "datapoints" : [
#           { "title" : "1-3-2012", "value" : 38.6 },
#           { "title" : "1-10-2012", "value" : 38.1 },
#           { "title" : "1-17-2012", "value" : 38 },
#           { "title" : "1-24-2012", "value" : 38 }
#         ]
#       }
#     ]
#   }
# }

def parseJsonWunderground(s1,s2):
#Fix up the json string to send to Datadog.
	print (s2)
	output = []
	graph=OrderedDict()
	graph['title'] = 'Daily History'
	datasequences = OrderedDict()
	graph['datasequences'] = datasequences

	for days in s1['history']['observations']:
		for key in days:
			#Check if required
			if key in s2:
				if key not in datasequences:
					datasequences[key] = OrderedDict({'title':key,'datapoints':[]})
				theDate = days['date']
				temp = {'title': theDate['mon']+'-'+theDate['mday']+'-'+theDate['year']+'-'+theDate['hour']+':'+theDate['min'],'value':days[key]}
				datasequences[key]['datapoints'].append(temp)


	
	#format graph
	dReturn={}
	dReturn['title']='Daily History'
	dReturn['datasequences'] = []

	#Fix Format to match TheDash
	for keys in datasequences:
		tempArray=[]
		for items in datasequences[keys]['datapoints']:
			tempArray.append(items)
		dReturn['datasequences'].append({'title':datasequences[keys]['title'],'datapoints':tempArray})



	return (jsonify({'graph':dReturn}))

def is_number(s):
    try:
        complex(s) # for int, long, float and complex
    except ValueError:
        return False

    return True

if __name__ == "__main__":
	main()