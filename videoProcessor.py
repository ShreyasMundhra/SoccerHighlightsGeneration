import cv2

if __name__ == "__main__":
	cap = cv2.VideoCapture("./ROM V LIV 1H EN 1080.mp4")
	print(cap.isOpened())
	# numFrames = cap.get(7)
	cap.set(cv2.CAP_PROP_POS_MSEC, 30000)

	fps = cap.get(cv2.CAP_PROP_FPS)
	w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	# codec = cap.get(cv2.CAP_PROP_FOURCC)
	writer = cv2.VideoWriter('clip.mp4', cv2.VideoWriter_fourcc(*'MP4V'), fps, (w, h), True)

	while cap.get(cv2.CAP_PROP_POS_MSEC) <= 40000:
		# print(cap.get(cv2.CAP_PROP_POS_MSEC))
		success, image = cap.read()
		writer.write(image)
		# cv2.imshow('image', image)
		# cv2.waitKey(0)