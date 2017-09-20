import requests
import pyparsing as pp
from pprint import pprint

def parse_verbs():
	get = pp.Literal("GET")
	post = pp.Literal("POST")
	options = pp.Literal("OPTIONS")
	put=pp.Literal("PUT")
	patch=pp.Literal("PATCH")
	delete=pp.Literal("DELETE")
	connect=pp.Literal("CONNECT")
	trace=pp.Literal("TRACE")
	track=pp.Literal("TRACK")
	head = pp.Literal("HEAD")
	crappaton = pp.Word(pp.printables).setResultsName('bleed')
	headers = pp.ZeroOrMore(get|post|head|options|put|patch|delete|connect|trace|track).setResultsName('headers')
	verb = pp.Dict(pp.Group((headers+pp.ZeroOrMore(crappaton))).setResultsName('results'))
	return verb
	

def get_verbs(url):
	try:
		requests.packages.urllib3.disable_warnings()
		res=requests.options(url,verify=False)
		if "allow" in res.headers:
			verbs = res.headers['allow']+"PAPAPAPA"
			if verbs is "":
				return "EMPTY"
			else:
				return verbs.replace(',', '')
		else:
			return "ERROR"
	except Exception as e:
		print "ERROR "+url+" : "+str(e)
		return "ERROR"
		
		
def check_bleeding(url,retests):
	for i in range(retests):
		print str(i+1),
		verbs=get_verbs(url)
		if (verbs == "EMPTY"):
			return url+" : ERROR EMPTY"
		else:
			parsed_verbs = (parse_verbs().parseString(verbs)).asDict()
			if "bleed" in parsed_verbs["results"]:
				if parsed_verbs["results"]["bleed"] is "":
					return url+" : EMPTY"
				elif "ERROR" in parsed_verbs["results"]["bleed"]:
					return url+" : ERROR"
				else:
					return 'BLEEDING: '+parsed_verbs["results"]["bleed"]
	return url+" : NO BLEEDING "


def http_url(url):
	return "http://"+url.rstrip()+"/"
def https_url(url):
	return "https://"+url.rstrip()+"/"


def main():
	with open("input.txt","r") as input,open("output.txt","w") as output:
		progress=""
		iters = 1
		for line in input.readlines():
			checked=check_bleeding(http_url(line),iters)+"\n"
			checked+=check_bleeding(https_url(line),iters)+"\n"
			print checked
			progress+=checked
		output.write(progress)

if __name__ == "__main__":
    main()
