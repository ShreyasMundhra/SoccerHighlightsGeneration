import cv2
import eventSelector as es
import time

def getHighlightEvents(filename, relImportances, mandatory=tuple(['goal']), eventSecs=10, highlightSecs=180):
	selected, remaining = es.getAllEvents(filename, mandatory)
	eventProbs = es.getEventProbs(selected, remaining, relImportances, eventSecs, highlightSecs)

	selected.extend(es.selectEvents(remaining, eventProbs))
	return selected

def createHighlights(videoFiles, outFile, selected, eventSecs=10):
	isSecondHalf = False

	cap1 = cv2.VideoCapture(videoFiles[0])
	cap2 = cv2.VideoCapture(videoFiles[1])
	print(cap2.isOpened())

	fps = cap1.get(cv2.CAP_PROP_FPS)
	w = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
	h = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
	writer = cv2.VideoWriter(outFile, cv2.VideoWriter_fourcc(*'MP4V'), fps, (w, h), True)

	count = 1
	cap = cap1

	start = time.time()
	for event in sorted(selected, key=lambda x: x.secs):
		print("Here: {}, {}".format(event.secs, len(selected)))
		# writer = cv2.VideoWriter(str(count) + ".mp4", cv2.VideoWriter_fourcc(*'MP4V'), fps, (w, h), True)
		# TODO: remove condition
		if event.secs > 45*60:
			if not isSecondHalf:
				isSecondHalf = True
				cap.release()
				cap = cap2
			event.secs = event.secs - 45*60
			# print("Here2: {}, {}, {}".format(cap == cap2, event.secs, cap2))
		cap.set(cv2.CAP_PROP_POS_MSEC, event.secs*1000 - eventSecs*1000)
		while cap.get(cv2.CAP_PROP_POS_MSEC) <= event.secs*1000:
			success, frame = cap.read()
			writer.write(frame)

		count = count + 1

	print("Time taken: {}")

	# return writer

if __name__ == "__main__":
	relImportances = {'Foul': 0.25, 'off_target': 0.33, 'yellow': 0.5, 'save': 1}
	selected = getHighlightEvents('match.xml', relImportances, mandatory=['goal'])
	createHighlights(["BAR-JUV 1st half ENG.mp4", "BAR-JUV 2nd half ENG.mp4"], "highlights.mp4", selected)

	# cap = cv2.VideoCapture("./ROM V LIV 1H EN 1080.mp4")
	# print(cap.isOpened())
	# # numFrames = cap.get(7)
	#
	# fps = cap.get(cv2.CAP_PROP_FPS)
	# w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	# h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	# # codec = cap.get(cv2.CAP_PROP_FOURCC)
	# writer = cv2.VideoWriter('clip.mp4', cv2.VideoWriter_fourcc(*'MP4V'), fps, (w, h), True)
	#
	# cap.set(cv2.CAP_PROP_POS_MSEC, 30000)
	#
	# while cap.get(cv2.CAP_PROP_POS_MSEC) <= 40000:
	# 	# print(cap.get(cv2.CAP_PROP_POS_MSEC))
	# 	success, image = cap.read()
	# 	writer.write(image)
	# 	# cv2.imshow('image', image)
	# 	# cv2.waitKey(0)

	# 28