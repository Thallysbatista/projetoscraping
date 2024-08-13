import pandas as pd 
from datetime import datetime 
from sqlalchemy import create_engine

# Definir o caminho para o arquivo JSONL 
df = pd.read_json('data\data.jsonl', lines=True)

# Add coluna source com valor fixo 
df['_source'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"

# Add coluna data_coleta com a data e hora atual 
df['_data_coleta'] = datetime.now()

# Tratar colunas 
df['old_price'] = df['old_price'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price'] = df['new_price'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)

# Remover os parênteses do reviews_amount e transformar para int 
df['reviews_amount'] = df['reviews_amount'].str.replace('[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# Tratar os preços como floats e calcular os valores reais 
df['old_price_real'] = df['old_price'] + df['old_price_centavos'] / 100
df['new_price_real'] = df['new_price'] + df['new_price_centavos'] / 100

# Remover as colunas antigas de preço 
df.drop(columns=['old_price','old_price_centavos','new_price','new_price_centavos'], inplace=True)

# Conectando ao banco de dados PostgreSQL usando SQLAlchemy
engine = create_engine('postgresql://postgres:123456789@localhost:5432/postgres')

# Salvar o DF no banco de dados PostgreSQL
df.to_sql('mercadolivre', con=engine, if_exists='replace', index=False)

# Fechando conexão 
engine.dispose()

print(df.head())
