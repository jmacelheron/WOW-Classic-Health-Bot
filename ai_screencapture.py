import mss
import pyautogui
import cv2 as cv
import numpy as np
import time

w, h = pyautogui.size()
print("Screen Res:" + "w:" + str(w) + " h:" + str(h))

# image capture
img = None
monitor = {"top": 0, "left": 0, "width": w, "height": h}

t0 = time.time()
n_frames = 1

with mss.mss() as sct:
    while True:
        img = sct.grab(monitor = monitor)
        #img is now stored in mem
        # this function captures in BGR not RGB, convenient because CV2 also works in BGR
        img = np.array(img)

        # reduce it by a scalar of 0.5, ignore second variable input so put in 0,0
        small = cv.resize(img, (0,0), fx = 0.5, fy = 0.5)

        cv.imshow("Computer Vision", small)

        # introduce a delay to see the screen
        # wait 1 ms
        key = cv.waitKey(1)
        if key == ord('q'):
            break
        elapsed_time = time.time() - t0
        fps = (n_frames / elapsed_time)
        print('FPS ' + str(fps))
        n_frames += 1
cv.destroyAllWindows()