from abc import ABC, abstractmethod
from negocio.modelos import Reserva, QuartoStandard, QuartoVIP, QuartoPresidencial
from dados.repositorio import RepositorioReservas
from threading import Lock

class Notificador(ABC):
    @abstractmethod
    def enviar(self, mensagem: str):
        pass

class NotificadorEmail(Notificador):
    def enviar(self, mensagem: str):
        print(f"[EMAIL ENVIADO]: {mensagem}")

class GerenciadorDeReservas:
    def __init__(self, repositorio: RepositorioReservas, notificador: Notificador):
        self.repositorio = repositorio
        self.notificador = notificador

        self.trava_de_acesso = Lock()
        
        self.inventario_quartos = {
                "101": QuartoStandard(numero="101"),
                "102": QuartoStandard(numero="102"),
                "103": QuartoStandard(numero="103"),
                "104": QuartoStandard(numero="104"),
                "201": QuartoVIP(numero="201"),
                "202": QuartoVIP(numero="202"),
                "203": QuartoVIP(numero="203"),
                "301": QuartoPresidencial(numero="301"),
                "302": QuartoPresidencial(numero="302")
            }    

    def gerar_extrato(self, reserva: Reserva) -> str:
        linhas = []
        linhas.append(f"--- EXTRATO DETALHADO ---")
        linhas.append(f"Cliente: {reserva.hospede}")
        linhas.append(f"Contato: {reserva.email} | {reserva.telefone}")
        endereco_completo = f"{reserva.rua}, {reserva.numero} - {reserva.bairro}, {reserva.cidade} - CEP: {reserva.cep}"
        linhas.append(f"Endereço: {endereco_completo}")
        linhas.append(f"Período: {reserva.data_entrada.strftime('%d/%m/%Y')} a {reserva.data_saida.strftime('%d/%m/%Y')} ({reserva.dias} dias)")
        
        valor_base = reserva.quarto.calcular_diaria() * reserva.dias
        dias_antecedencia = (reserva.data_entrada - reserva.data_reserva).days
        
        linhas.append(f"Diárias (Base): R$ {valor_base:.2f}")
        
        if dias_antecedencia >= 90:
            linhas.append(f"Desconto Antecedência (15%): - R$ {(valor_base * 0.15):.2f}")

        if reserva.servicos:
            linhas.append("Serviços Consumidos:")
            for servico in reserva.servicos:
                linhas.append(f"  - {servico.__class__.__name__}: R$ {servico.calcular_servico():.2f}")
        
        total = self.calcular_total(reserva)
        linhas.append(f"-------------------------")
        linhas.append(f"TOTAL GERAL: R$ {total:.2f}")
        
        return "\n".join(linhas)
    
    def validar_quarto(self, numero: str):
        return self.inventario_quartos.get(numero)

    def realizar_checkin(self, reserva: Reserva) -> str:
        codigo = reserva.quarto.numero 
        
        with self.trava_de_acesso:
            quarto_ocupado = self.repositorio.buscar(codigo)
            
            if quarto_ocupado:
            
                return None 
            
            self.repositorio.salvar(codigo, reserva)
        
        extrato = self.gerar_extrato(reserva)
        self.notificador.enviar(f"Olá {reserva.hospede}, sua reserva para o quarto {codigo} foi confirmada!\n{extrato}")
        
        return codigo

    def registrar_consumo(self, codigo: str, servico) -> bool:
        reserva = self.repositorio.buscar(codigo)
        if reserva:
            reserva.adicionar_servico(servico)
            self.repositorio.salvar(codigo, reserva)
            return True
        return False

    def calcular_total(self, reserva: Reserva) -> float:
        valor_base = reserva.quarto.calcular_diaria() * reserva.dias
        
        dias_antecedencia = (reserva.data_entrada - reserva.data_reserva).days
        if dias_antecedencia >= 90:
            valor_diarias_final = valor_base * 0.85 
        else:
            valor_diarias_final = valor_base 
            
        total = valor_diarias_final
        for servico in reserva.servicos:
            total += servico.calcular_servico()
        return total
    
    def listar_reservas_ativas(self) -> dict:
        return self.repositorio.listar_todos()

    def realizar_checkout(self, codigo: str) -> dict:
        reserva = self.repositorio.buscar(codigo)
        if not reserva:
            return None
        
        extrato = self.gerar_extrato(reserva)
        self.repositorio.remover(codigo)
        
        self.notificador.enviar(f"Obrigado por se hospedar, {reserva.hospede}! Volte sempre.\n{extrato}")
        
        return extrato