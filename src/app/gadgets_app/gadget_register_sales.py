import tkinter as tk
from tkinter import Tk

from src.app.window_app import AppWindow
from src.utils.common.logger import CustomLogger
from src.app.utils.frame_manager import FrameManager
from src.app.gadgets_app.gadget_visualize_sales import add_sale_to_visualizer
from src.utils.common.names import (
    WHITE_COLOR, BROWN_COLOR, METAL_GOLD_COLOR,
    BLACK_COLOR, BEIGE_COLOR, GREEN_COLOR)

logger = CustomLogger()


# Crear una función que a la hora de hacer un create frame o un create label se le pasen los parametros que se van a utilizar
def build_interface_component(app_window: AppWindow, component_type: str, parent, **kwargs) -> tk.Widget:
    """
    Función genérica para crear widgets (frames o labels) con parámetros personalizados
    
    Args:
        component_type (str): Tipo de widget a crear ('frame' o 'label')
        parent: Widget padre donde se creará el nuevo widget
        **kwargs: Parámetros de configuración del widget (bg, width, height, etc.)
    
    Returns:
        Frame o Label según el component_type especificado
    """
    if component_type.lower() == 'frame':
        return app_window.create_frame(parent, **kwargs)
    elif component_type.lower() == 'label':
        return app_window.create_label(parent, **kwargs)
    else:
        raise ValueError("component_type debe ser 'frame' o 'label'")
    


def create_register_sales_panel(app: Tk, app_window: AppWindow, frame_manager: FrameManager) -> tk.Frame:
    # Create the global payment container frame
    main_container = build_interface_component(
        app_window,
        "frame",
        app,
        bg="red",
        fill="both",
        expand=True,
        padx=400
    )
    # Add the global payment container frame to the Frame Manager
    frame_manager.register_frame('main_container', main_container)

    # Create a frame that is inside the global payment container frame
    center_container = build_interface_component(
        app_window,
        "frame",
        main_container,
        bg="green",
        expand=True
    )
    # Add the center container frame to the Frame Manager
    frame_manager.register_frame('center_container', center_container)

    # Create another frame inside the center container
    payment_frame = build_interface_component(
        app_window,
        "frame",
        center_container,
        bg='orange',
        pady=20,
        padx=20,
        side="left"
    )
    # Add the payment frame to the Frame Manager
    frame_manager.register_frame('payment_frame', payment_frame)

    # Create a frame for the entries and labels
    entries_frame = build_interface_component(
        app_window,
        "frame",
        payment_frame,
        bg= 'black',
        padx=5,
        pady=5,
        bd=0.5
    )
    # Add the entries frame to the Frame Manager
    frame_manager.register_frame('entries_frame', entries_frame)
    return entries_frame


def create_register_sales_widgets(app_window: AppWindow, entries_frame: tk.Frame) -> None:
   # 1.- Create a frame for the amout label and entry
    amount_container = build_interface_component(
        app_window,
        "frame",
        entries_frame,
        bg="pink"
    )

    # Create a Frame for the amount label with a fix width
    amount_label_frame = build_interface_component(
        app_window,
        "frame",
        amount_container,
        bg="pink",
        width=150,
        height=20
    )
    amount_label_frame.pack_propagate(False)

    # Create the Label for the amount label
    build_interface_component(
        app_window,
        "label",
        amount_label_frame,
        text="Import a cobrar:",
        font=("Times New Roman", 18),
        bg="pink",
        fg=BLACK_COLOR,
        side = "left",
        padx=5
    )
    amount_label_frame.pack(side="left")

    # Create the Entry for the amount
    app_window.create_entry(
        amount_container, 
        font=("Times New Roman", 18),
        bg=WHITE_COLOR,
        fg=BLACK_COLOR,
        highlightbackground=BEIGE_COLOR,
        side="left"
    )
    amount_container.pack()

    # 2.- Create a frame for the received label and entry
    received_container = build_interface_component(
        app_window,
        "frame",
        entries_frame,
        bg=BEIGE_COLOR
    )

    # Create a Frame for the received money label with a fix width and height
    received_label_frame = build_interface_component(
        app_window,
        "frame",
        received_container,
        bg=BROWN_COLOR,
        width=150,
        height=20
    )
    received_label_frame.pack_propagate(False)

    # Create the Label for the received money label
    build_interface_component(
        app_window,
        "label",
        received_label_frame,
        text="Import rebut:",
        font=("Times New Roman", 18),
        bg=BROWN_COLOR,
        fg=METAL_GOLD_COLOR,
        side="left",
        padx=5
    )
    received_label_frame.pack(side="left")

    # Create the Entry for the received money
    app_window.create_entry(
        received_container, 
        font=("Times New Roman", 18),
        bg=WHITE_COLOR,
        fg=BLACK_COLOR,
        highlightbackground=BEIGE_COLOR,
        side="left"
    )
    received_container.pack()

    # 3. Create a Frame for the change label and display
    change_container = build_interface_component(
        app_window,
        "frame",
        entries_frame,
        bg=BEIGE_COLOR
    )

    # Create a Frame for the change label with a fix width and height
    change_label_frame = build_interface_component(
        app_window,
        "frame",
        change_container,
        bg=BEIGE_COLOR,
        width=120,
        height=20
    )
    change_label_frame.pack_propagate(False)

    # Create the Label for the change label    
    build_interface_component(
        app_window,
        "label",
        change_label_frame,
        text="Canvi a tornar:",
        font=("Times New Roman", 16),
        bg=BEIGE_COLOR,
        fg=BLACK_COLOR,
        side="left",
        padx=5
    )
    change_label_frame.pack(side="left")
    
    # Create the display for the change amount
    change_display_frame = build_interface_component(
        app_window,
        "frame",
        change_container,
        bg=BEIGE_COLOR,
        side = "left"
    )
    
    build_interface_component(
        app_window,
        "label",
        change_display_frame,
        text="0.00 €",
        font=("Times New Roman", 16, "bold"),
        bg=BEIGE_COLOR,
        fg=GREEN_COLOR,
        side="left"
    )
    # Empaquetar el contenedor
    change_container.pack()
    

