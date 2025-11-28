import sys
import os
import threading
import traceback

# ===========================
# FLASK / SERVIDOR DE IMPRESIÓN
# ===========================
from flask import Flask, request, jsonify
from flask_cors import CORS
import win32print

# ===========================
# GUI PySide6
# ===========================
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QObject, Signal

# ===========================
# Icono de bandeja
# ===========================
import pystray
from PIL import Image

# ===========================
# Servidor WSGI (producción)
# ===========================
from waitress import serve


# ============================================================
#  🔧 FUNCIONES PARA MANEJO DE RUTAS (PYINSTALLER COMPATIBLE)
# ============================================================
def resource_path(rel_path: str):
    """
    Devuelve la ruta correcta tanto cuando se ejecuta con Python
    como cuando está empaquetado como .EXE con PyInstaller.
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)


# Rutas de recursos
ICON_PATH = resource_path("agent/printer.ico")
LOG_FILE = resource_path("agent/agent_error.log")


# ============================================================
#  📄 LOGGING
# ============================================================
def log_error(text: str):
    """Escribe errores en un archivo log."""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except:
        pass


# ============================================================
#   🌐 SERVIDOR FLASK (API LOCAL)
# ============================================================
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.get("/health")
def health():
    return jsonify({"ok": True})


@app.get("/printers")
def printers():
    """Devuelve la lista de impresoras instaladas en Windows."""
    try:
        flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
        printers = win32print.EnumPrinters(flags)
        return jsonify({"success": True, "printers": [p[2] for p in printers]})
    except Exception:
        log_error(traceback.format_exc())
        return jsonify({"success": False})


@app.post("/print-zpl")
def print_zpl():
    """Envía un comando ZPL RAW directamente a la impresora."""
    try:
        data = request.get_json() or {}
        zpl = data.get("zpl")
        printer = data.get("printerName")

        if not zpl or not printer:
            return jsonify({"success": False, "error": "Faltan parámetros"}), 400

        hPrinter = win32print.OpenPrinter(printer)
        job_info = ("ZPLPrintJob", None, "RAW")

        win32print.StartDocPrinter(hPrinter, 1, job_info)
        win32print.StartPagePrinter(hPrinter)
        win32print.WritePrinter(hPrinter, zpl.encode())
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
        win32print.ClosePrinter(hPrinter)

        return jsonify({"success": True})
    except Exception:
        log_error(traceback.format_exc())
        return jsonify({"success": False}), 500


def run_flask():
    """Ejecuta Waitress como servidor de producción."""
    try:
        serve(app, host="127.0.0.1", port=9123, threads=4)
    except Exception as e:
        log_error(str(e))


# ============================================================
#   🔔 SEÑALES DE QT PARA EVENTOS DEL TRAY
# ============================================================
class TraySignals(QObject):
    quit_app = Signal()  # solo necesitamos salir


signals = TraySignals()


# ============================================================
#   🚪 SALIR DEL AGENTE
# ============================================================
def tray_force_exit():
    """Cierra bandeja, GUI y proceso completo."""
    TRAY.stop()
    QApplication.quit()
    os._exit(0)


# ============================================================
#   🖥 CALLBACK (solo salir)
# ============================================================
def tray_quit(icon, item):
    signals.quit_app.emit()


# Bandeja global
TRAY = None


def start_tray():
    """Inicia el icono de bandeja en un hilo separado."""
    global TRAY
    img = Image.open(ICON_PATH)

    TRAY = pystray.Icon(
        "ZebraZPLAgent",
        img,
        "Servidor de impresión Zebra - Dev Amahecha",
        menu=pystray.Menu(
            pystray.MenuItem("Salir", tray_quit)
        )
    )

    TRAY.run()


# ============================================================
#   🪟 VENTANA PRINCIPAL
# ============================================================
class AgentWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Servidor de impresión Zebra.")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setFixedSize(350, 150)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        layout = QVBoxLayout()

        label = QLabel("El servidor de impresión Zebra está ejecutándose.\nPuedes minimizarlo a la bandeja.")
        label.setAlignment(Qt.AlignCenter)

        btn = QPushButton("Minimizar a bandeja")
        btn.clicked.connect(self.hide)

        layout.addWidget(label)
        layout.addWidget(btn)

        self.setLayout(layout)


# ============================================================
#   🚀 MAIN
# ============================================================
if __name__ == "__main__":

    # Iniciar el servidor Waitress en background
    threading.Thread(target=run_flask, daemon=True).start()

    # Crear app Qt
    qt_app = QApplication(sys.argv)

    # Conectar señal de salida
    signals.quit_app.connect(tray_force_exit)

    # Mostrar ventana principal
    window = AgentWindow()
    window.show()

    # Iniciar icono de bandeja
    threading.Thread(target=start_tray, daemon=True).start()

    # Loop de Qt
    sys.exit(qt_app.exec())
