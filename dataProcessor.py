import xml.etree.ElementTree as ET

def getFilters(root):
	return root.findall("./data_panel/filters")[0]

def getGoals(filters):
	return filters.findall("./goals_attempts//event[@type='goal']")

def getFouls(filters):
	return filters.findall("./fouls//event[@type='Foul']")

def getYellowCards(filters):
	yellows = filters.findall("./cards//event[card='yellow']")
	for yellow in yellows:
		# print(type(yellow))
		yellow.set('type', 'yellow')
	return yellows

def getSaves(filters):
	return filters.findall("./goal_keeping//event[@type='save']")

def getShotsOffTarget(filters):
	return filters.findall("./goals_attempts//event[@type='off_target']")

def getAllEventElements(filename):
	tree = ET.parse('match.xml')
	root = tree.getroot()
	filters = getFilters(root)

	goals = getGoals(filters)
	fouls = getFouls(filters)
	yellows = getYellowCards(filters)
	saves = getSaves(filters)
	offshots = getShotsOffTarget(filters)

	eventElements = []
	eventElements.extend(goals)
	eventElements.extend(fouls)
	eventElements.extend(yellows)
	eventElements.extend(saves)
	eventElements.extend(offshots)
	return eventElements

if __name__ == "__main__":
	eventElements = getAllEventElements('match.xml')
	for element in eventElements:
		print(element.attrib)