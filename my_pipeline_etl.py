from conexao_bd import conexaoBD

import pandas as pd
import json
import openai
from time import sleep

# E

pd_bmi_data = pd.read_csv('bmi.csv')

bmi_data = pd_bmi_data.to_dict()
bmi_data_len = len(bmi_data['Bmi'])
print(bmi_data_len)

# T

openai_key = ... # Por motivos de segurança, para este campo e rodar o código, será necessário da sua chave do OpenAI

openai.api_key = openai_key

def generate_ai_message(bmi_info):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role" : "system",
                "content" : "Você é um analista nutricional"
            },
            {
                "role" : "user",
                "content" : f'Aconselhe alguém que tem {bmi_info[0]} anos e BMI de {bmi_info[1]}(Máximo de 150 caracteres)'
            }
        ]
    )

    return json.dumps(completion, indent=2) # Choices deu problema, então elaborei esta solução

# L

count = 0

for id in range(bmi_data_len):
    obj = json.loads(generate_ai_message((bmi_data["Age"][id], bmi_data["Bmi"][id]))) # O limite de prompts é de 200/dia
    # logo os testes foram feitos com 200 linhas da tabela ou menos.
    message = obj['choices'][0]['message']['content'].strip('\"')

    if "Tips" not in bmi_data.keys():
        bmi_data["Tips"] = {id: message}
    else:
        bmi_data["Tips"].update({id: message})

    count += 1

    if count == 3:
        sleep(61.0) # O limite para execução de prompts é 3 prompts/min
        count = 0


def add_info(bmi_data):
    query = f"""
        INSERT INTO bmi VALUES(
    """

    for id in range(bmi_data_len):
        info = f"""({id},
          {bmi_data["Age"][id]}, 
          {bmi_data["Height"][id]}, 
          {bmi_data["Weight"][id]}, 
          {bmi_data["Bmi"][id]},
          '{bmi_data["BmiClass"][id]}',
          '{bmi_data["Tips"][id]}'
          ), """
        
        query += info
    else:
        query.strip(", ")
        query += ');'
    
    conexaoBD.executar_query(query)

    return "Sucesso!"

add_info(bmi_data)