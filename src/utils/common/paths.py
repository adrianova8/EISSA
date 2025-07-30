import json
from typing import Dict
from pathlib import Path


class ProjectPaths:
    def __init__(self):
        # Paths base
        self.root_dir = Path(__file__).parents[2].absolute()
        self.app_dir = self.root_dir / 'app'
        self.data_dir = self.root_dir / 'data'
        self.config_dir = self.root_dir / 'config'
        self.logs_dir = self.root_dir / 'logs'
        self.images_dir = self.root_dir / 'images'
        self.database_dir = self.data_dir / 'db'

        
        # Crear directorios necesarios
        self._create_directories()
        
        # Paths específicos
        self.config_file = self.config_dir / 'paths_config.json'
        self.database_file = self.database_dir / 'database.db'
        self.log_file = self.logs_dir / 'app.log'

    def _create_directories(self) -> None:
        """Crear estructura de directorios del proyecto"""
        directories = [
            self.data_dir,
            self.config_dir,
            self.logs_dir,
            self.images_dir,
            self.database_dir
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def get_all_paths(self) -> Dict[str, str]:
        """Obtener todos los paths como diccionario"""
        return {
            'root_dir': str(self.root_dir),
            'data_dir': str(self.data_dir),
            'config_dir': str(self.config_dir),
            'logs_dir': str(self.logs_dir),
            'images_dir': str(self.images_dir),
            'database_dir': str(self.database_dir),
            'config_file': str(self.config_file),
            'database_file': str(self.database_file),
            'log_file': str(self.log_file)
        }

    def save_paths_config(self) -> None:
        """Guardar configuración de paths en JSON"""
        with open(self.config_file, 'w') as f:
            json.dump(self.get_all_paths(), f, indent=4)

    def load_paths_config(self) -> Dict[str, str]:
        """Cargar configuración de paths desde JSON"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}

if __name__ == "__main__":
    # Ejemplo de uso
    project_paths = ProjectPaths()
    
    # Guardar configuración
    project_paths.save_paths_config()
    
    # Cargar configuración
    paths_config = project_paths.load_paths_config()
    
    # Mostrar paths generados
    print("Paths del proyecto:")
    for key, path in paths_config.items():
        print(f"{key}: {path}")