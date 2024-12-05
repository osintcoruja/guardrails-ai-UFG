import openai
from guardrails import Guard
from guardrails.hub import ValidURL

# Configurar chave da API da OpenAI
openai.api_key = ""

# Configurar Guard para usar o validador ValidURL
guard = Guard().use(ValidURL(on_fail="exception"))

def validar_url_via_prompt():
    """
    Valida uma URL fornecida pelo usuário via prompt utilizando OpenAI e Guardrails.
    """
    try:
        # Solicitar ao usuário a URL
        user_url = input("Por favor, insira uma URL que está sendo investigada para que a OPENAI faça a validação: ")

        # Consultar a OpenAI API sobre a validade da URL
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente para validação de URLs para investigação de crimes cibernéticos e fraudes digitais."},
                {"role": "user", "content": f"A URL investigada '{user_url}' é válida?"}
            ],
            max_tokens=50,
            temperature=0.7
        )

        # Resposta do modelo
        llm_output = response['choices'][0]['message']['content']
        print(f"Resposta do modelo: {llm_output}")

        # Validar a URL usando Guardrails
        try:
            validated_url = guard.validate(user_url)
            print(f"A URL '{validated_url}' foi validada com sucesso!")
        except Exception as e:
            print(f"A URL fornecida não é válida!!: {e}")

    except Exception as e:
        print(f"Erro ao interagir com a OpenAI API: {e}")

# Executar o script
if __name__ == "__main__":
    validar_url_via_prompt()
