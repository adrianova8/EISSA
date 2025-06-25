import tkinter as tk
from tkinter import Tk
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass

from src.app.window_app import AppWindow
from src.utils.common.logger import CustomLogger
from src.app.utils.frame_manager import FrameManager
from src.app.gadgets_app.gadget_visualize_sales import add_sale_to_visualizer
from src.utils.common.names import (
    WHITE_COLOR, BROWN_COLOR, METAL_GOLD_COLOR,
    BLACK_COLOR, BEIGE_COLOR, GREEN_COLOR)

logger = CustomLogger()


@dataclass
class WidgetConfig:
    """Configuración para la creación de widgets"""
    widget_type: str
    text: Optional[str] = None
    font: Optional[tuple] = None
    bg: Optional[str] = None
    fg: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    side: Optional[str] = None
    padx: Optional[int] = None
    pady: Optional[int] = None
    bd: Optional[int] = None
    expand: Optional[bool] = None
    fill: Optional[str] = None
    variable: Optional[tk.StringVar] = None
    value: Optional[str] = None
    command: Optional[callable] = None
    initial_value: Optional[str] = None
    activebackground: Optional[str] = None
    activeforeground: Optional[str] = None
    highlightbackground: Optional[str] = None
    highlightcolor: Optional[str] = None


@dataclass
class SectionConfig:
    """Configuración completa para una sección de la interfaz"""
    container_config: WidgetConfig
    label_frame_config: Optional[WidgetConfig] = None
    label_config: Optional[WidgetConfig] = None
    widget_config: Optional[WidgetConfig] = None
    label_frame_width: Optional[int] = None
    label_frame_height: Optional[int] = None


class WidgetFactory:
    """Factory para crear widgets de manera consistente"""
    
    def __init__(self, app_window: AppWindow):
        self.app_window = app_window
    
    def create_widget(self, parent: tk.Widget, config: WidgetConfig) -> tk.Widget:
        """Crear un widget basado en su configuración"""
        # Extraer parámetros de configuración
        widget_params = self._extract_widget_params(config)
        pack_params = self._extract_pack_params(config)
        
        # Crear el widget según su tipo
        widget = self._create_widget_by_type(parent, config, widget_params)
        
        # Empaquetar si tiene parámetros de pack
        if pack_params:
            widget.pack(**pack_params)
        
        return widget
    
    def _create_widget_by_type(self, parent: tk.Widget, config: WidgetConfig, params: Dict[str, Any]) -> tk.Widget:
        """Crear widget específico según su tipo"""
        widget_type = config.widget_type.lower()
        
        if widget_type == 'frame':
            return self.app_window.create_frame(parent, **params)
        elif widget_type == 'label':
            return self.app_window.create_label(parent, **params)
        elif widget_type == 'entry':
            return self.app_window.create_entry(parent, **params)
        elif widget_type == 'button':
            return self.app_window.create_button(parent, **params)
        elif widget_type == 'radiobutton':
            return self.app_window.create_radio_button(parent, **params)
        elif widget_type == 'stringvar':
            return self.app_window.create_string_var(initial_value=config.initial_value or "")
        else:
            raise ValueError(f"Tipo de widget no soportado: {widget_type}")
    
    def _extract_widget_params(self, config: WidgetConfig) -> Dict[str, Any]:
        """Extraer parámetros específicos para la creación del widget"""
        params = {}
        widget_attrs = ['text', 'font', 'bg', 'fg', 'width', 'height', 'bd', 
                       'expand', 'fill', 'variable', 'value', 'command', 
                       'initial_value', 'activebackground', 'activeforeground',
                       'highlightbackground', 'highlightcolor']
        
        for attr in widget_attrs:
            value = getattr(config, attr, None)
            if value is not None:
                params[attr] = value
        
        return params
    
    def _extract_pack_params(self, config: WidgetConfig) -> Dict[str, Any]:
        """Extraer parámetros para el método pack"""
        params = {}
        pack_attrs = ['side', 'padx', 'pady', 'expand', 'fill']
        
        for attr in pack_attrs:
            value = getattr(config, attr, None)
            if value is not None:
                params[attr] = value
        
        return params


