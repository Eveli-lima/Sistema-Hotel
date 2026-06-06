from abc import ABC, abstractmethod
from datetime import date

# --- ACOMODAÇÕES (OCP) ---
class QuartoBase(ABC):
    def __init__(self, numero: str):
        self.numero = numero

    @abstractmethod
    def calcular_diaria(self) -> float:
        pass

    @abstractmethod
    def exibir_detalhes(self) -> str:
        pass
class QuartoStandard(QuartoBase):
    def calcular_diaria(self) -> float: return 150.00
    def exibir_detalhes(self): return "Quarto Standard: Cama casal, wi-fi e TV"

class QuartoVIP(QuartoBase):
    def calcular_diaria(self) -> float: return 200.00
    def exibir_detalhes(self): return "Quarto VIP: Cama King, banheira, piscina aquecida."

class QuartoPresidencial(QuartoBase):
    def calcular_diaria(self) -> float: return 300.00
    def exibir_detalhes(self): return "Quarto Presidencial: Cobertura, frigobar livre, vista."

# --- SERVIÇOS ADICIONAIS (OCP) ---
class ServicoBase(ABC):
    @abstractmethod
    def calcular_servico(self) -> float:
        pass

class Frigobar(ServicoBase):
    def calcular_servico(self) -> float: return 50.00

class Spa(ServicoBase):
    def calcular_servico(self) -> float: return 150.00

class Lavanderia(ServicoBase):
    def calcular_servico(self) -> float: return 80.00

# --- ENTIDADE PRINCIPAL ---
class Reserva:
    def __init__(self, hospede: str, email: str, telefone: str, 
                 rua: str, numero: str, bairro: str, cidade: str, cep: str,
                 quarto: QuartoBase, data_entrada: date, data_saida: date, data_reserva: date = None):
        self.hospede = hospede
        self.email = email
        self.telefone = telefone
        # Novos campos detalhados:
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep
        
        self.quarto = quarto
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.data_reserva = data_reserva or date.today() 
        self.servicos = []

    @property
    def dias(self) -> int:
        delta = self.data_saida - self.data_entrada
        return delta.days if delta.days > 0 else 1

    def adicionar_servico(self, servico: ServicoBase):
        self.servicos.append(servico)