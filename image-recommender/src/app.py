import streamlit as st
from PIL import Image
from recommend import recommend

st.title("Sistema de Recomendação por Imagens")
uploaded_file = st.file_uploader("Faça upload de uma imagem", type=["jpg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem carregada", use_column_width=True)
    
    recommendations = recommend(image)
    st.write("Itens recomendados:")
    for item in recommendations:
        st.image(item)
