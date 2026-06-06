import os
import pickle
from abc import ABC, abstractmethod

class RepositorioReservas(ABC):
    @abstractmethod
    def salvar(self, codigo: str, reserva): pass

    @abstractmethod
    def buscar(self, codigo: str): pass

    @abstractmethod
    def remover(self, codigo: str): pass

    @abstractmethod
    def listar_todos(self) -> dict: pass

class BancoEmMemoria(RepositorioReservas):
    def __init__(self):
        self.tabela_reservas = {}

    def salvar(self, codigo: str, reserva):
        self.tabela_reservas[codigo] = reserva

    def buscar(self, codigo: str):
        return self.tabela_reservas.get(codigo)

    def remover(self, codigo: str):
        if codigo in self.tabela_reservas:
            del self.tabela_reservas[codigo]

    def listar_todos(self) -> dict:
        return self.tabela_reservas

class BancoPersistente(RepositorioReservas):
    def __init__(self, arquivo='banco_hotel.pkl'):
        self.arquivo = arquivo
        self.tabela_reservas = {}
        self._carregar_banco()

    def _carregar_banco(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'rb') as f:
                self.tabela_reservas = pickle.load(f)

    def _salvar_arquivo(self):
        with open(self.arquivo, 'wb') as f:
            pickle.dump(self.tabela_reservas, f)

    def salvar(self, codigo: str, reserva):
        self.tabela_reservas[codigo] = reserva
        self._salvar_arquivo()

    def buscar(self, codigo: str):
        return self.tabela_reservas.get(codigo)

    def remover(self, codigo: str):
        if codigo in self.tabela_reservas:
            del self.tabela_reservas[codigo]
            self._salvar_arquivo()

    def listar_todos(self) -> dict:
        return self.tabela_reservas