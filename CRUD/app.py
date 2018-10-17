#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://flask.pocoo.org/docs/1.0/tutorial/
# g  is a special object that is unique for each request.
# It is used to store data that might be accessed by multiple functions during the request.
from flask import (
    flash, g, redirect, render_template, request, session, url_for, Flask
)

# https://dev.mysql.com/doc/connector-python/en/connector-python-introduction.html
from mysql.connector import MySQLConnection, Error
from time import strftime, time, sleep
from sched import scheduler
import threading
import time

db_config = {
    'user': 'admin',
    'password': 'pj129008',
    'host': 'nuvem.sj.ifsc.edu.br',
    'port':'30003',
    'database': 'database',
    'raise_on_warnings': True,
}

SECRET_KEY = 'aula de BCD - string aleatória'

app = Flask(__name__)

app.secret_key = SECRET_KEY

def print_time():
    print('Time: %s' % strftime("%Hh%Mmin%Ss"))

def print_and_schedule():
    sch = scheduler(timefunc=time, delayfunc=sleep)
    print_time()
    sch.enter(5, 0, print_time, ())
    sch.run()

irreg = None
error = None

def verificaIrreg(message):

    global irreg
    with app.app_context():
        while 1:
            time.sleep(30)
            print(message)

            try:
                    g.db = MySQLConnection(**db_config)
                    cursor = g.db.cursor(prepared=True)

                    consulta = "SELECT *,TIMEDIFF(Hora_fim,Hora_inicio) AS horas FROM Utiliza WHERE TIMEDIFF(Hora_fim,Hora_inicio)>(4*10000)"
                    print("Realizando consulta...  :")
                    cursor.execute(consulta)
                    rows = cursor.fetchall()

                    for r in rows:
                        print("Irregularidade detectada!!!!")
                        sec = r[6]
                        if (sec.seconds*3600) > 4:
                            irreg = "Irregularidade detectada!"

                    cursor.close()
                    g.db.close()
            except Exception as e:
                    print("Tratando exceção...  :")
                    print(str(e))

t = threading.Thread(target=verificaIrreg, args=("Verificando Irregularidades...",))
t.daemon = True
t.start()

@app.route('/')
def main():
    print_time()
    #session.logged_in = True

    return render_template('index.html')

@app.route('/Funcionario')
def Funcionario():
    if irreg:
        flash("Irregularidade detectada!")
    return render_template('Funcionario.html', title='Funcionario', error=error)

@app.route('/Irregularidades')
def Irregularidades():
    return render_template('Irregularidades.html', title='Irregularidades')

@app.route('/About')
def About():
    return render_template('About.html', title='About')

@app.route('/insereFuncionario', methods=('GET', 'POST'))
def insereFuncionario():
    RE = request.form;
    if request.method == 'POST':
        dados = (RE['Nome'],
                 RE['Sobrenome'],
                 RE['CPF'],
                 RE['RG'],
                 RE['DataNascimento'],
                 RE['Endereco'],
                 RE['Sexo'],
                 RE['data_admissao'])
        if (RE['Nome']=='' or RE['Sobrenome']=='' or RE['CPF']=='' or RE['RG']=='' or RE['DataNascimento']=='' or RE['Endereco']=='' or RE['Sexo']=='' or RE['data_admissao']==''):
            print("Todos os parâmetros devem ser preenchidos")
        # else:
        try:
            g.db = MySQLConnection(**db_config)
            cursor = g.db.cursor()

            if (request.form['DataNascimento'] > request.form['data_admissao']):
                    print("Data de Nascimento > Data Admissão")
            else:
                consulta = "INSERT INTO Funcionario(Nome,Sobrenome,CPF,RG,DataNascimento,Endereco,Sexo,data_admissao) " \
                           "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(consulta, dados)
                g.db.commit()
                cursor.close()
                g.db.close()

        except Exception as e:
            return (str(e))
        return render_template('Funcionario.html')

    return render_template('insereFuncionario.html', title='Insere')