class SectionBuilder:
    """Builder para crear secciones completas de la interfaz"""
    
    def __init__(self, widget_factory: WidgetFactory):
        self.widget_factory = widget_factory
    
    def build_section(self, parent: tk.Widget, config: SectionConfig) -> Dict[str, tk.Widget]:
        """Construir una sección completa y retornar sus componentes"""
        components = {}
        
        # 1. Crear contenedor principal
        container = self.widget_factory.create_widget(parent, config.container_config)
        components['container'] = container
        
        # 2. Crear frame para label si está configurado
        if config.label_frame_config:
            label_frame = self.widget_factory.create_widget(container, config.label_frame_config)
            
            # Configurar propagación si se especifica
            if config.label_frame_width or config.label_frame_height:
                label_frame.pack_propagate(False)
                if config.label_frame_width:
                    label_frame.config(width=config.label_frame_width)
                if config.label_frame_height:
                    label_frame.config(height=config.label_frame_height)
            
            components['label_frame'] = label_frame
            
            # 3. Crear label si está configurado
            if config.label_config:
                label = self.widget_factory.create_widget(label_frame, config.label_config)
                components['label'] = label
        
        # 4. Crear widget principal si está configurado
        if config.widget_config:
            widget_parent = components.get('container', parent)
            main_widget = self.widget_factory.create_widget(widget_parent, config.widget_config)
            components['main_widget'] = main_widget
        
        return components


class SalesRegisterComponents:
    """Clase para mantener referencias a los widgets del registro de ventas"""
    def __init__(self):
        self.amount_entry = None
        self.received_entry = None
        self.change_display = None
        self.payment_var = None
        self.frame_manager = None
        self.app_window = None

    def calculate_change(self, *args):
        """Calculate and update change amount"""
        try:
            # Reemplazar coma por punto para el cálculo
            amount_str = self.amount_entry.get() if self.amount_entry.get() else '0'
            received_str = self.received_entry.get() if self.received_entry.get() else '0'
            
            # Convertir a float
            amount = float(amount_str.replace(',', '.'))
            received = float(received_str.replace(',', '.'))
            
            # Calcular cambio
            change = received - amount
            
            # Mostrar resultado con coma
            formatted_change = f"{change:.2f}".replace('.', ',')
            self.change_display.config(
                text=f"{formatted_change} €",
                fg=GREEN_COLOR if change >= 0 else "red"
            )
        except ValueError:
            self.change_display.config(text="Error", fg="red")

    def reset_fields(self):
        """Reset all form fields"""
        if self.amount_entry:
            self.amount_entry.delete(0, tk.END)
        if self.received_entry:
            self.received_entry.delete(0, tk.END)
        if self.change_display:
            self.change_display.config(text="0,00 €", fg=GREEN_COLOR)
        if self.amount_entry:
            self.amount_entry.focus()

    def save_sale(self):
        """Save the current sale"""
        try:
            amount_str = self.amount_entry.get().replace(',', '.')
            amount = float(amount_str)
            payment_method = "Efectiu" if self.payment_var.get() == "efectiu" else "Targeta"
            add_sale_to_visualizer(self.frame_manager, amount, payment_method)
            self.reset_fields()
            logger.info(f"Venta guardada: {amount}€ - {payment_method}")
        except ValueError:
            logger.info("Error: Introdueix un import vàlid.")


# Instancia global para mantener las referencias
sales_components = SalesRegisterComponents()


