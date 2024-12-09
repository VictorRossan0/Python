class AvaliadorModelo:
    """
    Classe para calcular métricas de avaliação de aprendizado de máquina com base em uma matriz de confusão.
    """
    
    def __init__(self, VP, VN, FP, FN):
        """
        Inicializa a classe com os valores da matriz de confusão.
        
        :param VP: Verdadeiros Positivos
        :param VN: Verdadeiros Negativos
        :param FP: Falsos Positivos
        :param FN: Falsos Negativos
        """
        self.VP = VP
        self.VN = VN
        self.FP = FP
        self.FN = FN
    
    def calcular_acuracia(self):
        """Calcula a acurácia."""
        total = self.VP + self.VN + self.FP + self.FN
        return (self.VP + self.VN) / total if total > 0 else 0
    
    def calcular_sensibilidade(self):
        """Calcula a sensibilidade (recall)."""
        return self.VP / (self.VP + self.FN) if (self.VP + self.FN) > 0 else 0
    
    def calcular_especificidade(self):
        """Calcula a especificidade."""
        return self.VN / (self.VN + self.FP) if (self.VN + self.FP) > 0 else 0
    
    def calcular_precisao(self):
        """Calcula a precisão."""
        return self.VP / (self.VP + self.FP) if (self.VP + self.FP) > 0 else 0
    
    def calcular_fscore(self):
        """Calcula o F-Score."""
        precisao = self.calcular_precisao()
        sensibilidade = self.calcular_sensibilidade()
        if (precisao + sensibilidade) > 0:
            return 2 * (precisao * sensibilidade) / (precisao + sensibilidade)
        return 0
    
    def exibir_metricas(self):
        """Exibe todas as métricas calculadas."""
        print("Métricas calculadas:")
        print(f"Acurácia: {self.calcular_acuracia():.2f}")
        print(f"Sensibilidade (Recall): {self.calcular_sensibilidade():.2f}")
        print(f"Especificidade: {self.calcular_especificidade():.2f}")
        print(f"Precisão: {self.calcular_precisao():.2f}")
        print(f"F-Score: {self.calcular_fscore():.2f}")

# Exemplo de uso
if __name__ == "__main__":
    # Valores da matriz de confusão
    VP = 50  # Verdadeiros Positivos
    VN = 40  # Verdadeiros Negativos
    FP = 10  # Falsos Positivos
    FN = 20  # Falsos Negativos
    
    # Instanciando a classe e exibindo métricas
    avaliador = AvaliadorModelo(VP, VN, FP, FN)
    avaliador.exibir_metricas()