@app.route('/removeFuncionario', methods=('GET', 'POST'))
def removeFuncionario():
    error = None
    if request.method == 'POST':
        nome = request.form['Nome']
        sobrenome = request.form['Sobrenome']
        data = request.form['data_demissao']

        try:
            g.db = MySQLConnection(**db_config)
            cursor = g.db.cursor()
            consulta1 = "SELECT * FROM Funcionario WHERE Nome=(%s) AND Sobrenome=(%s)"
            cursor.execute(consulta1, (nome, sobrenome))

            rows = cursor.fetchall()
            for r in rows:
                print(r)

            if cursor:
                try:
                    cursor = g.db.cursor(prepared=True)
                    consulta = "UPDATE Funcionario SET data_demissao:=(%s) WHERE Nome=(%s) AND Sobrenome=(%s)"

                    cursor.execute(consulta,(data, nome, sobrenome))
                    g.db.commit()
                    cursor.close()
                    g.db.close()
                    return render_template('Funcionario.html')
                except:
                    return render_template('removeFuncionario.html', title='removeFuncionario')
            else:
                cursor.close()
                g.db.close()
                return render_template('removeFuncionario.html', title='removeFuncionario')


        except Exception as e:
            # return (str(e))
            return render_template('removeFuncionario.html', title='removeFuncionario', error=e)

    return render_template('removeFuncionario.html', title='removeFuncionario')

@app.route('/irregularidadeFuncionario', methods=('GET', 'POST'))
def irregularidadeFuncionario():
    if error:
        flash("Irregularidade detectada!")
    objetos = []

    try:
        g.db = MySQLConnection(**db_config)
        cursor = g.db.cursor(prepared=True)

        consulta = "SELECT *,TIMEDIFF(Hora_fim,Hora_inicio) AS horas FROM Utiliza WHERE TIMEDIFF(Hora_fim,Hora_inicio)>(4*10000)"
        cursor.execute(consulta)
        for (ID, Hora_inicio, Hora_fim, Funcionario_ID, Bancada_ID, Bancada_Sala_ID, horas) in cursor:
            objetos.append(
                {'id': ID, 'inicio': Hora_inicio, 'fim': Hora_fim, 'id_func': Funcionario_ID,
                 'id_banc': Bancada_ID, 'id_sala': Bancada_Sala_ID, 'horas': horas})

        cursor.close()
        g.db.close()
    except Exception as e:
        print(str(e))

    return render_template('irregularidadeFuncionario.html', title='irregularidadeFuncionario', irregularidades=objetos, error=error)

@app.route('/listarFuncionario', methods=('GET', 'POST'))
def listarFuncionario():

    Funcionario = []

    g.db = MySQLConnection(**db_config)
    cursor = g.db.cursor()

  query = "SELECT ID,Nome,Sobrenome,CPF,RG,date_format(DataNascimento,'%d/%m/%y'),Endereco,Sexo,date_format(data_admissao,'%d/%m/%y'),date_format(data_demissao,'%d/%m/%y') FROM Funcionario"


    cursor.execute(query)
    for (ID, Nome,Sobrenome,CPF,RG,DataNascimento,Endereco,Sexo,data_admissao,data_demissao) in cursor:
        print(Nome)
        Funcionario.append({'ID': ID, 'Nome': Nome, 'Sobrenome': Sobrenome, 'CPF': CPF, 'RG': RG, 'DataNascimento': DataNascimento, 'Endereco': Endereco,'Sexo': Sexo, 'data_admissao': data_admissao, 'data_demissao':data_demissao })

    cursor.close()
    g.db.close()
    session['Funcionario'] = Funcionario

    return render_template('listarFuncionario.html', title='Listar funcionários', Funcionario=Funcionario, error=error)


