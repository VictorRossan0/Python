"""
Arquivo de configuração do pytest para testes Playwright.
Define fixtures globais e configurações compartilhadas.
"""

import pytest
import os


def pytest_configure(config):
    """Configuração inicial do pytest."""
    # Criar diretórios para reports se não existirem
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("videos", exist_ok=True)
    os.makedirs("traces", exist_ok=True)


# Configuração de markers customizados
def pytest_collection_modifyitems(config, items):
    """
    Modifica itens coletados para adicionar markers automáticos.
    """
    for item in items:
        # Adicionar marker 'slow' para testes que contenham 'slow' no nome
        if "slow" in item.name.lower() or hasattr(item.obj, "pytestmark"):
            for mark in getattr(item.obj, "pytestmark", []):
                if mark.name == "slow":
                    item.add_marker(pytest.mark.slow)


@pytest.fixture
def test_data():
    """Dados de teste comuns."""
    return {
        "valid_user": {
            "name": "João Silva",
            "email": "joao.silva@example.com",
            "phone": "11999999999",
            "address": "Rua das Flores, 123"
        },
        "invalid_user": {
            "name": "",
            "email": "email_invalido",
            "phone": "abc",
            "address": ""
        }
    }
