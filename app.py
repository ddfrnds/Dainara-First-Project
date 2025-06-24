import streamlit as st

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
    st.title("_Cadastro de usuarios da :blue[DaIf]_")
    st.caption(body="Me encontre em no github! [https://github.com/ddfrnds]")

    if "cpf" not in st.session_state:
        st.session_state["cpf"] = ""

    with st.container():
        nome = st.text_input("Nome")
        email = st.text_input("Email")
        telefone = st.text_input("Telefone")
        cpf = st.text_input("CPF", key="cpf", placeholder=formatar_cpf("99999999999"), on_change=on_change_cpf)
        profissao = st.text_input("Profissão")
        cep = st.text_input("CEP")
        endereco = st.text_input("Endereço completo")
        estado_civil = st.selectbox("Estado Civil", ("Solteiro", "Casado", "Separado", "Divorciado", "Viúvo"))
        tipo_de_servico = st.multiselect("Tipos de serviços", ("Escritura", "Inventario"))


app()