@app.route('/atualizaFuncionario', methods=('GET', 'POST'))
def atualizaFuncionario():
    if request.method == 'GET':
        ID = str(request.args.get('ID'))

        for f in session['Funcionario']:
            if str(f['ID']) == ID:
                session['func'] = f
                return render_template('atualizaFuncionario.html', title='atualizaFuncionario')

        return render_template('atualizaFuncionario.html', title='atualizaFuncionario')

    else:
        dados = (request.form['Nome'],
                 request.form['Sobrenome'],
                 request.form['CPF'],
                 request.form['RG'],
                 request.form['DataNascimento'],
                 request.form['Endereco'],
                 request.form['Sexo'],
                 request.form['data_admissao'],
                 str(session['func']['ID']))

        try:
            g.db = MySQLConnection(**db_config)
            cursor = g.db.cursor(prepared=True)
            consulta = "UPDATE Funcionario SET Nome:=(%s), Sobrenome:=(%s),CPF:=(%s),RG:=(%s),DataNascimento:=(%s)," \
                        "Endereco:=(%s),Sexo:=(%s),data_admissao:=(%s) WHERE ID=(%s)"

            cursor.execute(consulta, dados)
            g.db.commit()
            cursor.close()
            g.db.close()
            return redirect(url_for('listarFuncionario'))

        except Exception as e:
            return (str(e))

@app.route('/Ativos', methods=('GET', 'POST'))
def Ativos():

    Funcionario = []

    g.db = MySQLConnection(**db_config)
    cursor = g.db.cursor()

    query = "SELECT ID,Nome,Sobrenome,CPF,RG,DataNascimento,Endereco,Sexo,data_admissao FROM Funcionario where data_demissao is null"

    cursor.execute(query)
    for (ID, Nome,Sobrenome,CPF,RG,DataNascimento,Endereco,Sexo,data_admissao) in cursor:
        print(Nome)
        Funcionario.append({'ID': ID, 'Nome': Nome, 'Sobrenome': Sobrenome, 'CPF': CPF, 'RG': RG, 'DataNascimento': DataNascimento, 'Endereco': Endereco,'Sexo': Sexo, 'data_admissao': data_admissao })

    cursor.close()
    g.db.close()
    session['Funcionario'] = Funcionario

    return render_template('listarFuncionario.html', title='Pesquisa de funcionários - Ativos na empresa', Funcionario=Funcionario, error=error)

@app.route('/Inativos', methods=('GET', 'POST'))
def Inativos():

    Funcionario = []

    g.db = MySQLConnection(**db_config)
    cursor = g.db.cursor()

    query = "SELECT ID,Nome,Sobrenome,CPF,RG,DataNascimento,Endereco,Sexo,data_admissao,data_demissao FROM Funcionario where data_demissao is not null"

    cursor.execute(query)
    for (ID, Nome,Sobrenome,CPF,RG,DataNascimento,Endereco,Sexo,data_admissao,data_demissao) in cursor:
        print(Nome)
        Funcionario.append({'ID': ID, 'Nome': Nome, 'Sobrenome': Sobrenome, 'CPF': CPF, 'RG': RG, 'DataNascimento': DataNascimento, 'Endereco': Endereco,'Sexo': Sexo, 'data_admissao': data_admissao, 'data_demissao': data_demissao })

    cursor.close()
    g.db.close()
    session['Funcionario'] = Funcionario

    return render_template('listarFuncionario.html', title='Pesquisa de funcionários - Ativos na empresa', Funcionario=Funcionario, error=error)


@app.route('/Admitidos', methods=('GET', 'POST'))
def Admitidos():
    if request.method == 'GET':
        data_inicio = str(request.args.get('data_inicio'))

        for f in session['Funcionario']:
            if str(f['data_admissao']) >= data_inicio:
                session['func'] = f
                return render_template('Admitidos.html', title='Funcionários admitidos')

        return render_template('Admitidos.html', title='Funcionários admitidos')

    else:
        dados = (request.form['Nome'],
                 request.form['Sobrenome'],
                 request.form['CPF'],
                 request.form['RG'],
                 request.form['DataNascimento'],
                 request.form['Endereco'],
                 request.form['Sexo'],
                 request.form['data_admissao'],
                 str(session['func']['ID']))

        try:
            g.db = MySQLConnection(**db_config)
            cursor = g.db.cursor(prepared=True)
            consulta = "Select * from Funcionario WHERE data_admissao>=(%s) and data_demissao<=(%s)"

            cursor.execute(consulta, dados)
            g.db.commit()
            cursor.close()
            g.db.close()
            return redirect(url_for('listarFuncionario'), error=error)

        except Exception as e:
            return (str(e))



