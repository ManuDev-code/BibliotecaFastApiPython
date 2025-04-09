import os
import json
from typing import List, Dict, Any, Type, TypeVar, Generic

T = TypeVar('T')


class DataHandler(Generic[T]):
    def __init__(self, file_path: str, model_class: Type[T]):
        self.file_path = file_path
        self.model_class = model_class
        self.ensure_data_dir()

    def ensure_data_dir(self):
        """Asegura que el directorio de datos exista"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def load_data(self) -> List[T]:
        """Carga los datos desde el archivo JSON"""
        if not os.path.exists(self.file_path):
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [self.model_class.from_dict(item) for item in data]
        except Exception as e:
            print(f"Error al cargar datos desde {self.file_path}: {e}")
            return []

    def save_data(self, items: List[T]) -> bool:
        """Guarda los datos en el archivo JSON"""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([item.to_dict() for item in items], f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar datos en {self.file_path}: {e}")
            return False

    def save_counter(self, counter_name: str, value: int) -> bool:
        """Guarda el valor del contador en el archivo de contadores"""
        counter_file = "data/contadores.json"
        counters = {}

        if os.path.exists(counter_file):
            try:
                with open(counter_file, "r", encoding="utf-8") as f:
                    counters = json.load(f)
            except:
                pass

        counters[counter_name] = value

        try:
            with open(counter_file, "w", encoding="utf-8") as f:
                json.dump(counters, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar contador {counter_name}: {e}")
            return False

    def load_counter(self, counter_name: str, default: int = 0) -> int:
        """Carga el valor del contador desde el archivo de contadores"""
        counter_file = "data/contadores.json"

        if not os.path.exists(counter_file):
            return default

        try:
            with open(counter_file, "r", encoding="utf-8") as f:
                counters = json.load(f)
                return counters.get(counter_name, default)
        except Exception as e:
            print(f"Error al cargar contador {counter_name}: {e}")
            return default