def payment_container(app: Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
    """
    Create payment management container with amount, received and change calculation.
    
    Args:
        app (Tk): Main window instance
        app_window (AppWindow): Window manager instance
        frame_manager (FrameManager): Frame management instance
    """
    # Create register sales panel
    entries_frame = create_register_sales_panel(app, app_window, frame_manager)

    # Create widgets for the register sales panel
    create_register_sales_widgets(app_window, entries_frame)







    # def calculate_change(*args):
    #     """Calculate and update change amount"""
    #     try:
    #         # Reemplazar coma por punto para el cálculo
    #         amount_str = amount_entry.get() if amount_entry.get() else '0'
    #         received_str = received_entry.get() if received_entry.get() else '0'
            
    #         # Convertir a float
    #         amount = float(amount_str)
    #         received = float(received_str)
            
    #         # Calcular cambio
    #         change = received - amount
            
    #         # Mostrar resultado con coma
    #         formatted_change = f"{change:.2f}"
    #         change_display.config(
    #             text=f"{formatted_change} €",
    #             fg="green" if change >= 0 else "red"
    #         )
    #     except ValueError:
    #         change_display.config(text="Error", fg="red")

    # def reset_fields():
    #     """Reset all form fields"""
    #     amount_entry.delete(0, tk.END)
    #     received_entry.delete(0, tk.END)
    #     change_display.config(text="0.00 €", fg="green")
    #     amount_entry.focus()

    # # Frame para botones
    # buttons_frame = app_window.create_frame(
    #     entries_frame,
    #     bg=BEIGE_COLOR,
    #     pady=10,
    #     padx=5,
    #     bd=0.5
    # )

    # # Botón reset con configuración completa de colores
    # reset_button = tk.Button(
    #     buttons_frame,
    #     text="Netejar",
    #     font=("Times New Roman", 15),
    #     bg=BROWN_COLOR,            # Color de fondo del botón
    #     fg=BLACK_COLOR,         # Color del texto
    #     activebackground=BROWN_COLOR, # Color cuando se presiona
    #     activeforeground=BEIGE_COLOR, # Color del texto cuando se presiona 
    #     highlightbackground=BEIGE_COLOR,   # Color del borde cuando no tiene foco
    #     highlightcolor=BEIGE_COLOR,   # Color del borde cuando tiene foco
    #     command=reset_fields
    # )
    # reset_button.pack(side="left", padx=5)

    # # 5. Frame para método de pago
    # payment_method_frame = app_window.create_frame(
    #     entries_frame,
    #     bg=WHITE_COLOR,
    #     pady=5
    # )

    # # Variable para radio buttons
    # payment_var = tk.StringVar(value="efectiu")  # Valor por defecto

    # # Radio buttons para método de pago
    # cash_rb = tk.Radiobutton(
    #     payment_method_frame,
    #     text="Efectiu",
    #     variable=payment_var,
    #     value="efectiu",
    #     bg=WHITE_COLOR,
    #     font=("Times New Roman", 15)
    # )
    # cash_rb.pack(side="left", padx=10)

    # card_rb = tk.Radiobutton(
    #     payment_method_frame,
    #     text="Targeta",
    #     variable=payment_var,
    #     value="targeta",
    #     bg=WHITE_COLOR,
    #     font=("Times New Roman", 15)
    # )
    # card_rb.pack(side="left", padx=10)

    # def save_sale():
    #     try:
    #         amount = float(amount_entry.get())
    #         payment_method = "Efectiu" if payment_var.get() == "efectiu" else "Targeta"
    #         add_sale_to_visualizer(frame_manager, amount, payment_method)
    #         reset_fields()
    #     except ValueError:
    #         logger.info("Error: Introdueix un import válid.")

    # # Botón grabar
    # save_button = tk.Button(
    #     buttons_frame,
    #     text="Gravar venda",
    #     font=("Times New Roman", 15),
    #     bg=BROWN_COLOR,            # Color de fondo del botón
    #     fg=BLACK_COLOR,         # Color del texto
    #     activebackground=BROWN_COLOR, # Color cuando se presiona
    #     activeforeground=BEIGE_COLOR, # Color del texto cuando se presiona 
    #     highlightbackground=BEIGE_COLOR,   # Color del borde cuando no tiene foco
    #     highlightcolor=BEIGE_COLOR,   # Color del borde cuando tiene foco
    #     command=save_sale
    # )
    # save_button.pack(side="left", padx=10)

    # # # Vincular eventos
    # amount_entry.bind('<KeyRelease>', calculate_change)
    # received_entry.bind('<KeyRelease>', calculate_change)
    # app.bind('<Escape>', lambda e: reset_fields())
