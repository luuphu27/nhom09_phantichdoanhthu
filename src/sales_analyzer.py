import logging

class SalesAnalyzer:
    def __init__(self, df=None):
        self.df = df

    def analyze_data(self):
        try:
            if self.df is None:
                raise ValueError("DataFrame đang trống hoặc chưa được nạp dữ liệu.")
            
            logging.info("Đang thực hiện phân tích dữ liệu...")
            
        except ValueError as e:
            logging.warning(f"Cảnh báo nghiệp vụ: {e}")
        except Exception as e:
            logging.error(f"Lỗi trong quá trình phân tích: {e}")