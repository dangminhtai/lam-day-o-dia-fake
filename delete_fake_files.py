import psutil
import os
import subprocess

def delete_fake_files():
    # Xóa tệp giả từ thư mục Temp
    partitions = psutil.disk_partitions()

    for partition in partitions:
        temp_dir = os.path.join(partition.mountpoint, "Temp")
        fake_file_path = os.path.join(temp_dir, "fake_file.txt")
        
        if os.path.exists(fake_file_path):
            try:
                os.remove(fake_file_path)
            except Exception:
                pass  # Bỏ qua lỗi

    # Mở lại File Explorer tại "This PC"
    subprocess.run('explorer shell:MyComputerFolder', shell=True)

# Gọi hàm để xóa tệp giả
delete_fake_files()
