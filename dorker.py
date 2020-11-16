# Dorker: perform a list of google dorks on a given domain
# using python googlesearch (https://python-googlesearch.readthedocs.io/en/latest/)

import os
import argparse
from random import randint
from time import sleep
from termcolor import colored
from googlesearch import search, get_random_user_agent
import urllib.error

def prepare_query_domains(domain):
	"""
	prepare a domain or a list of domains for google query (adding site:*.)
	"""
	domain = domain.replace(" " , "").replace("," , " OR site:*.")
	domain = "site:*." + domain
	domain = domain.replace(".." , ".")
	return domain


def print_header():
	nameArt= r'''
	 __   __   __        ___  __  
	|  \ /  \ |__) |__/ |__  |__) 
	|__/ \__/ |  \ |  \ |___ |  \ 
                             
	'''	
	print(colored(nameArt, 'magenta', attrs=['bold']))


def google_search(query, resultsToRetrieve, userAgent, sleepDelay=1):
	"""
	perform google search and handle exceptions
	"""
	try:
		search_results = search(query, stop=resultsToRetrieve, user_agent=get_random_user_agent())
		#search_results = ["test result 1","test result 2"]
		if search_results != None: #i dont know why i need this for exception handling to work!!
			for item in search_results:
				pass
		# 		#print(str(item))
	except urllib.error.HTTPError as e:
		if e.code == 429 or str(e) == "HTTP Error 429: Too Many Requests":
			print(colored('\tRejected, sleeping for '+str(sleepDelay)+' min..', 'red'))
			sleep((sleepDelay * 60))
			print('\tRetrying..')
			google_search(query, resultsToRetrieve, userAgent, (sleepDelay * 2))
	else:
		return search_results


def dorkit (payloadsFile, domain, outputFolder, resultsToRetrieve, userAgent, additionalQuery): 
	"""
	perform google search and save to output files
	"""

	outputFile = outputFolder + "/" + domain.split(",")[0]
	queryDomain = prepare_query_domains(domain)
	currnetDorkIndex = 1
	totalDorks = len(open(payloadsFile).readlines(  ))


	print ("\nTarget domain(s): " + domain)
	print ("Output directory: " + outputFolder)
	print ("Results will be saved to: " + outputFile)
	print ("\nReading payload file: " + payloadsFile)
	print ("Number of dorks found:  " + str(totalDorks))


	#check session
	sessionIndex = check_session(outputFolder+"/dorker.session")
	with open(payloadsFile, 'r') as payloads:
		for payload in list(payloads.readlines()):

			if(currnetDorkIndex <= sessionIndex):
				currnetDorkIndex = currnetDorkIndex + 1
				continue

			
			payload = payload.rstrip('\n')
			print ('\n[+] Checking ('+ str(currnetDorkIndex) +'/'+ str(totalDorks) +'): ' + payload )
			try:
				dork = queryDomain + " " + payload +" "+ additionalQuery
				print ("\tQuery: "+ dork)
				
				results = google_search(dork, resultsToRetrieve, userAgent)
				if results == None:
					print("\tNo results")
				else:
					out = open(outputFile , "a") #move this outside
					out.write("\n## " + dork + "\n")
					for title in results:
						if title:
							print(colored("\t"+title, 'white'))
							out.write(title)
							out.write("\n")
					out.close()
				update_session(currnetDorkIndex, outputFolder+"/dorker.session")
				currnetDorkIndex = currnetDorkIndex + 1
			except Exception as e:
				print(colored('Exception: ' + str(e), 'red', attrs=['bold']))

			sleep(randint(4,6))


def check_session(session_file):
	"""
	read session file and return the current dork index
	"""	
	print("Checking session at: "+session_file)
	dork_index = 0
	try:
		if os.path.exists(session_file) == True and os.path.isfile(session_file) == True:
			with open(session_file, 'r') as file_contents:
				for session in list(file_contents.readlines()):
					dork_index = session.rstrip('\n')
			print(colored("Previous session detected at: " + session_file, "yellow"))
			print(colored("Resuming from dork number: " + str(int(dork_index)+1) , "yellow"))
	except Exception as e:
		print(colored("\tUnable to read session "+str(e),"red"))
	
	return int(dork_index)


def update_session(dork_index, session_file):
	"""
	save the current dork index in session file
	"""
	print("\tUpdating session with index: " + str(dork_index))
	if dork_index > 1:
		try:
			out = open(session_file , "w")
			out.write(str(dork_index))
			out.close()
			print("\tSession updated")
		except Exception as e:
			print(colored("\tUnable to update session "+str(e),"red"))
		finally:
			pass
	

def main():
	print_header()
	#Defaults
	userAgent = "Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0"
	resultsToRetrieve = 20
	outputFolder = "output"
	payloadsFile = "payloads"
	additionalQuery = ""


	# Add in argument options
	parser = argparse.ArgumentParser(description='To use proxy (export HTTPS_PROXY=127.0.0.1:8080)')
	parser.add_argument('-d', '--domain', action='store', dest='domain', help='Target domain or comma seperated multiple domains (i.e. "a.com,b.com,c.com")', required=True)
	parser.add_argument('-p', '--payloads', action='store', dest='payloads', help='Payloads list of google dorks', default="payloads")
	parser.add_argument('-o', '--output', action='store', dest='outputFolder', help='Output folder', default="output")
	parser.add_argument('-n', '--no-of-results', action='store', dest='resultsToRetrieve', help='Number of results to retrieve per dork', type=int , default="20")
	parser.add_argument('-a', '--additional-query', action='store', dest='additionalQuery', help='Additional Query')
	results = parser.parse_args()

	# populate args
	if results.domain == None:
		print(colored("ERROR: missing the target domain.\n USAGE: docker.py -d target.com, use -h option for more.", 'red'))
		exit()
	else:
		domain = results.domain

	if results.resultsToRetrieve != None:
		resultsToRetrieve = results.resultsToRetrieve

	if results.payloads != None:
		if os.path.exists(results.payloads) == True and os.path.isfile(results.payloads) == True:
			payloadsFile = results.payloads
		else:
			print(colored("ERROR: couldn't find the a payload file at: "+ results.payloads , 'red'))
			exit()
	elif os.path.exists(payloadsFile) == False or os.path.isfile(payloadsFile) == False:
		print(colored("ERROR: couldn't find the default payload file at " + payloadsFile + ", use -p to specify a payloads file.", 'red'))
		exit()

	if results.outputFolder != None:
		if os.path.exists(results.outputFolder) == True:
			outputFolder = results.outputFolder
		else:
			print(colored("Creating output directory " + results.outputFolder , 'yellow'))
			os.makedirs(results.outputFolder)
			outputFolder = results.outputFolder
	elif os.path.exists(outputFolder) == False:
		os.makedirs(outputFolder)

	if results.additionalQuery != None:
		additionalQuery = results.additionalQuery

	


	
	
	dorkit (payloadsFile, domain, outputFolder, resultsToRetrieve, userAgent, additionalQuery)
	print(colored("Done.","green"))

if __name__ == '__main__':
    exit(main())