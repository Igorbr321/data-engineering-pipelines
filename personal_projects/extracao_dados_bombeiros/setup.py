import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "ttkbootstrap", "tkinter", "requests", "bs4", "csv"],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable('interface_grafica.py', base=base),
]

setup(
    name="ProjetoBombeiros",
    version="0.1",
    description="Extrai informações do Site de Bombeiros e gera CSV via interface gráfica.",
    options={"build_exe": build_exe_options},
    executables=executables
)

