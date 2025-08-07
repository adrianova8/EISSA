import tkinter as tk
from datetime import datetime

from src.app.window_app import AppWindow
from src.utils.common.logger import CustomLogger
from src.app.utils.frame_manager import FrameManager
from src.app.gadgets_app.gadget_utils import current_time
from src.data.db.sales_record_db import get_sales_by_date
from src.utils.common.names import (
    BROWN_COLOR, METAL_GOLD_COLOR, BLACK_COLOR, BEIGE_COLOR)

logger = CustomLogger()


def create_sales_panel(app_window: AppWindow, frame_manager: FrameManager) -> tk.Frame:
    center_container = frame_manager.get_frame('center_container')
    sales_panel = app_window.create_frame(
        center_container, bg=BEIGE_COLOR, side="left")
    frame_manager.register_frame('sales_panel', sales_panel)
    return sales_panel


def create_totals_panel(app_window: AppWindow, parent: tk.Frame) -> tuple[tk.Label, tk.Label, tk.Label]:
    totals_frame = app_window.create_frame(parent, bg=BEIGE_COLOR, pady=11)
    totals_frame.pack()

    def make_total(label_text, color=METAL_GOLD_COLOR):
        frame = app_window.create_frame(
            totals_frame, bg=BEIGE_COLOR, padx=11, pady=6)
        app_window.create_label(frame, text=label_text, font=(
            "Times New Roman", 14, "bold"), bg=BROWN_COLOR, fg=color)
        label = app_window.create_label(frame, text="0.00 €", font=(
            "Times New Roman", 14), bg=BEIGE_COLOR, fg=BLACK_COLOR)
        frame.pack(side="left", padx=11)
        return label

    cash = make_total("Efectiu")
    card = make_total("Targeta")
    total = make_total("Total Vendes")
    return cash, card, total


def create_sales_list_section(app_window: AppWindow, parent: tk.Frame, frame_manager: FrameManager):
    sales_list_frame = app_window.create_frame(parent, bg=BEIGE_COLOR, pady=11)
    sales_list_frame.pack()

    app_window.create_label(
        sales_list_frame,
        text=f"Registre de vendes dia {current_time()}",
        font=("Times New Roman", 14, "bold"),
        bg=BEIGE_COLOR,
        fg=BLACK_COLOR
    )

    canvas_container = app_window.create_frame(sales_list_frame, bg="green")
    canvas_container.pack(fill="both", expand=True, pady=5)

    sales_canvas = tk.Canvas(
        canvas_container,
        bg=BEIGE_COLOR,
        width=451,
        height=501,
        highlightthickness=3,
        highlightbackground=BROWN_COLOR,
    )

    scrollbar = tk.Scrollbar(
        canvas_container, orient="vertical", command=sales_canvas.yview)
    sales_canvas.configure(yscrollcommand=scrollbar.set)

    sales_content = app_window.create_frame(
        sales_canvas, bg=BEIGE_COLOR, padx=6, pady=21)
    canvas_window = sales_canvas.create_window(
        (0, 0), window=sales_content, anchor="nw")

    def configure_scroll(event=None):
        sales_canvas.configure(scrollregion=sales_canvas.bbox("all"))

    def configure_canvas(event):
        sales_canvas.itemconfig(canvas_window, width=event.width - 20)

    def on_mousewheel(event): sales_canvas.yview_scroll(
        int(-1 * (event.delta / 120)), "units")

    def on_mousewheel_linux(event):
        sales_canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

    sales_content.bind("<Configure>", configure_scroll)
    sales_canvas.bind("<Configure>", configure_canvas)
    canvas_container.bind_all("<MouseWheel>", on_mousewheel)
    canvas_container.bind_all("<Button-4>", on_mousewheel_linux)
    canvas_container.bind_all("<Button-5>", on_mousewheel_linux)

    sales_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    frame_manager.register_frame('sales_content', sales_content)
    frame_manager.register_frame('sales_canvas', sales_canvas)


