# src/core/data_loader.py
import json
import os

class DataLoader:
    def load_data(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
