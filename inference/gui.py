import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import threading
import time


class VideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Upload and Display")
        self.root.geometry("800x600")

        # Biến lưu video
        self.video_path = None
        self.cap = None
        self.playing = False

        # Tạo nút Upload
        self.upload_btn = tk.Button(root, text="Upload Video", command=self.upload_video)
        self.upload_btn.pack(pady=10)

        # Tạo canvas để hiển thị video
        self.canvas = tk.Canvas(root, width=640, height=480, bg="black")
        self.canvas.pack()

    def upload_video(self):
        # Mở hộp thoại chọn file video
        self.video_path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
        )
        if self.video_path:
            # Dừng video cũ nếu đang phát
            self.playing = False
            if self.cap:
                self.cap.release()

            # Mở video mới
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Không thể mở video. Vui lòng thử lại.")
                return

            self.playing = True
            # Chạy video trong luồng riêng để không làm treo GUI
            threading.Thread(target=self.play_video, daemon=True).start()

    def play_video(self):
        while self.playing and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # Chuyển đổi khung hình sang định dạng hiển thị trên Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))  # Điều chỉnh kích thước
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image)

            # Cập nhật canvas
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.image = photo  # Giữ tham chiếu để tránh bị thu hồi

            # Delay nhỏ để đồng bộ tốc độ khung hình
            time.sleep(1 / 30)  # 30 FPS

        # Khi video kết thúc
        self.playing = False
        if self.cap:
            self.cap.release()
        messagebox.showinfo("Info", "Video đã kết thúc.")

    def __del__(self):
        # Giải phóng tài nguyên khi đóng
        if self.cap:
            self.cap.release()


# Tạo và chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root)
    root.mainloop()