@app.route('/insereAdministrador', methods=('GET', 'POST'))
def insereAdministrador():
    if request.method == 'POST':
        dados = (request.form['ID'],
                 request.form['CPF'],
                 request.form['Senha'])

        g.db = MySQLConnection(**db_config)
        cursor = g.db.cursor()

        consulta = "INSERT INTO Administrador(ID,CPF,Senha) VALUES (%s,%s,%s);";
        cursor.execute(consulta, dados)
        g.db.commit()
        cursor.close()
        g.db.close()

        return redirect(url_for('/'))

    return render_template('insereAdministrador.html', title='Administrador')

@app.route('/insereCamera', methods=('GET', 'POST'))
def insereCamera():
    if request.method == 'POST':
        dados = (request.form['ID'],
                 request.form['IP'],
                 request.form['Modelo'],
                 request.form['Marca'],
                 request.form['Datasheet'],
                 request.form['Sala_ID'])

        g.db = MySQLConnection(**db_config)
        cursor = g.db.cursor()

        consulta = "INSERT INTO Camera(ID,IP,Modelo,Marca,Datasheet,Sala_ID) VALUES (%s,%s,%s,%s,%s,%s);"
        cursor.execute(consulta, dados)
        g.db.commit()
        cursor.close()
        g.db.close()

        return redirect(url_for('/'))

    return render_template('insereCamera.html', title='Camera')

@app.route('/utilizaBancada', methods=('GET', 'POST'))
def utilizaBancada():
    if request.method == 'POST':
        dados = (request.form['Hora_inicio'],
                 request.form['Hora_fim'],
                 request.form['Funcionario_ID'],
                 request.form['Bancada_ID'],
                 request.form['Bancada_Sala_ID'])

        g.db = MySQLConnection(**db_config)
        cursor = g.db.cursor()

        consulta = "INSERT INTO utiliza(Hora_inicio,Hora_fim,Funcionario_ID,Bancada_ID,Bancada_Sala_ID) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(consulta, dados)
        g.db.commit()
        cursor.close()
        g.db.close()

        return redirect(url_for('utilizaBancada'))

    return render_template('utilizaBancada.html', title='Utiliza bancada')

@app.route('/Sala')
def Sala():
    return render_template('Sala.html', title='Sala')

@app.route('/Bancada')
def Bancada():
    return render_template('Bancada.html', title='Bancada')

@app.route('/editar/', methods=('GET', 'POST'))
def editar():
    if request.method == 'GET':
        cid = str(request.args.get('id'))
        g.db = MySQLConnection(**db_config)
        cursor = g.db.cursor(prepared=True)
        consulta = ("SELECT nome, email FROM Contato WHERE cID = %s")
        cursor.execute(consulta, (cid))
        linha = cursor.fetchone()
        cursor.close()
        g.db.close()

        session['cid'] = cid
        return render_template('editar.html', title='Editar contato', contato=linha)

    else:
        cid = session['cid']
        nome = request.form['nome']
        email = request.form['email']
        session.pop('cid', None)

        g.db = MySQLConnection(**db_config)
        cursor = g.db.cursor(prepared=True)
        consulta = "UPDATE Contato SET nome = %s, email = %s WHERE cId = %s"
        dados = (nome, email, str(cid))
        cursor.execute(consulta, dados)
        g.db.commit()
        cursor.close()
        g.db.close()

        return redirect(url_for('listar'))

@app.route('/insereSala', methods=('GET', 'POST'))
def inserirSala():
    if request.method == 'POST':
        ID = request.form['ID']
        Nome = request.form['Nome']

        g.db = MySQLConnection(**db_config)
        cursor = g.db.cursor()
        consulta = "INSERT INTO Sala (ID,Nome,Ativo) VALUES (%s,%s,'1')"
        dados = (ID, Nome)
        cursor.execute(consulta, dados)
        g.db.commit()
        cursor.close()
        g.db.close()

        return redirect(url_for('Sala'))

    return render_template('insereSala.html', title='Adicionar Sala')

