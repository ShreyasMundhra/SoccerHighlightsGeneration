import xml.etree.ElementTree as ET

def getFilters(root):
	return root.findall("./data_panel/filters")[0]

def getGoals(filters):
	return filters.findall("./goals_attempts//event[@type='goal']")

def getFouls(filters):
	return filters.findall("./fouls//event[@type='Foul']")

def getYellowCards(filters):
	return filters.findall("./cards//event[card='yellow']")

def getSaves(filters):
	return filters.findall("./goal_keeping//event[@type='save']")

def getShotsOffTarget(filters):
	return filters.findall("./goals_attempts//event[@type='off_target']")

if __name__ == "__main__":
	tree = ET.parse('match.xml')
	root = tree.getroot()
	filters = getFilters(root)
	# goals = getGoals(filters)
	# for goal in goals:
	# 	print(goal.attrib)

	# fouls = getFouls(filters)
	# for foul in fouls:
	# 	print(foul.attrib)

	# yellows = getYellowCards(filters)
	# for yellow in yellows:
	# 	print(yellow.attrib)

	# saves = getSaves(filters)
	# for save in saves:
	# 	print(save.attrib)

	offshots = getShotsOffTarget(filters)
	for offshot in offshots:
		print(offshot.attrib)