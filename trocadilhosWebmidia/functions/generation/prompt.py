import os 

def load_prompt(prompt_style, num_puns=None):
    """
    Carrega o conteúdo de um arquivo de prompt com base no estilo informado.

    Parâmetros:
        prompt_style (str): Caminho relativo (sem extensão) do estilo do prompt 
                            dentro da pasta 'files/prompts'.

    Retorna:
        str: Conteúdo completo do arquivo de prompt.
    """

    # Monta o caminho absoluto para o arquivo .txt usando f-string e barras compatíveis
    prompt_path = os.path.abspath(f'files/prompts/{prompt_style}.txt')

    # Abre o arquivo no modo leitura, usando UTF-8 para suportar acentos e caracteres especiais
    with open(prompt_path, 'r', encoding='utf-8') as file:
        prompt_text = file.read()  # Lê todo o conteúdo do arquivo como string
    prompt_text = prompt_text.replace('num_puns', f'{num_puns}')
    return prompt_text  # Retorna o texto do prompt
    