@app.route('/removeSala', methods=('GET', 'POST'))
def removeSala():
    error = None
    if request.method == 'GET':
        Funcionario = []

        g.db = MySQLConnection(**db_config)
        cursor = g.db.cursor()

        query = "SELECT ID,Nome,Sobrenome,CPF,RG,DataNascimento,Endereco,Sexo,data_admissao FROM Funcionario"

        cursor.execute(query)
        for (ID, Nome, Sobrenome, CPF, RG, DataNascimento, Endereco, Sexo, data_admissao) in cursor:
            print(Nome)
            Funcionario.append(
                {'ID': ID, 'Nome': Nome, 'Sobrenome': Sobrenome, 'CPF': CPF, 'RG': RG, 'DataNascimento': DataNascimento,
                 'Endereco': Endereco, 'Sexo': Sexo, 'data_admissao': data_admissao})

        cursor.close()
        g.db.close()
        session['Funcionario'] = Funcionario
    if request.method == 'POST':
        ID = request.form['ID']
        Nome = request.form['Nome']


        dados_demissao = (ID, Nome)
        try:
            g.db = MySQLConnection(**db_config)
            cursor = g.db.cursor()
            consulta1 = "SELECT * FROM Sala WHERE ID=(%s) AND Nome=(%s)"
            cursor.execute(consulta1, (ID, Nome))

            rows = cursor.fetchall()
            for r in rows:
                print(r)

            if cursor:
                try:
                    cursor = g.db.cursor(prepared=True)
                    consulta = "UPDATE Sala SET Ativo:='0' WHERE ID=(%s) AND Nome=(%s)"

                    cursor.execute(consulta,(ID, Nome))
                    g.db.commit()
                    cursor.close()
                    g.db.close()
                    return render_template('Sala.html')
                except:
                    return render_template('removeSala.html', title='removeSala')
            else:
                cursor.close()
                g.db.close()
                return render_template('removeSala.html', title='removeSala')


        except Exception as e:
            # return (str(e))
            return render_template('removeSala.html', title='removeSala', error=e)

    return render_template('removeSala.html', title='removeSala')

@app.route('/removeBancada', methods=('GET', 'POST'))
def removeBancada():
    error = None
    if request.method == 'POST':
        ID = request.form['ID']
        Tipo = request.form['Tipo']
        Ativo = request.form['Ativo']

        dados_demissao = (ID, Tipo, Ativo)
        try:
            g.db = MySQLConnection(**db_config)
            cursor = g.db.cursor()
            consulta1 = "SELECT * FROM bancada WHERE ID=(%s) AND Tipo=(%s)"
            cursor.execute(consulta1, (ID, Tipo))

            rows = cursor.fetchall()
            for r in rows:
                print(r)

            if cursor:
                try:
                    cursor = g.db.cursor(prepared=True)
                    consulta = "UPDATE bancada SET Ativo:=(%s) WHERE ID=(%s) AND Tipo=(%s)"

                    cursor.execute(consulta,(Ativo, ID, Tipo))
                    g.db.commit()
                    cursor.close()
                    g.db.close()
                    return render_template('Bancada.html')
                except:
                    return render_template('removeBancada.html', title='removeBancada')
            else:
                cursor.close()
                g.db.close()
                return render_template('removeBancada.html', title='removeBancada')


        except Exception as e:
            # return (str(e))
            return render_template('removeBancada.html', title='removeBancada', error=e)

    return render_template('removeBancada.html', title='removeBancada')

@app.route('/atualizaSala', methods=('GET', 'POST'))
def atualizaSala():
    if request.method == 'GET':
        ID = str(request.args.get('ID'))

        for f in session['Sala']:
            if str(f['ID']) == ID:
                session['func'] = f
                return render_template('atualizaSala.html', title='atualizaSala')

        return render_template('atualizaSala.html', title='atualizaSala')

    else:
        dados = (request.form['ID'],
                 request.form['Nome'])

        try:
            g.db = MySQLConnection(**db_config)
            cursor = g.db.cursor(prepared=True)
            consulta = "UPDATE Sala SET Nome:=(%s), Sobrenome:=(%s) WHERE ID=(%s)"

            cursor.execute(consulta, dados)
            g.db.commit()
            cursor.close()
            g.db.close()
            return redirect(url_for('listarSala'))

        except Exception as e:
            return (str(e))

