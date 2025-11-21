import numpy as np
import cv2
import os
from my_module.K21999.lecture05_camera_image_capture import MyVideoCapture

def lecture05_01():

    # カメラキャプチャ実行
    app = MyVideoCapture()
    app.run()

    # 画像をローカル変数に保存
    google_img_path = 'images/google.png'
    capture_img_path = 'images/capture.png'

    if not os.path.exists(google_img_path):
        print(f"[ERROR] File not found: {google_img_path}")
        return

    google_img: cv2.Mat = cv2.imread(google_img_path)
    capture_img = app.get_img()

    if capture_img is None:
        if not os.path.exists(capture_img_path):
            print(f"[ERROR] File not found: {capture_img_path}")
            return
        capture_img = cv2.imread(capture_img_path)

    if google_img is None or capture_img is None:
        print("[ERROR] Failed to load one or more images.")
        return

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
    output_dir = 'output_images'
    os.makedirs(output_dir, exist_ok=True)
    cv2.imwrite(os.path.join(output_dir, 'lecture05_01_k24110.png'), google_img)