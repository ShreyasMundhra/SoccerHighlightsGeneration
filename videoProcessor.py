import cv2
import eventSelector as es
import time

def getHighlightEvents(filename, relImportances, mandatory=tuple(['goal']), eventSecs=10, highlightSecs=180):
	selected, remaining = es.getAllEvents(filename, mandatory)
	eventProbs = es.getEventProbs(selected, remaining, relImportances, eventSecs, highlightSecs)

	selected.extend(es.selectEvents(remaining, eventProbs))
	return selected

def createHighlights(videoFiles, offsets, outFile, selected, eventSecs=10):
	isSecondHalf = False

	cap1 = cv2.VideoCapture(videoFiles[0])
	cap2 = cv2.VideoCapture(videoFiles[1])
	print(cap2.isOpened())

	fps = cap1.get(cv2.CAP_PROP_FPS)
	w = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
	h = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
	writer = cv2.VideoWriter(outFile, cv2.VideoWriter_fourcc(*'MP4V'), fps, (w, h), True)

	cap = cap1
	offset = offsets[0]
	start = time.time()
	for event in sorted(selected, key=lambda x: x.secs):
		print("Here: {}, {}".format(event.secs, len(selected)))
		# TODO: remove condition
		if event.secs > 45*60:
			if not isSecondHalf:
				isSecondHalf = True
				cap.release()
				cap = cap2
				offset = offsets[1]
			event.secs = event.secs - 45*60
		event.secs = event.secs + offset
		cap.set(cv2.CAP_PROP_POS_MSEC, event.secs*1000 - (eventSecs/2)*1000)
		while cap.get(cv2.CAP_PROP_POS_MSEC) <= event.secs*1000 + (eventSecs/2)*1000:
			success, frame = cap.read()
			writer.write(frame)
	print("Time taken: {}".format(time.time() - start))

if __name__ == "__main__":
	eventSecs = 17
	highlightSecs = 300
	relImportances = {'Foul': 0.25, 'off_target': 0.33, 'yellow': 0.5, 'save': 1}

	selected = getHighlightEvents('match.xml', relImportances, mandatory=['goal'], eventSecs=eventSecs, highlightSecs=highlightSecs)
	createHighlights(["BAR-JUV 1st half ENG.mp4", "BAR-JUV 2nd half ENG.mp4"], [226, 27], "highlights.mp4", selected, eventSecs=eventSecs)

	# offsets = [3*60 + 46 = 226, 27]