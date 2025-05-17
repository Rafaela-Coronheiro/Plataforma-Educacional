import json
import os
from statistics import mean, median, mode


def gerenciar_plataforma():
    inicializar_arquivos()
    while True:
        exibir_menu_principal()
        opcao = obter_opcao()
        executar_acao(opcao)


def inicializar_arquivos():
    for arquivo in ['estudantes.json', 'cursos.json']:
        if not os.path.exists(arquivo):
            with open(arquivo, 'w') as f:
                json.dump([], f)


def exibir_menu_principal():
    print("\nMENU PRINCIPAL")
    print("1. Registrar novo aluno")
    print("2. Visualizar cursos")
    print("3. Ver estatísticas")
    print("4. Sair do sistema")


def obter_opcao():
    while True:
        try:
            return int(input("\nOpção selecionada: "))
        except ValueError:
            print("Por favor, digite um número válido.")


def executar_acao(opcao):
    acoes = {
        1: registrar_aluno,
        2: navegar_cursos,
        3: exibir_estatisticas,
        4: sair_sistema
    }
    acoes.get(opcao, opcao_invalida)()


def registrar_aluno():
    aluno = {
        "nome": input("\nNome do aluno: "),
        "idade": validar_idade(),
        "nivel": input("Nível (Iniciante/Intermediário/Avançado): ").title()
    }
    salvar_dados('estudantes.json', aluno)
    print("Cadastro concluido. Seja bem vindo!")


def validar_idade():
    while True:
        try:
            idade = int(input("Idade: "))
            if idade > 0:
                return idade
            print("Idade deve ser positiva.")
        except ValueError:
            print("Digite um número válido.")


def navegar_cursos():
    cursos = carregar_cursos()
    while True:
        exibir_cursos(cursos)
        opcao = input(
            "\nPressione Enter para voltar ou digite o número do curso: ")
        if opcao == '':
            break  # Volta ao menu principal se pressionar Enter
        mostrar_curso(cursos, opcao)


def carregar_cursos():
    cursos = carregar_dados('cursos.json')
    if not cursos:  # Se o arquivo estiver vazio
        cursos = [
            {"id": 1, "nome": "Pensamento lógico Computacional",
                "aulas": ["Algoritmos", "Lógica"]},
            {"id": 2, "nome": "Programação em Python",
                "aulas": ["Sintaxe", "Funções"]},
            {"id": 3, "nome": "Segurança Digital",
                "aulas": ["Senhas", "Privacidade"]}
        ]
        salvar_dados('cursos.json', cursos[0])  # Salva o primeiro curso
        for curso in cursos[1:]:  # Salva os demais cursos
            salvar_dados('cursos.json', curso)
    return cursos


def exibir_cursos(cursos):
    print("\nCURSOS DISPONÍVEIS:")
    for curso in cursos:
        print(f"\n{curso['id']}. {curso['nome']}")
        for aula in curso['aulas']:
            print(f"   - {aula}")


def mostrar_curso(cursos, opcao):
    curso = next((c for c in cursos if str(c['id']) == opcao), None)
    if curso:
        print(f"\nDetalhes do curso {curso['nome']}:")
        for aula in curso['aulas']:
            print(f"  → {aula}")
    else:
        print("\nCurso não encontrado!")
    input("\nPressione Enter para continuar...")


def exibir_estatisticas():
    alunos = carregar_dados('estudantes.json')
    if not alunos:
        print("\nNenhum aluno registrado.")
        return

    idades = [a['idade'] for a in alunos]
    print("\nESTATÍSTICAS:")
    print(f"Total alunos: {len(alunos)}")
    print(f"Média idade: {mean(idades):.1f}")
    print(f"Mediana: {median(idades)}")
    print(f"Moda: {mode(idades)}")
    input("\nPressione Enter para voltar...")


def carregar_dados(arquivo):
    try:
        with open(arquivo) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_dados(arquivo, novo_registro):
    try:
        dados = carregar_dados(arquivo)
        dados.append(novo_registro)
        with open(arquivo, 'w') as f:
            json.dump(dados, f, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar dados: {e}")
        return False


def opcao_invalida():
    print("Opção inválida! Tente novamente.")


def sair_sistema():
    print("\nSistema encerrado. Até mais!")
    exit()


if __name__ == '__main__':
    gerenciar_plataforma()
