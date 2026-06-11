from flask import Flask, render_template, request, redirect, url_for, flash
from negocio.modelos import QuartoStandard, QuartoVIP, QuartoPresidencial, Reserva, Spa, Lavanderia, Frigobar, CamaExtra, TaxaPet, CafeDaManha
from negocio.gerenciador import GerenciadorDeReservas, NotificadorEmail
from dados.repositorio import BancoEmMemoria, BancoPersistente
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hotel_secreto_123' # Necessário para exibir alertas na tela

# Instanciamos o banco e o gerenciador uma única vez ao ligar o servidor
banco_dados = BancoPersistente()
metodo_notificacao = NotificadorEmail()
gerenciador = GerenciadorDeReservas(repositorio=banco_dados, notificador=metodo_notificacao)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        
        # Captura dos novos campos
        rua = request.form.get('rua')
        numero = request.form.get('numero')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')
        cep = request.form.get('cep')
        
        str_entrada = request.form.get('data_entrada')
        str_saida = request.form.get('data_saida')
        
        data_entrada = datetime.strptime(str_entrada, '%Y-%m-%d').date()
        data_saida = datetime.strptime(str_saida, '%Y-%m-%d').date()
        
        if data_saida <= data_entrada:
            flash('❌ A data de saída deve ser posterior à data de entrada!', 'danger')
            return redirect(url_for('checkin'))
        
        numero_quarto = request.form.get('numero_quarto')
        
        quarto = gerenciador.validar_quarto(numero_quarto)
        
        if not quarto:
            flash(f'❌ O quarto {numero_quarto} não existe no catálogo do hotel!', 'danger')
            return redirect(url_for('checkin'))
        
        reserva = Reserva(hospede=nome, email=email, telefone=telefone, 
                          rua=rua, numero=numero, bairro=bairro, cidade=cidade, cep=cep,
                          quarto=quarto, data_entrada=data_entrada, data_saida=data_saida)
        
        servicos = request.form.getlist('servicos')
        if 'spa' in servicos: reserva.adicionar_servico(Spa())
        if 'lavanderia' in servicos: reserva.adicionar_servico(Lavanderia())
        if 'cama_extra' in servicos: reserva.adicionar_servico(CamaExtra())
        if 'taxa_pet' in servicos: reserva.adicionar_servico(TaxaPet())
        if 'cafe_manha' in servicos: reserva.adicionar_servico(CafeDaManha())
        
        codigo = gerenciador.realizar_checkin(reserva)
        
        # A tela avalia o que o gerenciador respondeu:
        if codigo is None:
            flash(f'❌ ERRO: O quarto {numero_quarto} já está ocupado por outro hóspede!', 'danger')
            return redirect(url_for('checkin'))
            
        flash(f'✅ Check-in aprovado! Quarto {codigo} liberado para {nome}.', 'success')
        return redirect(url_for('index'))
        
    return render_template('checkin.html')

@app.route('/consumo', methods=['GET', 'POST'])
def consumo():
    if request.method == 'POST':
        codigo = request.form.get('codigo').upper()
        tipo_servico = request.form.get('servico')
        
        svc = None
        if tipo_servico == '1': svc = Frigobar()
        elif tipo_servico == '2': svc = Lavanderia()
        elif tipo_servico == '3': svc = Spa()
        
        if gerenciador.registrar_consumo(codigo, svc):
            flash(f'✅ Consumo registrado na ficha {codigo} com sucesso!', 'success')
        else:
            flash('❌ Erro: Código de reserva não encontrado.', 'danger')
        return redirect(url_for('index'))
        
    # --- NOVO: Pega a lista antes de renderizar a tela ---
    reservas_ativas = gerenciador.listar_reservas_ativas()
    return render_template('consumo.html', reservas=reservas_ativas)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    extrato = None
    if request.method == 'POST':
        codigo = request.form.get('codigo').upper()
        extrato = gerenciador.realizar_checkout(codigo)
        if not extrato:
            flash('❌ Erro: Código de reserva não encontrado ou já encerrado.', 'danger')
            
    # --- NOVO: Pega a lista antes de renderizar a tela ---
    reservas_ativas = gerenciador.listar_reservas_ativas()
    return render_template('checkout.html', extrato=extrato, reservas=reservas_ativas)

@app.route('/remover_consumo', methods=['POST'])
def remover_consumo():
    codigo = request.form.get('codigo').upper()
    index = int(request.form.get('index'))
    
    # Busca a reserva no repositório persistente ou em memória
    reserva = gerenciador.repositorio.buscar(codigo)
    
    if reserva and 0 <= index < len(reserva.servicos):
        # Remove o serviço pela posição dele na lista
        reserva.servicos.pop(index)
        
        # O repositório salva o estado atualizado da reserva
        gerenciador.repositorio.salvar(codigo, reserva)
        return 'OK', 200
        
    return 'Erro', 400

if __name__ == '__main__':
    app.run(debug=True)


