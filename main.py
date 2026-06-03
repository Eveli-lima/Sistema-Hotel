import os
from negocio.modelos import QuartoStandard, QuartoVIP, QuartoPresidencial, Reserva, Spa, Lavanderia, Frigobar
from negocio.gerenciador import GerenciadorDeReservas, NotificadorEmail
from dados.repositorio import BancoEmMemoria

# --- PALETA DE CORES ANSI ---
RESET = '\033[0m'
BOLD = '\033[1m'
VERDE = '\033[92m'
VERMELHO = '\033[91m'
CIANO = '\033[96m'
AMARELO = '\033[93m'
AZUL = '\033[94m'

def limpar_tela():
    """Limpa o terminal dependendo do sistema operacional (Windows ou Linux/Mac)"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    """Pausa a tela para o usuário ler as mensagens antes de limpar tudo"""
    input(f"\n{AMARELO}[Pressione ENTER para voltar ao Menu Principal...]{RESET}")

if __name__ == "__main__":
    # Injeção de Dependências
    banco_dados = BancoEmMemoria()
    metodo_notificacao = NotificadorEmail()
    gerenciador = GerenciadorDeReservas(repositorio=banco_dados, notificador=metodo_notificacao)

    while True:
        limpar_tela()
        
        # --- CABEÇALHO DO MENU ---
        print(f"{CIANO}{BOLD}╔══════════════════════════════════════════════╗")
        print(f"║            🏨 HOTEL DA SERRA - ERP           ║")
        print(f"╚══════════════════════════════════════════════╝{RESET}")
        print(f"\n{BOLD}O que você deseja fazer hoje?{RESET}\n")
        
        print(f"  [{CIANO}1{RESET}] Fazer Check-in (Nova Reserva)")
        print(f"  [{CIANO}2{RESET}] Lançar Consumo / Serviços Extras")
        print(f"  [{CIANO}3{RESET}] Fazer Check-out (Encerrar e Pagar)")
        print(f"  [{VERMELHO}0{RESET}] Sair do Sistema")
        
        print(f"\n{CIANO}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
        opcao = input(f"{BOLD}Escolha uma opção:{RESET} ")
        
        if opcao == "0":
            limpar_tela()
            print(f"\n{VERDE}{BOLD}Sistema encerrado. Até logo! 👋{RESET}\n")
            break
            
        # ... (código anterior do main.py)

        elif opcao == "1":
            limpar_tela()
            print(f"{AZUL}{BOLD}─── NOVO CHECK-IN ──────────────────────────────{RESET}\n")
            
            nome = input(f"👤 {BOLD}Nome do hóspede:{RESET} ")
            dias = int(input(f"📅 {BOLD}Dias de estadia:{RESET} "))
            
            print(f"\n{AZUL}Tipos de Acomodação:{RESET}")
            print(f"  [{CIANO}1{RESET}] Standard     (R$ 150,00/dia)")
            print(f"  [{CIANO}2{RESET}] VIP          (R$ 200,00/dia)")
            print(f"  [{CIANO}3{RESET}] Presidencial (R$ 300,00/dia)")
            
            esc_quarto = input(f"\n{BOLD}Escolha o quarto:{RESET} ")
            
            if esc_quarto == "1": quarto = QuartoStandard()
            elif esc_quarto == "2": quarto = QuartoVIP()
            elif esc_quarto == "3": quarto = QuartoPresidencial()
            else: 
                print(f"\n{VERMELHO}❌ Quarto inválido. Operação cancelada.{RESET}")
                pausar()
                continue

            reserva = Reserva(hospede=nome, quarto=quarto, dias=dias)
            
            # --- O NOVO LAÇO DE SERVIÇOS DO CHECK-IN ---
            print(f"\n{AZUL}Serviços de Entrada Antecipada:{RESET}")
            while True:
                print(f"  [{CIANO}1{RESET}] Spa (R$ 150) | [{CIANO}2{RESET}] Lavanderia (R$ 80) | [{VERMELHO}0{RESET}] Concluir")
                esc_svc = input(f"\n{BOLD}Adicionar algum?{RESET} ")
                
                if esc_svc == "0":
                    break # Só sai quando digita 0
                elif esc_svc == "1": 
                    reserva.adicionar_servico(Spa())
                    print(f"{VERDE}✅ Spa adicionado!{RESET}")
                elif esc_svc == "2": 
                    reserva.adicionar_servico(Lavanderia())
                    print(f"{VERDE}✅ Lavanderia adicionada!{RESET}")
                else:
                    print(f"{VERMELHO}❌ Opção inválida.{RESET}")

            print("\nProcessando reserva...")
            codigo = gerenciador.realizar_checkin(reserva)
            
            print(f"\n{VERDE}╔══════════════════════════════════════════╗")
            print(f"║ ✅ CHECK-IN APROVADO COM SUCESSO!        ║")
            print(f"║ 🏷️ CÓDIGO DA RESERVA: {BOLD}{codigo:<18}{RESET}{VERDE} ║")
            print(f"╚══════════════════════════════════════════╝{RESET}")
            
            pausar()
            
        elif opcao == "2":
            limpar_tela()
            print(f"{AZUL}{BOLD}─── LANÇAMENTO DE CONSUMO ──────────────────────{RESET}\n")
            
            cod = input(f"🏷️  {BOLD}Digite o CÓDIGO da reserva:{RESET} ").upper()
            
            # --- O NOVO LAÇO DE SERVIÇOS AVULSOS ---
            while True:
                print(f"\n{AZUL}Catálogo de Serviços Extras:{RESET}")
                print(f"  [{CIANO}1{RESET}] Frigobar   (R$  50,00)")
                print(f"  [{CIANO}2{RESET}] Lavanderia (R$  80,00)")
                print(f"  [{CIANO}3{RESET}] Spa        (R$ 150,00)")
                print(f"  [{VERMELHO}0{RESET}] Finalizar lançamentos")
                
                esc_svc = input(f"\n{BOLD}O que o hóspede consumiu?{RESET} ")
                
                if esc_svc == "0":
                    break # Só sai quando digita 0
                    
                svc = None
                if esc_svc == "1": svc = Frigobar()
                elif esc_svc == "2": svc = Lavanderia()
                elif esc_svc == "3": svc = Spa()
                
                if svc:
                    if gerenciador.registrar_consumo(cod, svc):
                        print(f"{VERDE}✅ Consumo registrado na ficha ({cod}) com sucesso!{RESET}")
                    else:
                        print(f"{VERMELHO}❌ Erro: Reserva não encontrada.{RESET}")
                        break # Se errou o código, sai do laço
                else:
                    print(f"{VERMELHO}❌ Opção inválida! Tente novamente.{RESET}")
                
            pausar()

        elif opcao == "3":
            limpar_tela()
            print(f"{AZUL}{BOLD}─── FECHAMENTO DE CONTA (CHECK-OUT) ────────────{RESET}\n")
            
            cod = input(f"🏷️  {BOLD}Digite o CÓDIGO da reserva:{RESET} ").upper()
            
            print("\nBuscando dados e calculando totais...\n")
            extrato = gerenciador.realizar_checkout(cod)
            
            if extrato:
                print(f"{VERDE}╔══════════════════════════════════════════╗")
                print(f"║ 🛎️  CHECK-OUT FINALIZADO                  ║")
                print(f"╠══════════════════════════════════════════╣{RESET}")
                
                # Imprime o extrato gerado limpo, direto do Negócio
                print(extrato) 
                
                print(f"{VERDE}╚══════════════════════════════════════════╝{RESET}")
            else:
                print(f"{VERMELHO}❌ Código de reserva não encontrado ou já encerrado.{RESET}")
                
            pausar()