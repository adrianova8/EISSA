import tkinter as tk
from datetime import datetime

from src.app.window_app import AppWindow
from src.app.utils.frame_manager import FrameManager
from src.app.gadgets_app.gadget_utils import current_time
from src.utils.common.names import (
    BROWN_COLOR, METAL_GOLD_COLOR,
    BLACK_COLOR, BEIGE_COLOR
)


def create_sales_panel(app_window: AppWindow, frame_manager: FrameManager) -> tk.Frame:
    center_container = frame_manager.get_frame('center_container')
    sales_panel = app_window.create_frame(center_container, bg=BEIGE_COLOR, pady=21, padx=11, side="left")
    frame_manager.register_frame('sales_panel', sales_panel)
    return sales_panel


def create_totals_panel(app_window: AppWindow, parent: tk.Frame) -> tuple[tk.Label, tk.Label, tk.Label]:
    totals_frame = app_window.create_frame(parent, bg=BEIGE_COLOR, pady=11)
    totals_frame.pack()

    def make_total(label_text, color=METAL_GOLD_COLOR):
        frame = app_window.create_frame(totals_frame, bg=BEIGE_COLOR, padx=11, pady=6)
        app_window.create_label(frame, text=label_text, font=("Times New Roman", 16, "bold"), bg=BROWN_COLOR, fg=color)
        label = app_window.create_label(frame, text="0.00 €", font=("Times New Roman", 16), bg=BEIGE_COLOR, fg=BLACK_COLOR)
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
        font=("Times New Roman", 16, "bold"),
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

    scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=sales_canvas.yview)
    sales_canvas.configure(yscrollcommand=scrollbar.set)

    sales_content = app_window.create_frame(sales_canvas, bg=BEIGE_COLOR, padx=6, pady=21)
    canvas_window = sales_canvas.create_window((0, 0), window=sales_content, anchor="nw")

    def configure_scroll(event=None):
        sales_canvas.configure(scrollregion=sales_canvas.bbox("all"))

    def configure_canvas(event):
        sales_canvas.itemconfig(canvas_window, width=event.width - 20)

    def on_mousewheel(event): sales_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
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
            font=("Times New Roman", 11, "bold"),
            bg=BROWN_COLOR,
            fg=METAL_GOLD_COLOR,
            highlightbackground=BEIGE_COLOR,
            command=command,
            width=10
        )
        scroll_button.pack(side="left", padx=3)

    nav_frame.pack(pady=5)


def sales_visualizer_container(app_window: AppWindow, frame_manager: FrameManager) -> None:
    sales_panel = create_sales_panel(app_window, frame_manager)

    # Totals
    cash_total, card_total, total_sales = create_totals_panel(app_window, sales_panel)

    # Sales list section (canvas + scrollbar)
    create_sales_list_section(app_window, sales_panel, frame_manager)

    # Scroll buttons
    sales_list_frame = frame_manager.get_frame('sales_panel').winfo_children()[1]
    sales_canvas = frame_manager.get_frame('sales_canvas')
    create_scroll_buttons(app_window, sales_list_frame, sales_canvas)

    # Register totals
    frame_manager.register_frame('cash_total', cash_total)
    frame_manager.register_frame('card_total', card_total)
    frame_manager.register_frame('total_sales', total_sales)