class SalesInterfaceConfigurator:
    """Configurador centralizado para la interfaz de ventas"""
    
    @staticmethod
    def get_panel_configs() -> Dict[str, SectionConfig]:
        """Obtener configuraciones para los paneles principales"""
        return {
            'main_container': SectionConfig(
                container_config=WidgetConfig(
                    widget_type='frame',
                    bg=BEIGE_COLOR,
                    fill="both",
                    expand=True,
                    padx=400
                )
            ),
            'center_container': SectionConfig(
                container_config=WidgetConfig(
                    widget_type='frame',
                    bg=BEIGE_COLOR,
                    expand=True
                )
            ),
            'payment_frame': SectionConfig(
                container_config=WidgetConfig(
                    widget_type='frame',
                    bg=BEIGE_COLOR,
                    pady=20,
                    padx=20,
                    side="left"
                )
            ),
            'entries_frame': SectionConfig(
                container_config=WidgetConfig(
                    widget_type='frame',
                    bg=BEIGE_COLOR,
                    padx=5,
                    pady=5,
                    bd=0.5
                )
            )
        }
    
    @staticmethod
    def get_widget_sections_configs() -> Dict[str, SectionConfig]:
        """Obtener configuraciones para las secciones de widgets"""
        return {
            'amount_section': SectionConfig(
                container_config=WidgetConfig(
                    widget_type='frame',
                    bg=BEIGE_COLOR
                ),
                label_frame_config=WidgetConfig(
                    widget_type='frame',
                    bg=BROWN_COLOR,
                    side="left"
                ),
                label_config=WidgetConfig(
                    widget_type='label',
                    text="Import a cobrar:",
                    font=("Times New Roman", 18),
                    bg=BROWN_COLOR,
                    fg=METAL_GOLD_COLOR,
                    side="left",
                    padx=5
                ),
                widget_config=WidgetConfig(
                    widget_type='entry',
                    font=("Times New Roman", 18),
                    bg=WHITE_COLOR,
                    fg=BLACK_COLOR,
                    highlightbackground=BEIGE_COLOR,
                    side="left"
                ),
                label_frame_width=150,
                label_frame_height=20
            ),
            'received_section': SectionConfig(
                container_config=WidgetConfig(
                    widget_type='frame',
                    bg=BEIGE_COLOR
                ),
                label_frame_config=WidgetConfig(
                    widget_type='frame',
                    bg=BROWN_COLOR,
                    side="left"
                ),
                label_config=WidgetConfig(
                    widget_type='label',
                    text="Import rebut:",
                    font=("Times New Roman", 18),
                    bg=BROWN_COLOR,
                    fg=METAL_GOLD_COLOR,
                    side="left",
                    padx=5
                ),
                widget_config=WidgetConfig(
                    widget_type='entry',
                    font=("Times New Roman", 18),
                    bg=WHITE_COLOR,
                    fg=BLACK_COLOR,
                    highlightbackground=BEIGE_COLOR,
                    side="left"
                ),
                label_frame_width=150,
                label_frame_height=20
            ),
            'change_section': SectionConfig(
                container_config=WidgetConfig(
                    widget_type='frame',
                    bg=BEIGE_COLOR
                ),
                label_frame_config=WidgetConfig(
                    widget_type='frame',
                    bg=BEIGE_COLOR,
                    side="left"
                ),
                label_config=WidgetConfig(
                    widget_type='label',
                    text="Canvi a tornar:",
                    font=("Times New Roman", 16),
                    bg=BEIGE_COLOR,
                    fg=BLACK_COLOR,
                    side="left",
                    padx=5
                ),
                widget_config=WidgetConfig(
                    widget_type='label',
                    text="0,00 €",
                    font=("Times New Roman", 16, "bold"),
                    bg=BEIGE_COLOR,
                    fg=GREEN_COLOR,
                    side="left"
                ),
                label_frame_width=120,
                label_frame_height=20
            ),
            'payment_method_section': SectionConfig(
                container_config=WidgetConfig(
                    widget_type='frame',
                    bg=BEIGE_COLOR,
                    pady=5
                )
            ),
            'buttons_section': SectionConfig(
                container_config=WidgetConfig(
                    widget_type='frame',
                    bg=BEIGE_COLOR,
                    pady=5,
                    padx=5
                )
            )
        }
    
    @staticmethod
    def get_button_configs() -> Dict[str, WidgetConfig]:
        """Obtener configuraciones para los botones"""
        return {
            'reset_button': WidgetConfig(
                widget_type='button',
                text="Netejar",
                font=("Times New Roman", 15),
                bg=BROWN_COLOR,
                fg=BLACK_COLOR,
                activebackground=BROWN_COLOR,
                activeforeground=BEIGE_COLOR,
                highlightbackground=BEIGE_COLOR,
                highlightcolor=BEIGE_COLOR,
                command=sales_components.reset_fields,
                side="left",
                padx=5
            ),
            'save_button': WidgetConfig(
                widget_type='button',
                text="Gravar venda",
                font=("Times New Roman", 15),
                bg=BROWN_COLOR,
                fg=BLACK_COLOR,
                activebackground=BROWN_COLOR,
                activeforeground=BEIGE_COLOR,
                highlightbackground=BEIGE_COLOR,
                highlightcolor=BEIGE_COLOR,
                command=sales_components.save_sale,
                side="left",
                padx=10
            )
        }
    
    @staticmethod
    def get_radio_button_configs(payment_var: tk.StringVar) -> Dict[str, WidgetConfig]:
        """Obtener configuraciones para los radio buttons"""
        return {
            'efectiu_radio': WidgetConfig(
                widget_type='radiobutton',
                text="Efectiu",
                variable=payment_var,
                value="efectiu",
                bg=BEIGE_COLOR,
                font=("Times New Roman", 15),
                side="left",
                padx=10
            ),
            'targeta_radio': WidgetConfig(
                widget_type='radiobutton',
                text="Targeta",
                variable=payment_var,
                value="targeta",
                bg=BEIGE_COLOR,
                font=("Times New Roman", 15),
                side="left",
                padx=10
            )
        }


