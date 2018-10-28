import cv2, time, pandas
from datetime import datetime


video = cv2.VideoCapture(0)

first_frame = None
status_list = [None, None]
status_times = []
times_df = pandas.DataFrame(columns = ["Start", "End"])

while True:
    check, frame = video.read()
    status = 0 #Indicator for whether or not object is in frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0) #smooths image to remove noise and increase accuracy

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame, gray)

    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (_,cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #if contours greater than specified parameter occurs, change status
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)

    status_list.append(status)

    #Only keep relevant status values, prevents running out of memory
    status_list = status_list[-2:]

    #Check for a change in status in the status list
    if status_list[-1] == 1 and status_list[-2] == 0:
        status_times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        status_times.append(datetime.now())

    #Display different frames as preferred for situational use
    #cv2.imshow("Gray Frame", gray)
    #cv2.imshow("Delta Frame", delta_frame)
    #cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Colour Frame", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if status == 1:
            status_times.append(datetime.now())
        break

for i in range(0, len(status_times), 2):
    times_df = times_df.append({"Start" : status_times[i], "End" : status_times[i + 1]}, ignore_index=True)

times_df.to_csv("status.csv")

video.release()
