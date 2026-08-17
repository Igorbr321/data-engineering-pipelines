"""
Pacote comum contendo módulos de autenticação, conexão com DW e utilitários.
"""

# Versão do pacote common
__version__ = "0.1.0"

# Expor submódulos
from . import authenticator_hml
from . import authenticator_prd   
from . import utils

# API pública desse pacote
__all__ = [
    "__version__",
    "authenticator_hml",    # Funções de autenticação (login, logout, etc.)
    "authenticator_prd",      # Conexão com Data Warehouse (connect_dw)
    "utils",             # Utilitários gerais (init_logging, retries, CSV, etc.)
]