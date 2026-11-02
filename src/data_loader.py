import logging
from pathlib import Path
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DataLoader:
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.df = None

    def load_data(self):
        try:
            if not self.file_path.exists():
                raise FileNotFoundError(f"Không tìm thấy file tại đường dẫn: {self.file_path}")

            logging.info(f"Đang tiến hành đọc file từ: {self.file_path}")
            self.df = pd.read_csv(self.file_path)
            logging.info(f"Đọc dữ liệu thành công! Kích thước: {self.df.shape}")
            return self.df

        except FileNotFoundError as e:
            logging.error(f"Lỗi File: {e}")
            return None
        except Exception as e:
            logging.error(f"Đã xảy ra lỗi không mong muốn khi đọc dữ liệu: {e}")
            return None

    def clean_data(self):
        if self.df is None:
            logging.error("Chưa có dữ liệu để kiểm tra!")
            return

        print("\n--- NHẬT KÝ KIỂM TRA DỮ LIỆU THÔ (Thành) ---")
        print(f"Số dòng và số cột: {self.df.shape}")
        
        print("\nSố lượng giá trị thiếu (Null) ở mỗi cột:")
        print(self.df.isnull().sum())
        
        print("\nKiểu dữ liệu của các cột:")
        print(self.df.dtypes)
        print("-" * 45)