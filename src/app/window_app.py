
import tkinter as tk
from typing import Optional, Tuple

from src.utils.common.paths import ProjectPaths
from src.utils.common.names import (BROWN_COLOR, BLACK_COLOR, BEIGE_COLOR)

paths = ProjectPaths()

class AppWindow:
    def __init__(self, app: tk.Tk):
        """
        Initialize AppWindow with a Tkinter root window.

        Args:
            app (tk.Tk): The root Tkinter window instance.
        """
        self.app = app

    def window_dimensions(
        self,
        width_ratio: float = 0.8,
        height_ratio: float = 0.8,
        center: bool = True
    ) -> Optional[Tuple[int, int, int, int]]:
        """
        Automatically set window size and position based on current screen.

        Args:
            width_ratio (float): Fraction of screen width for window (e.g., 0.8 = 80% width).
            height_ratio (float): Fraction of screen height for window.
            center (bool): Whether to center the window on screen.

        Returns:
            Optional[Tuple[int, int, int, int]]: (width, height, x, y) or None if error occurs.
        """
        try:
            # Get screen dimensions
            screen_width = self.app.winfo_screenwidth()
            screen_height = self.app.winfo_screenheight()

            # Validate ratios
            if not (0 < width_ratio <= 1):
                raise ValueError("width_ratio must be between 0 and 1")
            if not (0 < height_ratio <= 1):
                raise ValueError("height_ratio must be between 0 and 1")

            # Calculate dimensions
            window_width = int(screen_width * width_ratio)
            window_height = int(screen_height * height_ratio)

            # Ensure minimum size
            window_width = max(200, window_width)
            window_height = max(200, window_height)

            # Calculate position
            if center:
                position_x = (screen_width - window_width) // 2
                position_y = (screen_height - window_height) // 2
            else:
                position_x = 0
                position_y = 0

            # Set geometry
            geometry_data = f"{window_width}x{window_height}+{position_x}+{position_y}"
            self.app.geometry(geometry_data)

            return window_width, window_height, position_x, position_y

        except tk.TclError as e:
            print(f"Error setting window geometry: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None


    def window_title(self, title: str) -> Optional[bool]:
        """
        Set the window title with error handling.

        Args:
            title (str): The title text to be displayed in the window's title bar.

        Returns:
            Optional[bool]: True if title was set successfully, None if an error occurred.

        Raises:
            tk.TclError: If the title cannot be set.
            TypeError: If title is not a string.
        """
        try:
            if not isinstance(title, str):
                raise TypeError("Title must be a string")
                
            self.app.title(title)
            return True
            
        except tk.TclError as e:
            print(f"Error setting window title: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None


    def window_bg_color(self, color="lightblue"):
        """Configurar color de fondo de la ventana"""
        self.app.configure(bg=color)


    def create_frame(
        self, 
        parent: Optional[tk.Widget] = None, 
        bg: str = "lightblue",
        side: str = None,
        fill: str = None,
        expand: bool = False,
        padx: int = 0,
        pady: int = 0,
        **kwargs
    ) -> tk.Frame:
        """
        Create a frame with specified configuration.
        
        Args:
            parent: Parent widget (defaults to self.app if None)
            bg: Background color
            side: Pack side option
            fill: Pack fill option
            expand: Pack expand option
            padx: X padding
            pady: Y padding
            **kwargs: Additional frame configuration options
            
        Returns:
            tk.Frame: Created frame
        """
        parent = parent or self.app
        frame = tk.Frame(parent, bg=bg, **kwargs)
        
        pack_options = {'side': side, 'fill': fill, 'expand': expand, 
                       'padx': padx, 'pady': pady}
        # Eliminar opciones None
        pack_options = {k: v for k, v in pack_options.items() if v is not None}
        
        frame.pack(**pack_options)
        return frame

    def create_label(
        self,
        parent: tk.Widget,
        text: str = "",
        font: tuple = None,
        bg: str = "lightblue",
        fg: str = "black",
        image: tk.PhotoImage = None,
        side: str = None,
        **kwargs
    ) -> tk.Label:
        """
        Create a label with specified configuration.
        
        Args:
            parent: Parent widget
            text: Label text
            font: Text font tuple (family, size, style)
            bg: Background color
            fg: Foreground color
            image: Optional image
            side: Pack side option
            **kwargs: Additional label configuration options
            
        Returns:
            tk.Label: Created label
        """
        label = tk.Label(
            parent,
            text=text,
            font=font,
            bg=bg,
            fg=fg,
            image=image,
            **kwargs
        )
        
        pack_options = {'side': side}
        pack_options = {k: v for k, v in pack_options.items() if v is not None}
        
        label.pack(**pack_options)
        if image:
            label.image = image  # Keep reference
        return label


    def create_entry(
        self,
        parent: tk.Widget,
        textvariable: tk.StringVar = None,
        font: tuple = None,
        bg: str = "white",
        fg: str = "black",
        width: int = 20,
        side: str = None,
        **kwargs
    ) -> tk.Entry:
        """
        Create an entry widget with specified configuration.
        
        Args:
            parent: Parent widget
            textvariable: StringVar for entry text
            font: Text font tuple (family, size, style)
            bg: Background color
            fg: Foreground color
            width: Entry width
            side: Pack side option
            **kwargs: Additional entry configuration options
            
        Returns:
            tk.Entry: Created entry widget
        """
        entry = tk.Entry(
            parent,
            textvariable=textvariable,
            font=font,
            bg=bg,
            fg=fg,
            width=width,
            **kwargs
        )
        
        pack_options = {'side': side}
        pack_options = {k: v for k, v in pack_options.items() if v is not None}
        
        entry.pack(**pack_options)
        return entry
    
    def create_button(
        self,
        parent: tk.Widget,
        text: str = "",
        command: Optional[callable] = None,
        font: tuple = None,
        bg: str = BROWN_COLOR,
        fg: str = BLACK_COLOR,
        activebackground: str = BROWN_COLOR,
        activeforeground: str = BEIGE_COLOR,
        highlightbackground: str = BEIGE_COLOR,
        highlightcolor: str = BEIGE_COLOR,
        side: str = None,
        **kwargs
    ) -> tk.Button:
        """
        Create a button with specified configuration.
        
        Args:
            parent: Parent widget
            text: Button text
            command: Function to call when button is clicked
            font: Text font tuple (family, size, style)
            bg: Background color
            fg: Foreground color
            side: Pack side option
            **kwargs: Additional button configuration options
            
        Returns:
            tk.Button: Created button widget
        """
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=font,
            bg=bg,
            fg=fg,
            activebackground = BROWN_COLOR,
            activeforeground = BEIGE_COLOR,
            highlightbackground = BEIGE_COLOR,
            highlightcolor = BEIGE_COLOR,
            **kwargs
        )
        
        pack_options = {'side': side}
        pack_options = {k: v for k, v in pack_options.items() if v is not None}
        
        button.pack(**pack_options)
        return button

    def create_string_var(self, initial_value: str = "") -> tk.StringVar:
        """
        Create a StringVar with an optional initial value.
        
        Args:
            initial_value: Initial value for the StringVar
            
        Returns:
            tk.StringVar: Created StringVar instance
        """
        return tk.StringVar(value=initial_value)
    
    def create_radio_button(
        self,
        parent: tk.Widget,
        text: str = "",
        variable: tk.StringVar = None,
        value: str = "",
        command: Optional[callable] = None,
        font: tuple = None,
        bg: str = "lightblue",
        fg: str = "black",
        side: str = None,
        **kwargs
    ) -> tk.Radiobutton:
        """
        Create a radio button with specified configuration.
        
        Args:
            parent: Parent widget
            text: Radio button text
            variable: StringVar to associate with the radio button
            value: Value for the radio button
            command: Function to call when radio button is selected
            font: Text font tuple (family, size, style)
            bg: Background color
            fg: Foreground color
            side: Pack side option
            **kwargs: Additional radio button configuration options
            
        Returns:
            tk.Radiobutton: Created radio button widget
        """
        radio_button = tk.Radiobutton(
            parent,
            text=text,
            variable=variable,
            value=value,
            command=command,
            font=font,
            bg=bg,
            fg=fg,
            **kwargs
        )
        
        pack_options = {'side': side}
        pack_options = {k: v for k, v in pack_options.items() if v is not None}
        
        radio_button.pack(**pack_options)
        return radio_button

