import openai
import pandas as pd
import os
from typing import List, Dict, Any
import re
import json
from datetime import datetime
import time


class PunsGenerator:
    def __init__(self, openai_api_key: str, maritaca_api_key: str, use_sabia_generate: bool = False):
        """
        Inicializa o gerador com controle do modelo de geração (GPT ou Sabiá).
        Análises sempre serão feitas por ambos os modelos.
        """
        self.use_sabia_generate = use_sabia_generate
        self.df = self._load_or_create_dataframe()

        # Clientes
        openai.api_key = openai_api_key
        self.client_gpt = openai

        self.client_sabia = openai.OpenAI(
            api_key=maritaca_api_key,
            base_url="https://chat.maritaca.ai/api"
        )

    def _load_or_create_dataframe(self) -> pd.DataFrame:
        if os.path.exists(os.path.abspath('files\puns_sintetico\puns_history.csv')):
            return pd.read_csv(os.path.abspath('files\puns_sintetico\puns_history.csv'))
        # agora com as colunas de estilo incluídas
        return pd.DataFrame(columns=[
            'timestamp', 'puns',
            'pun_bin_sabia', 'pun_style_sabia', 'analyses_sabia',
            'pun_bin_gpt',   'pun_style_gpt',   'analyses_gpt'
        ])

    def generate_puns(self, promtp_generation: str) -> List[str]:
        """
        Gera trocadilhos com GPT ou Sabiá.
        """

        client = self.client_sabia if self.use_sabia_generate else self.client_gpt
        model = "sabia-3.1" if self.use_sabia_generate else "gpt-4o"

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": promtp_generation}],
            temperature=0.7,
            max_tokens=7000
        )

        puns = response.choices[0].message.content.strip().split('\n')
        return [pun.strip() for pun in puns if pun.strip()]

    def _clean_json_response(self, response_text: str) -> str:
        """
        Extrai JSON bruto da resposta.
        """
        json_pattern = r'```(?:json)?\s*([\s\S]*?)```'
        matches = re.findall(json_pattern, response_text)
        return matches[0].strip() if matches else response_text.strip()

    def analyze_puns(self, puns: List[str], prompt_recognition_2: str, model_name: str) -> List[Dict[str, str]]:
        """
        Analisa trocadilhos com o modelo especificado: 'sabia' ou 'gpt'
        """
        prompt_recognition = """Você é um analista especializado em reconhecimento e avaliação de humor linguístico, com foco específico em trocadilhos.

- Definição: Trocadilhos são jogos de palavras que exploram ambiguidade semântica com a mesma grafia e múltiplos significados (trocadilhos homográficos) ou a semelhança sonora entre palavras de grafia distinta (trocadilhos heterográficos) com objetivo é causar surpresa e humor inteligente.

Exemplos de Trocadilhos Homográficos:
• Deve ser difícil ser professor de natação. Você ensina, ensina, e o aluno nada.
• Como é que os sapateiros entram nas piscinas? Fazem um salto.
• Por que o carro do dentista foi apreendido? Porque ele estava sem placa.
• Porque é que os indecisos não atravessam o rio? Porque não há margem para dúvidas.
• Se honestidade responsabilidade e humildade pudessem ser negociados, onde se daria essa negociação? Na bolsa de valores.

Exemplos de Trocadilhos Heterográficos:
• Qual o animal que trabalha bem como carpinteiro? Rinocerrote.
• Qual árvore ficou de saco cheio e mandou você embora? Bom... sai.
• Qual a cidade que está inovando sua forma de comunicação? Emoji Mirim.
• Como se chamava a apresentadora do primeiro programa feito para a internet? Web Camargo.
• Como se chama o cara que ficou rico vendendo pipoca? Milhonário.

Tarefa: Determinar se o conteúdo atende aos critérios para ser classificado como um trocadilho, considerando a defição imposta e nos exemplos dados. Avalie a estrutura e o uso de humor de cada frase fornecida. Após isso, guarde a reposta na sua memória de "SIM" ou "NÃO".

• Se a resposta de ser um trocadilho for "NÃO", sem realizar as análises posteriores, retorne imediatamente o JSON com:
{
  "pun_bin": "NÃO",
  "pun": "",
  "analysis": ""
}

• Se a resposta de ser um trocadilho for "SIM", explique o trocadilho e de onde que vem o caráter humorístico dele. Formato obrigatório de saída: Retorne todas as respostas em JSON, como descrito abaixo:
{
  "ratings": [
    {
      "pun_bin": "SIM",
      "pun_style": "TROCADILHO HOMOGRAFICO" ou "TROCADILHO HETEROGRAFICO",
      "pun": "texto do trocadilho",
      "analysis": "breve análise crítica"
    },
    {
      "pun_bin": "NÃO",
      "pun_style": ""
      "pun": "",
      "analysis": ""
    }
    // repita conforme necessário
  ]
}"""
        prompt_recognition += f"\nTextos para análise:\n{json.dumps(puns, indent=2, ensure_ascii=False)}"

        if model_name == "sabia":
            client = self.client_sabia
            model = "sabia-3.1"
        else:
            client = self.client_gpt
            model = "gpt-4o"

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt_recognition}],
            temperature=0.7,
            max_tokens=4000
        )

        content = response.choices[0].message.content
        cleaned = self._clean_json_response(content)

        data = json.loads(cleaned)
        return data.get("ratings", [])


    def save_to_dataframe(self, ratings_sabia: List[Dict[str, Any]], ratings_gpt: List[Dict[str, Any]]) -> None:
        """
        Salva resultados de ambas as análises no DataFrame.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rows = []

        min_len = min(len(ratings_sabia), len(ratings_gpt))

        for i in range(min_len):
            rows.append({
                'timestamp': timestamp,
                'puns': ratings_sabia[i].get('pun', '') or ratings_gpt[i].get('pun', ''),
                'pun_bin_sabia': ratings_sabia[i].get('pun_bin', ''),
                'pun_style_sabia': ratings_sabia[i].get('pun_style', ''),
                'analyses_sabia': ratings_sabia[i].get('analysis', ''),
                'pun_bin_gpt': ratings_gpt[i].get('pun_bin', ''),
                'pun_style_gpt': ratings_gpt[i].get('pun_style', ''),
                'analyses_gpt': ratings_gpt[i].get('analysis', '')
            })

        self.df = pd.concat([self.df, pd.DataFrame(rows)], ignore_index=True)
        self.df.to_csv(os.path.abspath('files\puns_sintetico\puns_history.csv'), index=False)

    def run_batch_process(self, prompt_generation, prompt_recognition: str, num_batches: int = 1):
        print(f"🎭 Rodando {num_batches} batches...\n")

        for i in range(num_batches):
            print(f"📦 Batch {i+1}/{num_batches}")
            print("-" * 50)

            try:
                puns = self.generate_puns(prompt_generation)
                print(puns)
                print(f"🔤 Gerados {len(puns)} trocadilhos.")

                ratings_sabia = self.analyze_puns(puns, prompt_recognition, model_name="sabia")
                ratings_gpt = self.analyze_puns(puns, prompt_recognition, model_name="gpt")

                self.save_to_dataframe(ratings_sabia, ratings_gpt)
                print("✅ Resultados salvos!\n")

                if i < num_batches - 1:
                    time.sleep(2)

            except Exception as e:
                print(f"❌ Erro no batch {i+1}: {str(e)}")
                import traceback
                traceback.print_exc()

        print("🏁 Finalizado!")

    def get_history(self) -> pd.DataFrame:
        return self.df

