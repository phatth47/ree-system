import os
import cv2
import threading
from deepface import DeepFace
import uuid
from datetime import datetime

# Set up camera connection details
ip_address = '192.168.1.3'  # Replace with the IP address of your camera
port = '554'  # Replace with the port number for your camera
username = 'admin123'  # Replace with the username for your camera
password = 'admin123'  # Replace with the password for your camera

# Construct the RTSP stream URLs using variables
url_640x480 = f"rtsp://{username}:{password}@{ip_address}:{port}/stream2"
url_1080p = f"rtsp://{username}:{password}@{ip_address}:{port}/stream1"

# Set up RTSP stream URL
rtsp_url = url_640x480

cap = cv2.VideoCapture(rtsp_url)  # change source to tapo camera rtsp

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# reference_img = cv2.imread('C://Users//Admin//Desktop//IMG_1836.jpg')

face_match = False
capture_image = True  # Biến cờ để chỉ cho phép chụp hình khuôn mặt 1 lần
avatar_images_dir = "D://develop//ree_system//avatar"
avatar_images = [os.path.join(avatar_images_dir, img) for img in os.listdir(avatar_images_dir)]


def check_face():
    global face_match, capture_image
    ret, frame = cap.read()

    any_match = False

    if ret:
        try:
            # Kiểm tra từng ảnh trong danh sách "avatar_images"
            for img_path in avatar_images:
                reference_img = cv2.imread(img_path)
                # Log the reference image
                print(f"Reference image: {img_path}")
                for _ in range(5):
                    if DeepFace.verify(frame, reference_img.copy(), model_name='Facenet512', detector_backend='opencv',
                                       distance_metric='euclidean_l2', enforce_detection=False)['verified']:
                        # Log the matched face
                        print(f"Matched face: Matched with {img_path}")
                        face_match = True
                        any_match = True
                        capture_image = False  # Khớp khuôn mặt, không cần chụp lại
                        break

                if face_match:
                    break
                else:
                    print(f"Matched face: No match with {img_path}")

            # Kiểm tra nếu không có ảnh nào khớp khuôn mặt, thì mới tạo mới hình ảnh
            if not any_match and capture_image:
                # Đổi tên ảnh thành tên ngẫu nhiên và lưu vào thư mục "avatar"
                new_filename = generate_random_filename()
                # Log the new filename
                print(f"New filename: {new_filename}")
                new_filepath = os.path.join(avatar_images_dir, new_filename)
                # Log the new filepath
                print(f"New filepath: {new_filepath}")
                cv2.imwrite(new_filepath, frame)
                # Logs the new face
                print(f"New face detected and saved: {new_filename}")
                capture_image = False  # Đánh dấu đã chụp hình để không chụp lại

        except ValueError:
            face_match = False
        except Exception as e:
            print(e)
            face_match = False

    return face_match, capture_image


# counter = 0
# a = 0
# while a == 0:
#     a = 1
#     ret, frame = cap.read()
#
#     if ret:
#         if counter % 10 == 0:
#             try:
#                 threading.Thread(target=check_face, args=(frame.copy(),)).start()
#                 # print('working')
#             except ValueError:
#                 pass
#         # print(counter)
#         counter += 1
#
#         if face_match:
#             cv2.putText(frame, 'MATCH!', (00, 350), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3, cv2.LINE_AA, False)
#         else:
#             cv2.putText(frame, 'NO MATCH!', (00, 350), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3, cv2.LINE_AA, False)
#
#         cv2.imshow('video', frame)
#
#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break
#
# cv2.destroyAllWindows()


def generate_random_filename():
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    random_string = str(uuid.uuid4().hex)[:6]
    return f"{now}_{random_string}.jpg"
