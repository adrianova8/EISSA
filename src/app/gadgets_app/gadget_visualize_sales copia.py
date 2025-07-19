import tkinter as tk
from tkinter import Tk
from datetime import datetime

from src.app.window_app import AppWindow
from src.app.utils.frame_manager import FrameManager
from src.app.gadgets_app.gadget_utils import current_time
from src.utils.common.names import (
    WHITE_COLOR, BROWN_COLOR, METAL_GOLD_COLOR,
    BLACK_COLOR, BEIGE_COLOR, GREEN_COLOR
)


def sales_visualizer_container(app: Tk, app_window: AppWindow, frame_manager: FrameManager) -> None:
    center_container = frame_manager.get_frame('center_container')

    sales_panel = app_window.create_frame(
        center_container,
        bg=BEIGE_COLOR,
        pady=21,
        padx=11,
        side="left"
    )
    frame_manager.register_frame('sales_panel', sales_panel)

    # Totales
    totals_frame = app_window.create_frame(sales_panel, bg=BEIGE_COLOR, pady=11)

    def make_total_frame(label, color=METAL_GOLD_COLOR):
        f = app_window.create_frame(totals_frame, bg=BEIGE_COLOR, padx=11, pady=6)
        app_window.create_label(f, text=label, font=("Times New Roman", 16, "bold"), bg=BROWN_COLOR, fg=color)
        lbl = app_window.create_label(f, text="0.00 €", font=("Times New Roman", 16), bg=BEIGE_COLOR, fg=BLACK_COLOR)
        f.pack(side="left", padx=11)
        return lbl

    cash_total = make_total_frame("Efectiu")
    card_total = make_total_frame("Targeta")
    total_sales = make_total_frame("Total Vendes")

    # Lista de ventas
    sales_list_frame = app_window.create_frame(sales_panel, bg=BEIGE_COLOR, pady=11)

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

    scrollbar = tk.Scrollbar(
        canvas_container,
        orient="vertical",
        command=sales_canvas.yview
    )
    sales_canvas.configure(yscrollcommand=scrollbar.set)

    sales_content = app_window.create_frame(sales_canvas, bg=BEIGE_COLOR, padx=6, pady=21)

    canvas_window = sales_canvas.create_window((0, 0), window=sales_content, anchor="nw")

    # Scroll bindings
    def configure_scroll(event=None):
        sales_canvas.configure(scrollregion=sales_canvas.bbox("all"))

    def configure_canvas(event):
        sales_canvas.itemconfig(canvas_window, width=event.width - 20)

    def on_mousewheel(event):
        sales_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_mousewheel_linux(event):
        if event.num == 4:
            sales_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            sales_canvas.yview_scroll(1, "units")

    sales_content.bind("<Configure>", configure_scroll)
    sales_canvas.bind("<Configure>", configure_canvas)
    canvas_container.bind_all("<MouseWheel>", on_mousewheel)
    canvas_container.bind_all("<Button-4>", on_mousewheel_linux)
    canvas_container.bind_all("<Button-5>", on_mousewheel_linux)

    sales_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Botones scroll
    nav_frame = app_window.create_frame(sales_list_frame, bg=BEIGE_COLOR, pady=5)

    def scroll_to_top(): sales_canvas.yview_moveto(0.0)
    def scroll_to_bottom(): sales_canvas.yview_moveto(1.0)
    def scroll_up(): sales_canvas.yview_scroll(-3, "units")
    def scroll_down(): sales_canvas.yview_scroll(3, "units")

    for text, cmd in [
        ("⬆⬆ Dalt", scroll_to_top),
        ("⬆ Amunt", scroll_up),
        ("⬇ Avall", scroll_down),
        ("⬇⬇ Baix", scroll_to_bottom)
    ]:
        tk.Button(nav_frame, text=text, font=("Times New Roman", 11, "bold"),
                  bg=BROWN_COLOR, fg=METAL_GOLD_COLOR,
                  activebackground=METAL_GOLD_COLOR, activeforeground=BROWN_COLOR,
                  highlightbackground=BEIGE_COLOR, command=cmd, width=10).pack(side="left", padx=3)

    nav_frame.pack(pady=5)

    frame_manager.register_frame('sales_content', sales_content)
    frame_manager.register_frame('cash_total', cash_total)
    frame_manager.register_frame('card_total', card_total)
    frame_manager.register_frame('total_sales', total_sales)
    frame_manager.register_frame('sales_canvas', sales_canvas)


def add_sale_to_visualizer(frame_manager: FrameManager, amount: float, payment_method: str):
    sales_content = frame_manager.get_frame('sales_content')
    cash_total = frame_manager.get_frame('cash_total')
    card_total = frame_manager.get_frame('card_total')
    total_sales = frame_manager.get_frame('total_sales')
    sales_canvas = frame_manager.get_frame('sales_canvas')

    sale_frame = tk.Frame(sales_content, bg=BEIGE_COLOR, relief="solid", bd=1)
    sale_frame.pack(fill="x", pady=3, padx=2)

    time_now = datetime.now().strftime("%H:%M:%S")
    sale_text = f"{time_now} - {amount:.2f}€ ({payment_method})"
    tk.Label(
        sale_frame,
        text=sale_text,
        font=("Times New Roman", 13),
        bg=METAL_GOLD_COLOR,
        fg=BLACK_COLOR,
        padx=5,
        pady=3
    ).pack(anchor="w", fill="x")

    try:
        current_cash = float(cash_total.cget("text").replace("€", "").strip())
        current_card = float(card_total.cget("text").replace("€", "").strip())
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

    sales_canvas.update_idletasks()
    sales_canvas.configure(scrollregion=sales_canvas.bbox("all"))
    sales_canvas.yview_moveto(1.0)
