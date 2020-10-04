#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import json


class synonames2solr(object):

	dictionary = {}

	def __init__(self):
	
		self.verbose = False
                
		self.filename = './aleph-elasticsearch/synonames.txt'

		self.solr = "http://localhost:8983/solr/opensemanticsearch"

		self.solr_managed_synonyms_resource = "skos"
		

	#
	# append synonyms by Solr REST API for managed resources
	#
	def synonyms2solr(self):
		
		url = self.solr + '/schema/analysis/synonyms/' + self.solr_managed_synonyms_resource
		headers = {'content-type' : 'application/json'}
		
		r = requests.post(url=url, data=json.dumps(self.dictionary), headers=headers)


	def import_synonames(self):

		synonamesfile = open(self.filename, encoding="utf-8")
		for line in synonamesfile:
			line = line.strip()
			if line:

				values = line.split(',')
				concept = values[0].strip()
				synonym = values[1].strip()

				if self.verbose:
					print("Appending synonym {} to concept {} and same in other direction".format(synonym, concept))

				# create dictionary entry for concept
				if not concept in self.dictionary:
					# add concept itself as synonym, so original concept will be found, too, not only rewritten to synonym(s)
					self.dictionary[concept] = [concept]

				# add synonyms to synonym array for concepts entry in dictionary
				if synonym not in self.dictionary[concept]:
					self.dictionary[concept].append(synonym)

				# do the same in other direction to get bidirectional synonyms
				if not synonym in self.dictionary:
					self.dictionary[synonym] = [synonym]
				if concept not in self.dictionary[synonym]:
					self.dictionary[synonym].append(concept)


		synonamesfile.close()

		self.synonyms2solr()


# start by command line
if __name__ == "__main__":

	from optparse import OptionParser

	parser = OptionParser("synonames2solr [options]")

	parser.add_option("-f", "--file", dest="filename", default='./aleph-elasticsearch/synonames.txt', help="Source file: Synonym config filename")

	parser.add_option("-s", "--solr", dest="solr", default='http://localhost:8983/solr/opensemanticsearch', help="Solr URL and core")

	parser.add_option("-g", "--graph", dest="graph", default='skos', help="Solr managed synonyms resource")

	(options, args) = parser.parse_args()

	converter = synonames2solr()

	converter.solr = options.solr
	converter.solr_managed_synonyms_resource = options.graph
	converter.filename = options.filename

	converter.import_synonames()
