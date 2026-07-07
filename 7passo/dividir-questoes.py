from PIL import Image
import os

def encontrar_linha_preta(imagem, limite_preto=30, largura_minima_porcentagem=0.9):
    """
    Encontra posições de corte baseando-se em uma linha contínua escura (preta).
    
    :param limite_preto: Valor máximo do canal RGB para ser considerado preto (ex: < 30).
    :param largura_minima_porcentagem: Qual porcentagem da linha horizontal precisa ser preta.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    largura_alvo = int(largura * largura_minima_porcentagem)
    
    y = 0
    while y < altura:
        pixels_pretos_na_linha = 0
        
        # Analisa a linha horizontal, ignorando pequenas margens nas bordas (5% de cada lado)
        margem = int(largura * 0.05)
        for x in range(margem, largura - margem):
            pixel = pixels[x, y]
            
            # Trata se for RGBA ou RGB
            r, g, b = pixel[:3]
            
            # Verifica se o pixel é suficientemente escuro/preto
            if r < limite_preto and g < limite_preto and b < limite_preto:
                pixels_pretos_na_linha += 1
        
        # Se a grande maioria da linha horizontal for preta, identificamos o padrão
        if pixels_pretos_na_linha >= (largura - 2 * margem) * largura_minima_porcentagem:
            # Como a linha preta faz parte do cabeçalho ('Questão 1'), cortamos exatamente nela 
            # ou 2 pixels acima para garantir uma margem limpa
            posicao_corte = y - 2
            if posicao_corte < 0:
                posicao_corte = 0
                
            posicoes_corte.append(posicao_corte)
            print(f"Linha preta de divisão encontrada em y={y}, cortando em y={posicao_corte}")
            
            # Pula alguns pixels para baixo (ex: 20 pixels) para não detectar a mesma linha ou o bloco preto adjacente
            y += 20 
        else:
            y += 1
            
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida):
    """
    Divide a imagem verticalmente cortando ANTES das linhas pretas demarcadoras
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    # Encontra as posições com base nas linhas contínuas escuras
    posicoes_corte = encontrar_linha_preta(imagem)
    
    if not posicoes_corte:
        print("Nenhuma linha divisória preta foi encontrada na imagem!")
        return
    
    print(f"Encontradas {len(posicoes_corte)} linhas pretas para corte")
    
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    
    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        # Corta o bloco correspondente à questão anterior
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"questao_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        # A próxima questão começa a partir do ponto de corte atual
        posicao_anterior = posicao_corte
    
    # Corta a última seção após o último divisor encontrado
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"questao_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    # CONFIGURAÇÃO DE ENTRADA E SAÍDA
    caminho_imagem = "colunas_concatenadas_verticalmente.png"  # Ajuste a extensão se necessário (.png ou .jpg)
    pasta_saida = "questoes_divididas" 
    
    # Executa o algoritmo
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida)
    
    print("Divisão concluída!")