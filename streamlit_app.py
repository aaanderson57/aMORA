# prompt: gere um código que lê as entradas do usuário e retorna o preço de venda em um streamlit

import streamlit as st
import pickle
import pandas as pd
import sklearn

# Carrega o modelo treinado
try:
    model = pickle.load(open('housing_price_model1.pkl', 'rb'))
except FileNotFoundError:
    st.error("Erro: Arquivo 'housing_price_model.pkl' não encontrado. Certifique-se de que o modelo foi treinado e salvo corretamente.")
    st.stop()

st.title('Predição de Preço de Venda de Imóveis')

# Cria os campos de entrada para as features
quartos = st.number_input('Número de Quartos', min_value=0, value=2)
banheiros = st.number_input('Número de Banheiros', min_value=0, value=2)
vagas = st.number_input('Número de Vagas na Garagem', min_value=0, value=1)
area_util = st.number_input('Área Útil (m²)', min_value=0, value=50)


# Cria um botão para realizar a predição
if st.button('Prever Preço'):
    # Cria um DataFrame com os valores de entrada
    input_data = pd.DataFrame({
        'quartos': [quartos],
        'banheiros': [banheiros],
        'vagas_garagem': [vagas],
        'area_util': [area_util]
    })

    # Faz a predição usando o modelo carregado
    try:
        prediction = model.predict(input_data)[0]
        st.success(f'Preço de venda estimado: R$ {prediction:.2f}')
    except ValueError as e:
        st.error(f"Erro ao realizar a predição: {e}. Verifique os valores inseridos.")