def create_register_sales_panel(app: Tk, app_window: AppWindow, frame_manager: FrameManager) -> tk.Frame:
    """Crear el panel principal del registro de ventas usando el nuevo sistema"""
    widget_factory = WidgetFactory(app_window)
    section_builder = SectionBuilder(widget_factory)
    
    panel_configs = SalesInterfaceConfigurator.get_panel_configs()
    
    # Crear jerarquía de paneles
    panels = {}
    
    # Main container
    main_components = section_builder.build_section(app, panel_configs['main_container'])
    panels['main_container'] = main_components['container']
    frame_manager.register_frame('main_container', panels['main_container'])
    
    # Center container
    center_components = section_builder.build_section(panels['main_container'], panel_configs['center_container'])
    panels['center_container'] = center_components['container']
    frame_manager.register_frame('center_container', panels['center_container'])
    
    # Payment frame
    payment_components = section_builder.build_section(panels['center_container'], panel_configs['payment_frame'])
    panels['payment_frame'] = payment_components['container']
    frame_manager.register_frame('payment_frame', panels['payment_frame'])
    
    # Entries frame
    entries_components = section_builder.build_section(panels['payment_frame'], panel_configs['entries_frame'])
    panels['entries_frame'] = entries_components['container']
    frame_manager.register_frame('entries_frame', panels['entries_frame'])
    
    return panels['entries_frame']


def create_register_sales_widgets(app_window: AppWindow, entries_frame: tk.Frame, frame_manager: FrameManager) -> None:
    """Crear todos los widgets del registro de ventas usando el nuevo sistema"""
    
    # Guardar referencias necesarias
    sales_components.app_window = app_window
    sales_components.frame_manager = frame_manager
    
    widget_factory = WidgetFactory(app_window)
    section_builder = SectionBuilder(widget_factory)
    
    # Obtener configuraciones
    widget_configs = SalesInterfaceConfigurator.get_widget_sections_configs()
    button_configs = SalesInterfaceConfigurator.get_button_configs()
    
    # 1. Crear sección de importe
    amount_components = section_builder.build_section(entries_frame, widget_configs['amount_section'])
    sales_components.amount_entry = amount_components['main_widget']
    amount_components['container'].pack()
    
    # 2. Crear sección de importe recibido
    received_components = section_builder.build_section(entries_frame, widget_configs['received_section'])
    sales_components.received_entry = received_components['main_widget']
    received_components['container'].pack()
    
    # 3. Crear sección de cambio
    change_components = section_builder.build_section(entries_frame, widget_configs['change_section'])
    sales_components.change_display = change_components['main_widget']
    change_components['container'].pack()
    
    # 4. Crear sección de método de pago
    payment_components = section_builder.build_section(entries_frame, widget_configs['payment_method_section'])
    payment_container = payment_components['container']
    
    # Crear StringVar para método de pago
    sales_components.payment_var = widget_factory.create_widget(
        None, 
        WidgetConfig(widget_type='stringvar', initial_value="efectiu")
    )
    
    # Crear radio buttons
    radio_configs = SalesInterfaceConfigurator.get_radio_button_configs(sales_components.payment_var)
    for radio_config in radio_configs.values():
        widget_factory.create_widget(payment_container, radio_config)
    
    # 5. Crear sección de botones
    buttons_components = section_builder.build_section(entries_frame, widget_configs['buttons_section'])
    buttons_container = buttons_components['container']
    
    # Crear botones
    for button_config in button_configs.values():
        widget_factory.create_widget(buttons_container, button_config)


def setup_event_bindings(app: Tk) -> None:
    """Configurar los event bindings"""
    # Vincular eventos para el cálculo del cambio
    if sales_components.amount_entry:
        sales_components.amount_entry.bind('<KeyRelease>', sales_components.calculate_change)
    
    if sales_components.received_entry:
        sales_components.received_entry.bind('<KeyRelease>', sales_components.calculate_change)
    
    # Vincular tecla Escape para resetear campos
    app.bind('<Escape>', lambda e: sales_components.reset_fields())


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
    create_register_sales_widgets(app_window, entries_frame, frame_manager)
    
    # Setup event bindings
    setup_event_bindings(app)