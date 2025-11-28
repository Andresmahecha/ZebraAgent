# 🐍 Zebra ZPL Agent  
Agente local para impresión ZPL en impresoras Zebra desde aplicaciones web o de escritorio.

Este agente se ejecuta en Windows, escucha peticiones HTTP en `127.0.0.1:9123` y envía comandos ZPL directamente a la impresora usando **RAW printing**.

Incluye:
- Servidor local con **Waitress** (producción)
- API Flask minimalista
- Interfaz gráfica con **PySide6**
- Icono en bandeja (system tray) con **pystray**
- Ejecución en segundo plano
- Integración con PyInstaller para empaquetar en un `.exe`

---

## 🚀 Características

- Listado de impresoras instaladas (Windows)
- Envío de comandos ZPL directamente a la impresora
- GUI liviana con opción para minimizar a bandeja
- Cierre limpio desde el menú del tray
- Servidor WSGI con Waitress (sin warnings de desarrollo)
- Compatible con Windows 10/11
- Pensado para distribuciones empresariales

---

## 📦 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/Andresmahecha/ZebraAgent.git
cd ZebraAgent
