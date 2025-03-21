class Cliente:
    def __init__(self, nome, cpf, data_nascimento):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf})"


class ContaBancaria:
    def __init__(self, numero_conta, cliente):
        self.numero_conta = numero_conta
        self.cliente = cliente
        self.saldo = 0
        self.historico = []

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.historico.append(f"Depósito de R$ {valor:.2f}")
            print("Depósito realizado com sucesso!")
        else:
            print("Valor inválido para depósito.")

    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            self.historico.append(f"Saque de R$ {valor:.2f}")
            print("Saque realizado com sucesso!")
        else:
            print("Saldo insuficiente ou valor inválido.")

    def consultar_saldo(self):
        print(f"Saldo atual: R$ {self.saldo:.2f}")

    def exibir_historico(self):
        print("Histórico de transações:")
        for transacao in self.historico:
            print("-", transacao)


class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []

    def cadastrar_cliente(self, cliente):
        self.clientes.append(cliente)
        print(f"Cliente {cliente.nome} cadastrado com sucesso!")

    def criar_conta(self, cliente):
        numero_conta = len(self.contas) + 1
        conta = ContaBancaria(numero_conta, cliente)
        self.contas.append(conta)
        print(f"Conta criada para {cliente.nome}. Número da conta: {numero_conta}")
        return conta


# Exemplo de uso
banco = Banco()
cliente1 = Cliente("João Silva", "123.456.789-00", "01/01/1980")
banco.cadastrar_cliente(cliente1)

conta1 = banco.criar_conta(cliente1)
conta1.depositar(500)
conta1.sacar(200)
conta1.consultar_saldo()
conta1.exibir_historico()
