import dataProcessor as dp
import xml.etree.ElementTree as ET

class Event():
	def __init__(self, type, secs):
		self.type = type
		self.secs = secs
		if type in ['goal']:
			self.isIncluded = True
		else:
			self.isIncluded = False

def getAllEvents(filename):
	eventElements = dp.getAllEventElements('match.xml')

	events = []
	for element in eventElements:
		attrib = element.attrib
		# TODO: use (mins and secs) or minsec?
		events.append(Event(attrib['type'], int(attrib['minsec'])))

	events = sorted(events, key=lambda x: x.secs)
	return events

if __name__ == "__main__":
	events = getAllEvents('match.xml')
	print(len(events))