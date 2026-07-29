# -*- coding: utf-8 -*-
"""
Propósito: Dividir as questões por padrão (faixa preta de 40px de altura por 2px de largura no canto esquerdo).
Autor: Adaptado com base no código de Alexandre Nassar de Peder
Atualização: 16/07/2026
"""

from PIL import Image
import os

def encontrar_faixas_pretas(imagem, cor_alvo=(0, 0, 0), tolerancia=15, altura_alvo=40, margem_erro=3):
    """
    Encontra posições onde há uma faixa vertical de largura 2 (pixels x=0 e x=1) 
    e altura aproximada de 40 pixels (entre 37 e 43) da cor preta.
    Retorna as coordenadas y de início de cada faixa.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    posicoes_corte = []
    
    # Alturas aceitáveis com base na margem de erro
    altura_minima = altura_alvo - margem_erro
    altura_maxima = altura_alvo + margem_erro
    
    y = 0
    while y < altura:
        # Verifica se o pixel atual em x=0 e x=1 é preto (dentro da tolerância)
        def eh_cor_alvo(px_x, px_y):
            if px_y >= altura:
                return False
            pixel = pixels[px_x, px_y]
            if len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
            else:  # RGB
                r, g, b = pixel[:3]
                
            return (abs(r - cor_alvo[0]) <= tolerancia and 
                    abs(g - cor_alvo[1]) <= tolerancia and 
                    abs(b - cor_alvo[2]) <= tolerancia)

        # Se detectamos o início de uma potencial faixa nos dois primeiros pixels da esquerda
        if eh_cor_alvo(0, y) and eh_cor_alvo(1, y):
            # Mede a altura consecutiva da faixa
            altura_detectada = 0
            temp_y = y
            
            while temp_y < altura and eh_cor_alvo(0, temp_y) and eh_cor_alvo(1, temp_y):
                altura_detectada += 1
                temp_y += 1
            
            # Verifica se a altura está dentro da margem de erro (37 a 43 pixels)
            if altura_minima <= altura_detectada <= altura_maxima:
                # O corte é exatamente no início do padrão (y), assim o padrão permanece no início da próxima imagem
                posicoes_corte.append(y)
                print(f"  Padrão preto encontrado de y={y} até {temp_y-1} (altura={altura_detectada}px).")
                # Avança o cursor para o fim da faixa detectada para evitar detecções redundantes
                y = temp_y
            else:
                # Se não era do tamanho correto, apenas avança um pixel para continuar procurando
                y += 1
        else:
            y += 1
            
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, nome_base_imagem):
    """
    Divide a imagem verticalmente cortando exatamente no início de cada padrão encontrado.
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    
    # Encontra as posições das faixas pretas (RGB 0,0,0)
    posicoes_corte = encontrar_faixas_pretas(imagem, cor_alvo=(0, 0, 0))
    
    if not posicoes_corte:
        print(f"  Nenhum padrão encontrado na imagem {nome_base_imagem}!")
        return
    
    print(f"  Encontrados {len(posicoes_corte)} padrões para corte.")
    
    # Cria a subpasta de saída específica para esta imagem se não existir
    pasta_saida_especifica = os.path.join(pasta_saida, os.path.splitext(nome_base_imagem)[0])
    os.makedirs(pasta_saida_especifica, exist_ok=True)
    
    posicao_anterior = 0
    
    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        # Corta a seção anterior (que vai até o início do padrão atual)
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida_especifica, nome_arquivo)
        secao.save(caminho_completo)
        print(f"  Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        # A próxima seção começa exatamente no início da faixa preta (posicao_corte),
        # mantendo assim o padrão visual preto no início da próxima imagem cortada.
        posicao_anterior = posicao_corte
    
    # Corta a seção final (do último padrão até o fim da imagem)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida_especifica, nome_arquivo)
        secao.save(caminho_completo)
        print(f"  Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

def processar_pasta_de_imagens(pasta_entrada, pasta_saida):
    """
    Percorre todas as imagens de uma pasta de entrada e executa o corte por padrão.
    """
    if not os.path.exists(pasta_entrada):
        print(f"A pasta de entrada '{pasta_entrada}' não existe!")
        return

    formatos_suportados = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    imagens = [f for f in os.listdir(pasta_entrada) if f.lower().endswith(formatos_suportados)]
    
    if not imagens:
        print(f"Nenhuma imagem encontrada na pasta '{pasta_entrada}'.")
        return
        
    print(f"Encontradas {len(imagens)} imagens para processar.\n")
    
    for nome_imagem in imagens:
        caminho_completo = os.path.join(pasta_entrada, nome_imagem)
        print(f"Processando imagem: {nome_imagem}...")
        dividir_imagem_por_faixas(caminho_completo, pasta_saida, nome_imagem)
        print("-" * 50)

if __name__ == "__main__":
    # Configure aqui o caminho das suas pastas
    #pasta_de_entrada = "933-sem-bordas"
    #pasta_de_saida = "933-divididas"

    #pasta_de_entrada = "992-sem-bordas"
    #pasta_de_saida = "992-divididas"

    #pasta_de_entrada = "1092-sem-bordas"
    #pasta_de_saida = "1092-divididas"

    pasta_de_entrada = "933-sem-bordas"
    pasta_de_saida = "933-divididas"
    
    processar_pasta_de_imagens(pasta_de_entrada, pasta_de_saida)
    print("\nProcessamento de todas as imagens concluído!")