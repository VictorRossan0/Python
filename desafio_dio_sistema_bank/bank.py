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

    def registrar_transacao(self, descricao):
        self.historico.append(descricao)

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.registrar_transacao(f"Depósito de R$ {valor:.2f}")
            return "Depósito realizado com sucesso!"
        return "Valor inválido para depósito."

    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            self.registrar_transacao(f"Saque de R$ {valor:.2f}")
            return "Saque realizado com sucesso!"
        return "Saldo insuficiente ou valor inválido."

    def consultar_saldo(self):
        return f"Saldo atual: R$ {self.saldo:.2f}"

    def exibir_historico(self):
        if not self.historico:
            return "Nenhuma transação realizada."
        return "Histórico de transações:\n" + "\n".join(f"- {transacao}" for transacao in self.historico)


class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []

    def cadastrar_cliente(self, nome, cpf, data_nascimento):
        cliente = Cliente(nome, cpf, data_nascimento)
        self.clientes.append(cliente)
        return f"Cliente {nome} cadastrado com sucesso!"

    def criar_conta(self, cliente):
        numero_conta = len(self.contas) + 1
        conta = ContaBancaria(numero_conta, cliente)
        self.contas.append(conta)
        return f"Conta criada para {cliente.nome}. Número da conta: {numero_conta}", conta


# Funções para operar o sistema
def realizar_deposito(conta, valor):
    return conta.depositar(valor)

def realizar_saque(conta, valor):
    return conta.sacar(valor)

def consultar_saldo(conta):
    return conta.consultar_saldo()

def exibir_historico(conta):
    return conta.exibir_historico()


# Exemplo de uso
banco = Banco()
print(banco.cadastrar_cliente("João Silva", "123.456.789-00", "01/01/1980"))

cliente1 = banco.clientes[0]
mensagem, conta1 = banco.criar_conta(cliente1)
print(mensagem)

print(realizar_deposito(conta1, 500))
print(realizar_saque(conta1, 200))
print(consultar_saldo(conta1))
print(exibir_historico(conta1))
