from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'segredo_123'  # necessário para usar sessões


def gerar_pergunta():
    """Gera uma pergunta com números de 1 a 10 e resultado positivo dentro da tabuada"""
    operadores = ['+', '-', '*', '/']
    operador_correto = random.choice(operadores)

    # Garante que todos os valores e resultados fiquem entre 1 e 10
    if operador_correto == '+':
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        resultado = num1 + num2
        # Se o resultado passar de 10, gera novamente
        while resultado > 10:
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            resultado = num1 + num2

    elif operador_correto == '-':
        num1 = random.randint(1, 10)
        num2 = random.randint(1, num1)  # evita negativo
        resultado = num1 - num2

    elif operador_correto == '*':
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        resultado = num1 * num2
        # Evita resultados maiores que 10
        while resultado > 10:
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            resultado = num1 * num2

    elif operador_correto == '/':
        # Garante divisão exata e resultado de 1 a 10
        resultado = random.randint(1, 10)
        num2 = random.randint(1, 10)
        num1 = resultado * num2
        # Se passar de 10, gera novamente
        while num1 > 10 or num2 > 10:
            resultado = random.randint(1, 10)
            num2 = random.randint(1, 10)
            num1 = resultado * num2

    # Embaralha as opções
    opcoes = ['+', '-', '*', '/']
    random.shuffle(opcoes)

    return {
        'num1': num1,
        'num2': num2,
        'resultado': resultado,
        'correto': operador_correto,
        'opcoes': opcoes
    }


@app.route('/')
def index():
    # Inicializa o jogo
    if 'acertos' not in session:
        session['acertos'] = 0
        session['erros'] = 0
        session['pergunta'] = 1
        session['pergunta_atual'] = gerar_pergunta()

    return render_template('index.html',
                           pergunta=session['pergunta_atual'],
                           num_pergunta=session['pergunta'],
                           acertos=session['acertos'],
                           erros=session['erros'],
                           mensagem=None)


@app.route('/responder', methods=['POST'])
def responder():
    resposta = request.form.get('operador')
    correto = session['pergunta_atual']['correto']

    if resposta == correto:
        session['acertos'] += 1
        mensagem = "✅ Correto! Você acertou!"
    else:
        session['erros'] += 1
        mensagem = f"❌ Errado! A resposta certa era '{correto}'."

    session['pergunta'] += 1

    # Se terminar o jogo
    if session['pergunta'] > 10:
        return render_template('fim.html',
                               acertos=session['acertos'],
                               erros=session['erros'])

    # Gera nova pergunta
    session['pergunta_atual'] = gerar_pergunta()

    return render_template('index.html',
                           pergunta=session['pergunta_atual'],
                           num_pergunta=session['pergunta'],
                           acertos=session['acertos'],
                           erros=session['erros'],
                           mensagem=mensagem)


@app.route('/reiniciar')
def reiniciar():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

