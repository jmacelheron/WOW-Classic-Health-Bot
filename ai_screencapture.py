import mss
import pyautogui
import cv2 as cv
import numpy as np
import time
import multiprocessing

class ScreencaptureAgent:
    def __init__(self) -> None:
        self.img = None
        self.img_health = None
        self.capture_process = None
        self.fps = None
        self.img_health_HSV = None
        self.enable_cv_preview = True

        self.top_left = (473, 485)
        self.bottom_right = (682, 495)

        #self.w, self.h = pyautogui.size()
        self.w = 1306
        self.h = 1076
        print("Screen Res:" + "w:" + str(self.w) + " h:" + str(self.h))
        self.monitor = {"top": 0, "left": 0, "width": self.w, "height": self.h}

    def capture_screen(self):
        fps_report_time = time.time()
        fps_report_delay = 5
        n_frames = 1

        with mss.mss() as sct:
            while True:
                self.img = sct.grab(monitor = self.monitor)
                #img is now stored in mem
                # this function captures in BGR not RGB, convenient because CV2 also works in BGR
                self.img = np.array(self.img)
                self.img_health = self.img[
                    self.top_left[1]: self.bottom_right[1],
                    self.top_left[0]: self.bottom_right[0]
                ]

                self.img_health_HSV = cv.cvtColor(self.img_health, cv.COLOR_BGR2HSV)

                # reduce it by a scalar of 0.5, ignore second variable input so put in 0,0
                if(self.enable_cv_preview) :
                    small = cv.resize(self.img, (0,0), fx = 0.5, fy = 0.5)

                    if self.fps is None:
                        fps_text = ""
                    else:
                        fps_text = f'FPS:{self.fps:.2f}'
                        cv.putText(
                            small,
                            fps_text,
                            (25, 50),
                            cv.FONT_HERSHEY_COMPLEX,
                            1,
                            (174, 255, 99),
                            1,
                            cv.LINE_AA
                        )
                        cv.putText(
                            small,
                            "Health: " + str(hue_match_pct(self.img_health_HSV, 0, 15)),
                            (25, 100),
                            cv.FONT_HERSHEY_COMPLEX,
                            1,
                            (0, 0, 255),
                            1,
                            cv.LINE_AA
                        )
                    cv.imshow("Computer Vision", small)
                    cv.imshow("Health Bar", self.img_health)

                # introduce a delay to see the screen
                # wait 1 ms
                
                elapsed_time = time.time() - fps_report_time
                if(elapsed_time >= fps_report_delay):
                    self.fps = (n_frames / elapsed_time)
                    print('FPS ' + str(self.fps))
                    n_frames = 0
                    fps_report_time = time.time()
                n_frames += 1
                cv.waitKey(1)             

class bColors:
    PINK = '\033[95m'
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'

def print_menu():
    print(f'{bColors.CYAN}Command Menu{bColors.ENDC}')
    print(f'{bColors.GREEN}\tr - run{bColors.ENDC}\t\tStart screen capture')
    print(f'{bColors.RED}\ts - stop{bColors.ENDC}\tStop screen capture')
    print(f'\tq - quit\tQuit the program')

def convert_hue(hue):
        ratio = 361 /180
        return np.round(hue / ratio, 2)

def hue_match_pct(img , hue_low, hue_high):
    match_pixels = 0
    no_match_pixels = 0
    for pixel in img:
        for h, s, v in pixel:
            if convert_hue(hue_low) <= h <= convert_hue(hue_high):
                match_pixels += 1
            else:
                no_match_pixels += 1
    total_pixels = match_pixels + no_match_pixels
    return np.round(match_pixels / total_pixels, 2) * 100
#entry point
if __name__ == "__main__":
    screen_agent = ScreencaptureAgent()
    while True:
        print_menu()
        user_input = input().strip().lower()
        if user_input == 'quit' or user_input == 'q':
            if(screen_agent.capture_process is not None):
                screen_agent.capture_process.terminate()
            break
        elif user_input == 'run' or user_input == 'r':
            if screen_agent.capture_process is not None:
                print(f'{bColors.YELLOW}WARNING {bColors.ENDC} capture process already running')
                continue
            # create a process
            screen_agent.capture_process = multiprocessing.Process(
                # note do not use the () operator on capture_screen because you dont want the return value, you want the actual function
                target = screen_agent.capture_screen,
                args = (),
                name = "screen capture process"
            )
            screen_agent.capture_process.start()
        elif user_input == 'stop' or user_input == 's':
            if screen_agent.capture_process is None:
                print(f'{bColors.YELLOW}WARNING {bColors.ENDC} capture process not running')
                continue
            screen_agent.capture_process.terminate()
            screen_agent.capture_process = None
        else:
            print(f'{bColors.RED}ERROR:{bColors.ENDC} Invalid Selection')
print("Done")