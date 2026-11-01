import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataLoader:
    def __init__(self, file_path: str | Path):
        # Sử dụng pathlib để tạo đường dẫn tương đối linh hoạt
        self.file_path = Path(file_path)

    def load_data(self):
        try:
            if not self.file_path.exists():
                raise FileNotFoundError(f"Không tìm thấy file tại đường dẫn: {self.file_path}")
            
            logging.info(f"Đang tiến hành đọc file từ: {self.file_path}")
            # Sau này sẽ viết logic dùng pandas đọc file tại đây
            
        except FileNotFoundError as e:
            logging.error(f"Lỗi File: {e}")
        except Exception as e:
            logging.error(f"Đã xảy ra lỗi không mong muốn khi đọc dữ liệu: {e}")