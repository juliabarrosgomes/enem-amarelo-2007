
from PIL import Image
import os

pasta_imagens = "933-cortadas"
pasta_saida = "933-sem-bordas"

#pasta_imagens = "992-cortadas"
#pasta_saida = "992-sem-bordas"

#pasta_imagens = "1092-cortadas"
#pasta_saida = "1092-sem-bordas"

#pasta_imagens = "1169-cortadas"
#pasta_saida = "1169-sem-bordas"

os.makedirs(pasta_saida, exist_ok=True)

for nome_arquivo in os.listdir(pasta_imagens):
    if nome_arquivo.lower().endswith(".png"):
        caminho_entrada = os.path.join(pasta_imagens, nome_arquivo)
        imagem = Image.open(caminho_entrada)
        
        largura, altura = imagem.size
        
        # Aplica o corte original das bordas totais
        caixa_corte = (0, 0, largura, altura)
        
        # Aplica cortes adicionais baseados no nome do arquivo
        if nome_arquivo.endswith("_esquerda.png"):
            #caixa_corte = (caixa_corte[0], caixa_corte[1], caixa_corte[2] - 31, caixa_corte[3]) # ESQUERDA do pixel 933 cortado ao meio
            #caixa_corte = (caixa_corte[0], caixa_corte[1], caixa_corte[2] - 40, caixa_corte[3]) # ESQUERDA do pixel 992 cortado ao meio
            #caixa_corte = (caixa_corte[0], caixa_corte[1], caixa_corte[2] - 40, caixa_corte[3]) # ESQUERDA do pixel 1092 cortado ao meio
            caixa_corte = (caixa_corte[0], caixa_corte[1], caixa_corte[2] - 42, caixa_corte[3]) # ESQUERDA do pixel 1169 cortado ao meio
        
        elif nome_arquivo.endswith("_direita.png"):
            #caixa_corte = (caixa_corte[0] + 47, caixa_corte[1], caixa_corte[2] - 2, caixa_corte[3]) # DIREITA do pixel 933 cortado ao meio
            #caixa_corte = (caixa_corte[0] + 48, caixa_corte[1], caixa_corte[2] - 17, caixa_corte[3]) # DIREITA do pixel 992 cortado ao meio
            #caixa_corte = (caixa_corte[0] + 48, caixa_corte[1], caixa_corte[2], caixa_corte[3]) # DIREITA do pixel 1092 cortado ao meio
            caixa_corte = (caixa_corte[0] + 48, caixa_corte[1], caixa_corte[2] - 16, caixa_corte[3]) # DIREITA do pixel 1169 cortado ao meio
        
        imagem_cortada = imagem.crop(caixa_corte)
        
        caminho_saida = os.path.join(pasta_saida, nome_arquivo)
        imagem_cortada.save(caminho_saida)

print("Recorte das bordas concluído.")