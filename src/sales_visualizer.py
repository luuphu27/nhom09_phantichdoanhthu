import logging

class SalesVisualizer:
    def __init__(self, df=None):
        self.df = df

    def plot_charts(self):
        try:
            if self.df is None:
                raise ValueError("Không có dữ liệu để vẽ biểu đồ.")
            
            logging.info("Đang khởi tạo các biểu đồ trực quan...")
            
        except ValueError as e:
            logging.warning(f"Cảnh báo trực quan: {e}")
        except Exception as e:
            logging.error(f"Lỗi khi vẽ biểu đồ: {e}")