@app.route('/historicoBancada', methods=('GET', 'POST'))
def historicoBancada():

    Bancada = []

    g.db = MySQLConnection(**db_config)
    cursor = g.db.cursor()

    query = "SELECT Hora_inicio, Hora_fim, Funcionario_ID, Bancada_ID, Bancada_Sala_ID FROM Utiliza"

    cursor.execute(query)
    for (Hora_inicio, Hora_fim, Funcionario_ID, Bancada_ID, Bancada_Sala_ID) in cursor:
        Bancada.append({'Hora_inicio': Hora_inicio, 'Hora_fim': Hora_fim, 'Funcionario_ID': Funcionario_ID, 'Bancada_ID': Bancada_ID, 'Bancada_Sala_ID':Bancada_Sala_ID})

    cursor.close()
    g.db.close()
    session['Bancada'] = Bancada

    return render_template('historicoBancada.html', title='Historico Bancada')

@app.route('/historicoSala', methods=('GET', 'POST'))
def historicoSala():

    Sala = []

    g.db = MySQLConnection(**db_config)
    cursor = g.db.cursor()

    query = "SELECT Hora_entrada, Hora_saida, Funcionario_ID, Sala_ID FROM Acessa"

    cursor.execute(query)
    for (Hora_entrada, Hora_saida, Funcionario_ID, Sala_ID) in cursor:
        Sala.append({'Hora_entrada': Hora_entrada, 'Hora_saida': Hora_saida, 'Funcionario_ID': Funcionario_ID, 'Sala_ID':Sala_ID})

    cursor.close()
    g.db.close()
    session['Sala'] = Sala

    return render_template('historicoSala.html', title='historicoSala')

@app.route('/atualizaBancada', methods=('GET', 'POST'))
def atualizaBancada():
    if request.method == 'GET':
        ID = str(request.args.get('ID'))

        for f in session['Bancada']:
            if str(f['ID']) == ID:
                session['func'] = f
                return render_template('atualizaBancada.html', title='atualizaBancada')

        return render_template('atualizaBancada.html', title='atualizaBancada')

    else:
        dados = (request.form['ID'],
                 request.form['Tipo'],
                 request.form['Sala_ID'],
                 request.form['Ativo'],
                 str(session['func']['ID']))

        try:
            g.db = MySQLConnection(**db_config)
            cursor = g.db.cursor(prepared=True)
            consulta = "UPDATE Funcionario SET Nome:=(%s), Sobrenome:=(%s),CPF:=(%s),RG:=(%s),DataNascimento:=(%s)," \
                        "Endereco:=(%s),Sexo:=(%s),data_admissao:=(%s) WHERE ID=(%s)"

            cursor.execute(consulta, dados)
            g.db.commit()
            cursor.close()
            g.db.close()
            return redirect(url_for('listarFuncionario'))

        except Exception as e:
            return (str(e))



@app.route('/Utilizar', methods=('GET', 'POST'))
def Utilizar():
    return render_template('Utilizar.html', title='Utilizar')

@app.route('/utilizaSala', methods=('GET', 'POST'))
def utilizaSala():
    if request.method == 'POST':
        dados = (request.form['Hora_entrada'],
                 request.form['Hora_saida'],
                 request.form['Funcionario_ID'],
                 request.form['Sala_ID'])

        g.db = MySQLConnection(**db_config)
        cursor = g.db.cursor()

        consulta = "INSERT INTO Acessa(Hora_entrada,Hora_saida,Funcionario_ID,Sala_ID) VALUES (%s,%s,%s,%s)"
        cursor.execute(consulta, dados)
        g.db.commit()
        cursor.close()
        g.db.close()

        return redirect(url_for('utilizaSala'))

    return render_template('utilizaSala.html', title='Utiliza Sala')


@app.route('/pi', methods=('GET', 'POST'))
def pi():
    return render_template('pi.html', title='pi')

