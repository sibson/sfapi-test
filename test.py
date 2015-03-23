from datetime import datetime
import os

from sforce.partner import SforcePartnerClient
client = SforcePartnerClient('./partnerwsdl.xml')
client.login("scottp+test@heroku.com", os.environ['PASSWORD'], os.environ['TOKEN'])
queryOptions = client.generateHeader('QueryOptions')
queryOptions.batchSize = 2000
client.setQueryOptions(queryOptions)

class Timer():
	def __init__(self, name):
		self.name = name

	def __enter__(self):
		self.start = datetime.now()

	def __exit__(self, *args):
		delta = datetime.now() - self.start
		print "{} - {} secs".format(self.name, delta)


total = 0

with Timer("totalRun"):
	with Timer("query"):	
		r = client.query("Select Id, Name, Birthdate__c, FirstName__c, LastName__c from Contact1m__c")
		total += len(r.records)

	while not r.done:
		with Timer("queryMore"):
			r = client.queryMore(r.queryLocator)
			total += len(r.records)
			print total

	print "Fetched {} total records".format(total)


# Localhost test:
# Fetched 1000001 total records
# totalRun - 0:24:38.476870 (24 mins)
