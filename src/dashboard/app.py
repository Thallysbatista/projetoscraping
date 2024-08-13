import streamlit as st 
import pandas as pd
from sqlalchemy import create_engine 
import psycopg2

# Conectar ao banco de dados 

engine = create_engine('postgresql://postgres:123456789@localhost:5432/postgres')

# Carregar os dados da tabela mercadolivre em um DataFrame pandas
# with engine.connect() as conn:: Isso cria um contexto para a conexão. 
# Quando o bloco de código é executado, a conexão é automaticamente fechada após a conclusão do bloco.
with engine.connect() as conn:
    df = pd.read_sql_query("SELECT * FROM mercadolivre", conn)

# Título da aplicação 

st.title('Pesquisa de mercado - Tênis esportivos ML')
st.subheader('KPIs principais do sistema')
col1,col2,col3,col4 = st.columns(4)

# KPI 1 Número total de itens 
total_itens = df.shape[0]
col1.metric(label="Número Total de Itens", value = total_itens)

# KPI 2 Número de marcas únicas
unique_brands = df['brand'].nunique()
col2.metric(label="Número de marcas únicas", value = unique_brands)

# KPI 3 Preço médio em reais 
avg_price = df['new_price_real'].mean().round(2)
col3.metric(label="Preço médio", value = avg_price)

# KPI 4 Mediana em reais 
median_price = df['new_price_real'].median()
col4.metric(label="Mediana", value = f"{median_price:.2f}")

# KPI 5 Quais marcas são mais encontradas até a página 10
st.subheader('Marcas mais encontradas até a página 10')
col1, col2 = st.columns([4,2])

top_10 = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_10)
col2.write(top_10)

# KPI 6 Preço médio por marca
st.subheader('Preço médio por marca')
col1, col2 = st.columns([4,2])
df_non_zero_price = df[df['new_price_real']>0]
avg_price_by_brand = df_non_zero_price.groupby('brand')['new_price_real'].mean().sort_values(ascending=False)
col1.bar_chart(avg_price_by_brand)
col2.write(avg_price_by_brand)

# KPI 7 Satisfação média por marca
st.subheader('Avaliação por marca')
col1, col2 = st.columns([4,2])
df_non_zero_reviews = df[df['reviews_rating_number']>0]
satisfaction_by_brand = df_non_zero_reviews.groupby('brand')['reviews_rating_number'].mean().sort_values(ascending=False)
col1.bar_chart(satisfaction_by_brand)
col2.write(satisfaction_by_brand)