def create_scroll_buttons(app_window: AppWindow, parent: tk.Frame, canvas: tk.Canvas):
    nav_frame = app_window.create_frame(parent, bg=BEIGE_COLOR, pady=5)

    def scroll_to_top(): canvas.yview_moveto(0.0)
    def scroll_to_bottom(): canvas.yview_moveto(1.0)
    def scroll_up(): canvas.yview_scroll(-3, "units")
    def scroll_down(): canvas.yview_scroll(3, "units")

    buttons = [
        ("⬆⬆ Dalt", scroll_to_top),
        ("⬆ Amunt", scroll_up),
        ("⬇ Avall", scroll_down),
        ("⬇⬇ Baix", scroll_to_bottom)
    ]

    for text, command in buttons:
        scroll_button = app_window.create_button(
            nav_frame,
            text=text,
            font=("Times New Roman", 10),
            bg=BROWN_COLOR,
            fg=METAL_GOLD_COLOR,
            highlightbackground=BEIGE_COLOR,
            command=command,
            width=10
        )
        scroll_button.pack(side="left", padx=3)

    nav_frame.pack(pady=5)


def add_sale_to_visualizer_only(app_window: AppWindow, frame_manager: FrameManager,
                                time_str: str, amount: float, payment_method: str,
                                update_totals: bool = True):
    """
    Función para añadir una venta al visualizador sin duplicar en BD
    Útil para cargar ventas existentes desde la base de datos
    """
    sales_content = frame_manager.get_frame('sales_content')

    # Crear frame para la venta
    sale_frame = app_window.create_frame(
        sales_content, bg=BEIGE_COLOR, relief="solid", bd=1)
    sale_frame.pack(fill="x", pady=3, padx=2)

    # Crear texto de la venta
    sale_text = f"[{time_str}] {amount:.2f}€ ({payment_method})"
    sales_label = app_window.create_label(
        sale_frame,
        text=sale_text,
        font=("Times New Roman", 13),
        bg=METAL_GOLD_COLOR,
        fg=BLACK_COLOR,
        padx=5,
        pady=3
    )
    sales_label.pack(anchor="w", fill="x")

    # Actualizar totales si se solicita
    if update_totals:
        cash_total = frame_manager.get_frame('cash_total')
        card_total = frame_manager.get_frame('card_total')
        total_sales = frame_manager.get_frame('total_sales')

        try:
            current_cash = float(cash_total.cget(
                "text").replace("€", "").strip())
            current_card = float(card_total.cget(
                "text").replace("€", "").strip())
        except ValueError:
            current_cash = 0.0
            current_card = 0.0

        if payment_method == "Efectiu":
            current_cash += amount
            cash_total.config(text=f"{current_cash:.2f} €")
        else:
            current_card += amount
            card_total.config(text=f"{current_card:.2f} €")

        total_sales.config(text=f"{(current_cash + current_card):.2f} €")


def load_today_sales_from_db(app_window: AppWindow, frame_manager: FrameManager):
    """
    Load today's sales from the database into the visualizer
    """
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        sales = get_sales_by_date(today)

        if sales:
            logger.info(f"Carregant {len(sales)} vendes del dia {today}")

            # Cargar cada venta al visualizador
            for time_str, amount, method in sales:
                add_sale_to_visualizer_only(
                    app_window, frame_manager, time_str, amount, method)

            # Actualizar scroll para mostrar la última venta
            sales_canvas = frame_manager.get_frame('sales_canvas')
            sales_canvas.update_idletasks()
            sales_canvas.configure(scrollregion=sales_canvas.bbox("all"))
            sales_canvas.yview_moveto(1.0)

            logger.info(f"S'han carregat {len(sales)} vendes del dia actual")
        else:
            logger.info("No hi ha vendes registrades per al dia d'avui")

    except Exception as e:
        logger.error(f"Error al carregar vendes del dia desde la BD: {e}")


def sales_visualizer_container(app_window: AppWindow, frame_manager: FrameManager) -> None:
    """
    Load the current sales when the visualizer is initialized.
    """
    sales_panel = create_sales_panel(app_window, frame_manager)

    # Totals
    cash_total, card_total, total_sales = create_totals_panel(
        app_window, sales_panel)

    # Sales list section (canvas + scrollbar)
    create_sales_list_section(app_window, sales_panel, frame_manager)

    # Scroll buttons
    sales_list_frame = frame_manager.get_frame(
        'sales_panel').winfo_children()[1]
    sales_canvas = frame_manager.get_frame('sales_canvas')
    create_scroll_buttons(app_window, sales_list_frame, sales_canvas)

    # Register totals
    frame_manager.register_frame('cash_total', cash_total)
    frame_manager.register_frame('card_total', card_total)
    frame_manager.register_frame('total_sales', total_sales)

    # NUEVO: Cargar ventas del día actual desde la base de datos
    # Usamos after() para asegurar que todos los widgets estén inicializados
    frame_manager.get_frame('sales_panel').after(100,
                                                 lambda: load_today_sales_from_db(app_window, frame_manager))
