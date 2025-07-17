import streamlit as st
from docxtpl import DocxTemplate
from num2words import num2words
import tempfile
import os

# utils
def formatar_cpf(cpf: str) -> str:
    """
    Formata uma string de CPF para o padrão XXX.XXX.XXX-XX.

    :param cpf: String contendo o CPF apenas com números (com ou sem pontuação).
    :return: CPF formatado ou string original se inválido.
    """
    # Remove qualquer caractere que não seja número
    cpf_numeros = ''.join(filter(str.isdigit, cpf))

    if len(cpf_numeros) != 11:
        return cpf  # Retorna o original se não tiver 11 dígitos

    return f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"

def on_change_cpf():
    cpf_atual = st.session_state['cpf']
    st.session_state['cpf'] = formatar_cpf(cpf_atual)

# app
def app():
    st.title("_Gerador de Contratos_")
    st.caption(body="Me encontre em no github! [https://github.com/ddfrnds]")

    if "cpf" not in st.session_state:
        st.session_state["cpf"] = ""
        
    estados = [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
        "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
        "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    ]

    nacionalidades_visuais = ["brasileiro(a)", "português(a)", "americano(a)"]
    estados_civis_visuais = ["solteiro(a)", "casado(a)", "divorciado(a)", "viúvo(a)"]
    
    nacionalidades_dict = {
        "Feminino": ["brasileira", "portuguesa", "americana"],
        "Masculino": ["brasileiro", "português", "americano"]
    }

    estados_civis_dict = {
        "Feminino": ["solteira", "casada", "divorciada", "viúva"],
        "Masculino": ["solteiro", "casado", "divorciado", "viúvo"]
    }

    with st.container():
        nome = st.text_input("Nome")
        genero = st.selectbox("Gênero", ["Feminino", "Masculino"])
        nacionalidade_input = st.selectbox("Nacionalidade", nacionalidades_visuais)
        estado_civil_input = st.selectbox("Estado Civil", estados_civis_visuais)
        profissao = st.text_input("Profissão")
        cpf = st.text_input("CPF", key="cpf", placeholder=formatar_cpf("99999999999"), on_change=on_change_cpf)
        carteira_de_identidade = st.text_input("RG")
        cep = st.text_input("CEP")
        rua = st.text_input("Rua")
        numero = st.text_input("Número") 
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        estado = st.selectbox ("Estado",estados)
        email = st.text_input("Email")
        telefone = st.text_input("Telefone")
        valor = st.number_input("Valor do serviço (R$)", min_value=0.00, format="%.2f", step=0.01)
        expectativa_de_faturamento = st.number_input("Expectativa de faturamento (R$)", min_value=0.00, format="%.2f", step=0.01)

        valor_extenso = num2words(valor, lang='pt_BR', to='currency')
        expectativa_extenso = num2words(expectativa_de_faturamento, lang='pt_BR', to='currency')

        forma_de_pagamento = st.text_input("Forma de pagamento")
        garantia = st.selectbox("Possui garantia?", ["Sim", "Não"])
        data_do_contrato = st.text_input("Data do contrato")
        
        if st.button("Gerar Contrato"):
            
            if genero == "Feminino":
                artigo = "a"
                ARTIGO = "A"
                preposicao_a = "à"
                preposicao_de = "da"
                MENTORADO_LABEL = "MENTORADA"
                portador = "portadora"
                inscrito = "inscrita"
            
            else:
                artigo = "o"
                ARTIGO = "O"
                preposicao_a = "ao"
                preposicao_de = "do"
                MENTORADO_LABEL = "MENTORADO"
                portador = "portador"
                inscrito = "inscrito"

            nacionalidade = nacionalidades_dict[genero][nacionalidades_visuais.index(nacionalidade_input)]
            estado_civil = estados_civis_dict[genero][estados_civis_visuais.index(estado_civil_input)]
                
            if all([nome, nacionalidade, profissao, estado_civil, cpf, carteira_de_identidade, cep, rua]):
                doc = DocxTemplate("contrato_rinp_modelo.docx")
                
                context = {
                    "NOME_COMPLETO": nome,
                    "artigo": artigo,
                    "ARTIGO": ARTIGO,
                    "preposicao_a": preposicao_a,
                    "preposicao_de": preposicao_de,
                    "MENTORADO_LABEL": MENTORADO_LABEL,
                    "inscrito": inscrito,
                    "portador": portador,
                    "nacionalidade": nacionalidade,
                    "profissão": profissao,
                    "estado_civil": estado_civil,
                    "cpf": cpf,
                    "RG": carteira_de_identidade,
                    "nome_da_rua": rua,
                    "n_da_casa": numero,
                    "bairro": bairro,
                    "cidade": cidade,
                    "estado": estado,
                    "email": email,
                    "numero_telefone": telefone,
                    "valor": f" {valor:.2f}".replace(".", ","),
                    "valor_extenso": valor_extenso,
                    "forma_de_pagamento": forma_de_pagamento,
                    "expectativa_de_faturamento": f" {expectativa_de_faturamento:.2f}".replace(".", ","),
                    "expectativa_extenso": expectativa_extenso,
                    "garantia": garantia == "Sim",  # usado no template
                    "data_extenso": data_do_contrato
                }
                
                doc.render(context)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                doc.save(tmp.name)
                st.success("Contrato gerado com sucesso!")
                
                with open(tmp.name, "rb") as file:
                    st.download_button(
                        label="📄 Baixar Contrato",
                        data=file,
                        file_name="ContratoGerado.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )


app()
