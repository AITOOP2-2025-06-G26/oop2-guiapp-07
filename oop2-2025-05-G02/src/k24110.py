import numpy as np
import cv2
from my_module.K21999.lecture05_camera_image_capture import MyVideoCapture

def lecture05_01():

    # カメラキャプチャ実行
    app = MyVideoCapture()
    app.run()

    # 画像をローカル変数に保存
    google_img : cv2.Mat = cv2.imread('images/google.png')
    capture_img = app.get_img()
    if capture_img is None:
        capture_img = cv2.imread('images/capture.png')
    
    g_hight, g_width, g_channel = google_img.shape
    c_hight, c_width, c_channel = capture_img.shape
    print(google_img.shape)
    print(capture_img.shape)

    for x in range(g_width):
        for y in range(g_hight):
            b, g, r = google_img[y, x]
            # もし白色(255,255,255)だったら置き換える
            if (b, g, r) == (255, 255, 255):
                b2, g2, r2 = capture_img[y % c_hight, x % c_width]
                google_img[y, x] = (b2, g2, r2)


    # 書き込み処理
    cv2.imwrite('output_images/lecture05_01_k24110.png', google_img)