import time
import eventSelector as es
import subprocess
import os

def getHighlightEvents(filename, relImportances, mandatory=tuple(['goal']), eventSecs=10, highlightSecs=180):
	selected, remaining = es.getAllEvents(filename, mandatory)
	eventProbs = es.getEventProbs(selected, remaining, relImportances, eventSecs, highlightSecs)

	selected.extend(es.selectEvents(remaining, eventProbs))
	return selected

def createHighlights(videoFiles, offsets, selected, beforeAfterRatios, eventSecs=10):
	isSecondHalf = False

	file1 = videoFiles[0]
	file2 = videoFiles[1]

	file = file1
	offset = offsets[0]
	start = time.time()
	count = 0
	for event in sorted(selected, key=lambda x: x.secs):
		if count % 3 == 0:
			print("{}: Time, num events: {}, {}".format(count, event.secs, len(selected)))
		if event.secs > 45*60:
			if not isSecondHalf:
				isSecondHalf = True
				file = file2
				offset = offsets[1]
			event.secs = event.secs - 45*60
		event.secs = event.secs + offset

		beforeAfterRatio = beforeAfterRatios[event.type]
		before = (beforeAfterRatio/(1.0 + beforeAfterRatio))*eventSecs

		getClipInInterval(file, "./intermediate/" + str(count) + ".mp4", event.secs - before, eventSecs)
		count = count + 1

	print("Time taken: {}".format(time.time() - start))

def mergeClips(concatFile, outFile):
	cmd = "ffmpeg -f concat -safe 0 -i " + concatFile + " -c copy " + outFile
	subprocess.call(cmd, shell=True)

def createConcatFile(inputDir, outFile):
	numFiles = len(os.listdir(inputDir))
	text = ""

	for i in range(0, numFiles):
		text = text + "file '" + inputDir + "/" + str(i) + ".mp4'\n"
	with open(outFile, 'w') as f:
		f.write(text)

def getClipInInterval(inputFile, outFile, start, duration):
	cmd = "ffmpeg -ss " + str(start) + " -t " + str(duration) + " -i \"" + inputFile + "\" \"" + outFile + "\""
	subprocess.call(cmd, shell=True)

if __name__ == "__main__":
	eventSecs = 17
	highlightSecs = 300
	relImportances = {'Foul': 0.25, 'off_target': 0.33, 'yellow': 0.5, 'save': 1}
	beforeAfterRatios = {'Foul': 1.0, 'off_target': 1.0, 'yellow': 5 / 12.0, 'save': 1.0, 'goal': 2 / 3.0}

	selected = getHighlightEvents('match.xml', relImportances, mandatory=['goal'], eventSecs=eventSecs,
								  highlightSecs=highlightSecs)
	createHighlights(["BAR-JUV 1st half ENG.mp4", "BAR-JUV 2nd half ENG.mp4"], [226, 27], selected,
					 beforeAfterRatios, eventSecs=eventSecs)
	createConcatFile("./intermediate", "concat.txt")
	mergeClips("concat.txt", "highlights.mp4")

	# offsets = [3*60 + 46 = 226, 27]