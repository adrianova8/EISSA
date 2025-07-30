import sqlite3
import tkinter as tk
from datetime import datetime, timedelta

from src.app.window_app import AppWindow
from src.utils.common.paths import ProjectPaths
from src.app.utils.frame_manager import FrameManager
from src.data.db.sales_record_db import get_sales_by_date
from src.utils.common.names import (WHITE_COLOR, BROWN_COLOR, METAL_GOLD_COLOR, BLACK_COLOR, BEIGE_COLOR, GREEN_COLOR)

paths = ProjectPaths()

DB_NAME = f"{paths.database_dir}/sales.db"

def update_display(state):
    app_window = state["app_window"]
    selected_date = state["selected_date"]
    current_date = state["current_date"]
    content_frame = state["content_frame"]
    date_label = state["date_label"]
    canvas = state["canvas"]
    db_path =  DB_NAME

    # Actualizar fecha
    date_str = selected_date.strftime('%d/%m/%Y')
    if selected_date.date() == current_date.date():
        date_str += " (Avui)"
    date_label.config(text=date_str)

    # Limpiar contenido anterior
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Título del día
    app_window.create_label(
        content_frame,
        text=f"Vendes del {selected_date.strftime('%d/%m/%Y')}",
        font=("Times New Roman", 16),
        bg=BROWN_COLOR,
        fg=METAL_GOLD_COLOR,
    ).pack(fill="x")

    # Query the database for sales data
    sales_data = []
    try:
        selected_date = selected_date.strftime("%Y-%m-%d")
        rows = get_sales_by_date(selected_date)

        for row in rows:
            sales_data.append({
                "time": row[0],
                "amount": row[1],
                "method": row[2]
            })
    except sqlite3.Error as e:
        print("Error accedint a la base de dades:", e)

    total_efectiu = 0
    total_targeta = 0

    for sale in sales_data:
        sale_frame = app_window.create_frame(content_frame, bg=METAL_GOLD_COLOR, relief="solid", bd=1)
        sale_frame.pack(fill="x")
        app_window.create_label(
            sale_frame,
            text=f"{sale['time']} - {sale['amount']:.2f}€ ({sale['method']})",
            font=("Times New Roman", 11),
            bg=METAL_GOLD_COLOR,
            fg=BLACK_COLOR,
        ).pack(anchor="w")

        if sale['method'] == "Efectiu":
            total_efectiu += sale['amount']
        else:
            total_targeta += sale['amount']

    totals_frame = app_window.create_frame(content_frame, bg=BEIGE_COLOR)
    totals_frame.pack(fill="x")

    app_window.create_label(
        totals_frame,
        text=f"Efectiu: {total_efectiu:.2f}€",
        font=("Times New Roman", 12),
        bg=BROWN_COLOR,
        fg=METAL_GOLD_COLOR
    ).pack(fill="x")

    app_window.create_label(
        totals_frame,
        text=f"Targeta: {total_targeta:.2f}€",
        font=("Times New Roman", 12),
        bg=BROWN_COLOR,
        fg=METAL_GOLD_COLOR
    ).pack(fill="x")

    app_window.create_label(
        totals_frame,
        text=f"TOTAL: {(total_efectiu + total_targeta):.2f}€",
        font=("Times New Roman", 14),
        bg=GREEN_COLOR,
        fg=WHITE_COLOR,
    ).pack(fill="x")

    # Scroll al final
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def historical_sales_navigator_container(app, app_window: AppWindow, frame_manager: FrameManager):

    # Initialize context
    current_date = datetime.now()
    selected_date = current_date

    state = {
        "app": app,
        "app_window": app_window,
        "frame_manager": frame_manager,
        "current_date": current_date,
        "selected_date": selected_date,
        "content_frame": None,
        "date_label": None
    }
    parent = frame_manager.get_frame('payment_frame')

    # Historical visualizer frame
    frame = app_window.create_frame(parent, bg=BEIGE_COLOR, side="top")

    # Historical visualizer title
    app_window.create_label(
        frame,
        text="Històric de Vendes",
        font=("Times New Roman", 18),
        bg=BEIGE_COLOR,
        fg=BLACK_COLOR
    )

    # Historical visualizer navigator frame
    nav_frame = app_window.create_frame(frame, bg=BEIGE_COLOR)

    # Functions to navigate through dates
    def go_previous():
        state["selected_date"] -= timedelta(days=1)
        update_display(state)

    def go_next():
        if state["selected_date"].date() < state["current_date"].date():
            state["selected_date"] += timedelta(days=1)
            update_display(state)

    def go_today():
        state["selected_date"] = state["current_date"]
        update_display(state)

    app_window.create_button(nav_frame, "◀ Anterior", command=go_previous, font=("Times New Roman", 12),
                             bg=BROWN_COLOR, fg=METAL_GOLD_COLOR, highlightbackground=BEIGE_COLOR, width=8).pack(side="left")

    date_label = app_window.create_label(nav_frame, text=selected_date.strftime('%d/%m/%Y'),
                                         font=("Times New Roman", 16), bg=BEIGE_COLOR, fg=BLACK_COLOR)
    date_label.pack(side="left")
    state["date_label"] = date_label

    app_window.create_button(nav_frame, "Següent ▶", command=go_next, font=("Times New Roman", 12),
                             bg=BROWN_COLOR, fg=METAL_GOLD_COLOR, highlightbackground=BEIGE_COLOR, width=8).pack(side="left")

    app_window.create_button(nav_frame, "Avui", command=go_today, font=("Times New Roman", 12),
                             bg=BROWN_COLOR, fg=METAL_GOLD_COLOR, highlightbackground=BEIGE_COLOR, width=8).pack(side="left")

    nav_frame.pack()

    info_frame = app_window.create_frame(frame, bg=BEIGE_COLOR)
    canvas = tk.Canvas(info_frame, bg=BEIGE_COLOR, width=300, height=400,
                       highlightthickness=2, highlightbackground=BROWN_COLOR)
    scrollbar = tk.Scrollbar(info_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    state["canvas"] = canvas

    content_frame = app_window.create_frame(canvas, bg=BEIGE_COLOR)
    canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")
    state["content_frame"] = content_frame

    def configure_scroll(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def configure_canvas(event):
        canvas.itemconfig(canvas_window, width=event.width - 10)

    content_frame.bind("<Configure>", configure_scroll)
    canvas.bind("<Configure>", configure_canvas)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    info_frame.pack(fill="both", expand=True)

    update_display(state)

    frame_manager.register_frame("history_navigator", frame)

    return frame
