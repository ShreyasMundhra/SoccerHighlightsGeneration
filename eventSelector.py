import dataProcessor as dp
import random

class Event():
	def __init__(self, type, secs):
		self.type = type
		self.secs = secs

def getAllEvents(filename, mandatory=tuple(['goal'])):
	eventElements = dp.getAllEventElements(filename)

	selected = []
	remaining = []
	for element in eventElements:
		attrib = element.attrib
		# TODO: use (mins and secs) or minsec?
		event = Event(attrib['type'], int(attrib['minsec']))
		if attrib["type"] in mandatory:
			selected.append(event)
		else:
			remaining.append(event)

	# events = sorted(events, key=lambda x: x.secs)
	return selected, remaining

def findRemainingNumberOfSelectedEvents(selected, eventSecs=10, highlightSecs=180):
	return highlightSecs/eventSecs - len(selected)


def getEventCounts(events):
	counts = {}
	for event in events:
		if event.type not in counts:
			counts[event.type] = 1
		else:
			counts[event.type] = counts[event.type] + 1

	return counts


def getEventProbs(selected, remaining, relImportances, eventSecs=10, highlightSecs=180):
	numRemaining = findRemainingNumberOfSelectedEvents(selected, eventSecs, highlightSecs)
	eventCounts = getEventCounts(remaining)

	denominator = 0
	for event in eventCounts.keys():
		denominator = denominator + eventCounts[event]*relImportances[event]

	probs = {}
	for event in relImportances:
		probs[event] = relImportances[event]*numRemaining/float(denominator)
	return probs

def selectEvents(remaining, eventProbs):
	selected = []
	for event in remaining:
		if random.random() <= eventProbs[event.type]:
			selected.append(event)

	return selected

if __name__ == "__main__":
	selected, remaining = getAllEvents('match.xml', ['goal'])

	# TODO: Store all event types somewhere (list?) instead of hardcoding
	# TODO: Try changing relImportances
	relImportances = {'Foul': 0.25, 'off_target': 0.33, 'yellow': 0.5, 'save': 1}
	eventProbs = getEventProbs(selected, remaining, relImportances)

	# TODO: Select events to be shown in highlights based on eventProbs
	# TODO: Substitutions near beginning or end of game should be selected
	# TODO: No two consecutive events should be of the same type

	print(eventProbs)

	selected.extend(selectEvents(remaining, eventProbs))
	for event in sorted(selected, key=lambda x: x.secs):
		print(event.type, event.secs)

	# TODO: Run multiple times and write about results in the report