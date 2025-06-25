import tkinter as tk
from typing import Dict, Optional

class FrameManager:
    """
    Singleton class to manage all frames in the application.
    Allows frame reuse across different gadgets.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._frames: Dict[str, tk.Frame] = {}
        return cls._instance
    
    def register_frame(self, name: str, frame: tk.Frame) -> None:
        """Register a frame for later reuse"""
        self._frames[name] = frame
    
    def get_frame(self, name: str) -> Optional[tk.Frame]:
        """Retrieve a previously registered frame"""
        return self._frames.get(name)
    
    def has_frame(self, name: str) -> bool:
        """Check if a frame exists"""
        return name in self._frames
