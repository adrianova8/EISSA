
import tkinter as tk
from typing import Union, Optional, Tuple

from src.utils.common.paths import ProjectPaths
from src.utils.common.names import (
    WHITE_COLOR, BROWN_COLOR, METAL_GOLD_COLOR,
    BLACK_COLOR, BEIGE_COLOR, GREEN_COLOR)

paths = ProjectPaths()

class AppWindow:
    def __init__(self, app: tk.Tk):
        """
        Initialize AppWindow with a Tkinter root window.

        Args:
            app (tk.Tk): The root Tkinter window instance.
        """
        self.app = app
        
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


    def window_dimensions(
        self,
        screen_division: float = 2.0,
        height_ratio: float = 1.2,
        horizontal_position: int = 2,
        vertical_position: int = 2
    ) -> Optional[Tuple[int, int, int, int]]:
        """
        Configure window dimensions and position with screen limits.
    
        Args:
            screen_division (float): Screen width division factor (2 = half, 3 = third, etc).
            height_ratio (float): Window height/width ratio (1.0 = square, >1 = taller).
            horizontal_position (int): Horizontal position division factor (2 = center).
            vertical_position (int): Vertical position division factor (2 = center).
    
        Returns:
            Optional[Tuple[int, int, int, int]]: Window dimensions and position (width, height, x, y)
                or None if configuration fails.
    
        Raises:
            ValueError: If any input parameter is <= 0.
            tk.TclError: If window geometry cannot be set.
            ZeroDivisionError: If division by zero occurs during calculations.
        """
        try:
            screen_width = self.app.winfo_screenwidth()
            screen_height = self.app.winfo_screenheight()
            
            # Parameter validation
            def validate_param(value: Union[int, float], name: str, default: Union[int, float]) -> Union[int, float]:
                if value <= 0:
                    raise ValueError(f"{name} must be greater than 0. Using default: {default}")
                return value
            
            # Apply validations
            try:
                screen_division = validate_param(screen_division, "screen_division", 2.0)
                height_ratio = validate_param(height_ratio, "height_ratio", 1.2)
                horizontal_position = validate_param(horizontal_position, "horizontal_position", 2)
                vertical_position = validate_param(vertical_position, "vertical_position", 2)
            except ValueError as e:
                print(f"Warning: {str(e)}")
            
            # Calculate initial dimensions
            window_width = int(screen_width // screen_division)
            window_height = int(window_width * height_ratio)
            
            # Ensure dimensions don't exceed screen
            if window_width > screen_width:
                window_width = screen_width
                window_height = int(window_width * height_ratio)
            
            if window_height > screen_height:
                window_height = screen_height
                window_width = int(window_height / height_ratio)
            
            # Ensure window is visible (minimum 200x200)
            window_width = max(200, min(window_width, screen_width))
            window_height = max(200, min(window_height, screen_height))
            
            # Calculate position ensuring window stays within screen
            position_x = min(max(0, int((screen_width - window_width) // horizontal_position)), screen_width - window_width)
            position_y = min(max(0, int((screen_height - window_height) // vertical_position)), screen_height - window_height)
            
            # Set window geometry
            geometry_data = f"{window_width}x{window_height}+{position_x}+{position_y}"
            self.app.geometry(geometry_data)
            
            return window_width, window_height, position_x, position_y
            
        except tk.TclError as e:
            print(f"Error setting window geometry: {str(e)}")
            return None
        except ZeroDivisionError as e:
            print(f"Error in calculations: {str(e)}")
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
            label.image = image  # Mantener referencia
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