@app.route('/listarSala', methods=('GET', 'POST'))
def listarSala():

    Sala = []

    g.db = MySQLConnection(**db_config)
    cursor = g.db.cursor()

    query = "SELECT * FROM Sala"

    cursor.execute(query)
    for (ID, Nome,Ativo) in cursor:
        Sala.append({'ID':ID,'Nome': Nome, 'Ativo': Ativo})

    cursor.close()
    g.db.close()

    return render_template('listarSala.html', title='listarSala', Sala=Sala)

@app.route('/SalaAtiva', methods=('GET', 'POST'))
def SalaAtiva():

    Sala = []

    g.db = MySQLConnection(**db_config)
    cursor = g.db.cursor()

    query = "SELECT * FROM Sala where Ativo=1"

    cursor.execute(query)
    for (ID, Nome,Ativo) in cursor:
        Sala.append({'ID':ID,'Nome': Nome, 'Ativo': 'Sim'})

    cursor.close()
    g.db.close()

    return render_template('listarSala.html', title='listarSala', Sala=Sala)

@app.route('/SalaInativa', methods=('GET', 'POST'))
def SalaInativa():

    Sala = []

    g.db = MySQLConnection(**db_config)
    cursor = g.db.cursor()

    query = "SELECT * FROM Sala where Ativo=0"

    cursor.execute(query)
    for (ID, Nome,Ativo) in cursor:
        Sala.append({'ID':ID,'Nome': Nome, 'Ativo': 'Não'})

    cursor.close()
    g.db.close()

    return render_template('listarSala.html', title='listarSala', Sala=Sala)


@app.route('/listarBancada', methods=('GET', 'POST'))
def listarBancada():

    Bancada = []

    g.db = MySQLConnection(**db_config)
    cursor = g.db.cursor()

    query = "SELECT * FROM Bancada"

    cursor.execute(query)
    for (ID, Tipo,Sala_ID,Ativo) in cursor:
        Bancada.append({'ID':ID,'Tipo': Tipo,'Sala_ID': Sala_ID, 'Ativo': Ativo})

    cursor.close()
    g.db.close()

    return render_template('listarBancada.html', title='listarBancada', Bancada=Bancada)

@app.route('/BancadaAtiva', methods=('GET', 'POST'))
def BancadaAtiva():

    Bancada = []

    g.db = MySQLConnection(**db_config)
    cursor = g.db.cursor()

    query = "SELECT * FROM Bancada where Ativo=1"

    cursor.execute(query)
    for (ID, Tipo,Sala_ID,Ativo) in cursor:
        Bancada.append({'ID':ID,'Tipo': Tipo,'Sala_ID': Sala_ID, 'Ativo': 'Sim'})

    cursor.close()
    g.db.close()

    return render_template('listarBancada.html', title='listarBancada', Bancada=Bancada)

@app.route('/BancadaInativa', methods=('GET', 'POST'))
def BancadaInativa():

    Bancada = []

    g.db = MySQLConnection(**db_config)
    cursor = g.db.cursor()

    query = "SELECT * FROM Bancada where Ativo=0"

    cursor.execute(query)
    for (ID, Tipo,Sala_ID,Ativo) in cursor:
        Bancada.append({'ID':ID,'Tipo': Tipo,'Sala_ID': Sala_ID,'Ativo':'Não'})

    cursor.close()
    g.db.close()

    return render_template('listarBancada.html', title='listarBancada', Bancada=Bancada)


@app.route('/insereBancada', methods=('GET', 'POST'))
def insereBancada():
    if request.method == 'POST':
        dados = (request.form['ID'],
                 request.form['Tipo'],
                 request.form['Sala_ID'])

        g.db = MySQLConnection(**db_config)
        cursor = g.db.cursor()

        consulta = "INSERT INTO bancada(ID,Tipo,Sala_ID,Ativo) VALUES (%s,%s,%s,'0')"
        cursor.execute(consulta, dados)
        g.db.commit()
        cursor.close()
        g.db.close()

        return redirect(url_for('Bancada'))

    return render_template('insereBancada.html', title='Bancada')

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)


