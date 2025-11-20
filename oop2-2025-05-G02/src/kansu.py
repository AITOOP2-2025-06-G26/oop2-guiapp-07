import cv2
import cv2
from ivent import Takeforbotton
import uuid
import os

# 保存フォルダ
SAVE_DIR = "photos"
os.makedirs(SAVE_DIR, exist_ok=True)

def start_capture(picture):
    """
   picture: 撮った画像をGUIに送る関数（担当Aが用意）
    """

    while True:
        Takeforbotton.ok_flag = False
        Takeforbotton.retry_flag = False

        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow("Capture", frame)

            # キャンセル（いいえ）
            if Takeforbotton.cancel_capture_flag:
                cap.release()
                cv2.destroyAllWindows()
                return

            # 撮影確定（担当Aが OK を押したとき）
            if Takeforbotton.ok_flag:
                img_name = f"{uuid.uuid4().hex}.png"
                save_path = os.path.join(SAVE_DIR, img_name)

                cv2.imwrite(save_path, frame)  # 写真保存

                # GUI に表示
                picture(save_path)

                cap.release()
                cv2.destroyAllWindows()
                return  # 完了

            # いいえ → 撮り直し
            if Takeforbotton.retry_flag:
                break  # whileを抜けて撮影し直し

            # qキーで終了（デバッグ用）
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return

        cap.release()
        cv2.destroyAllWindows()





