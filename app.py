import streamlit as st
import pandas as pd
import base64
from pathlib import Path

# --- CONFIGURAÇÕES BÁSICAS ---
st.set_page_config(page_title="RioFresco", page_icon="🌡️", layout="wide")

# --- CAMINHOS ---
BASE_DIR = Path(__file__).parent.resolve()
DADOS = BASE_DIR / "RioFresco-main" / "dados"
ASSETS = BASE_DIR / "RioFresco-main" / "assets"

ARQUIVO_FUNDO = "fundo.png"
ARQUIVO_CLIMA = "clima_otimizado.csv"

def get_b64(path):
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode()
    return None

# --- ESTILO CSS PERSONALIZADO ---
bg_b64 = get_b64(BASE_DIR / ARQUIVO_FUNDO)
st.markdown(f"""
    <style>
    header, footer {{ visibility: hidden; }}
    
    .stApp {{ 
        background: {f'url("data:image/png;base64,{bg_b64}") center/cover fixed' if bg_b64 else "#0d0d0d"}; 
    }}

    .main-overlay {{
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(12px);
        padding: 50px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        text-align: center;
    }}

    h1 {{ color: #f4813f !important; font-weight: 900 !important; }}
    h2, h3 {{ color: #f4813f !important; }}
    
    .process-box {{
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #f4813f;
        text-align: left;
        margin-top: 10px;
    }}

    .img-container {{
        border: 4px solid #f4813f;
        border-radius: 20px;
        margin: 30px auto;
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        max-width: 85%;
    }}
    </style>
""", unsafe_allow_html=True)

# --- CONTEÚDO PRINCIPAL ---
st.markdown('<div class="main-overlay">', unsafe_allow_html=True)

# 1. CABEÇALHO
st.title("RioFresco: Resiliência Térmica e Saúde Urbana")
st.markdown("""
O **RioFresco** analisa a correlação entre cobertura vegetal, ondas de calor e impactos na saúde pública no Rio de Janeiro. 
Utilizamos dados climáticos históricos, mapeamento geoespacial e indicadores oficiais do Data.Rio e DataSUS.
""")

st.divider()

# 2. ARQUITETURA DO PROJETO (PROCESSOS ENUMERADOS E INTERATIVOS)
st.header("🛠️ Arquitetura e Processos")
st.write("Selecione uma etapa para ver os detalhes técnicos:")

# Uso de Tabs para uma visualização enumerada e organizada
tab1, tab2, tab3, tab4 = st.tabs(["1. Coleta", "2. Processamento", "3. Integração", "4. Inteligência"])

with tab1:
    st.markdown("""
    <div class="process-box">
        <h4>1. Coleta e Ingestão (baixa_csv.py)</h4>
        <p>Extração de dados da API Open-Meteo Archive com:</p>
        <ul>
            <li><b>Resiliência:</b> Exponential Backoff para Rate Limits (Erro 429).</li>
            <li><b>Consistência:</b> Sistema de Checkpoint para retomada de downloads.</li>
            <li><b>Escalabilidade:</b> Suporte a mais de 160 bairros via CLI.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="process-box">
        <h4>2. Processamento e Limpeza (EDA)</h4>
        <ul>
            <li><b>Clima:</b> Normalização de strings e criação de novas features.</li>
            <li><b>Saúde:</b> Tratamento de encodings Latin1 e padronização DataSUS.</li>
            <li><b>Vegetação:</b> Cálculo de área real (m²) via SIRGAS 2000 / UTM 23S.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div class="process-box">
        <h4>3. Integração de Dados</h4>
        <p>Unificação de três fontes em um dataset consolidado para modelos de regressão:</p>
        <ul>
            <li><b>Dataset Verde:</b> % de cobertura vegetal por bairro.</li>
            <li><b>Dataset Clima:</b> Médias e máximas térmicas mensais.</li>
            <li><b>Dataset Saúde:</b> Taxas de internação hospitalar.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown("""
    <div class="process-box">
        <h4>4. Pesquisa e Machine Learning</h4>
        <ul>
            <li><b>Regressão Linear:</b> R² de 5% indicando que altitude e mar influenciam mais que vegetação isolada.</li>
            <li><b>Clusterização:</b> Uso de K-Means para criar o <b>IVT (Índice de Vulnerabilidade Térmica)</b>.</li>
            <li><b>PCA:</b> Redução de dimensionalidade para visualização dos perfis de risco.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 3. ANÁLISES GEOESPACIAIS (PNGs)
st.header("📊 Análises Geoespaciais")
pngs = [
    ("clusters_pca.png", "Clusters de Risco (PCA)"),
    ("distribuicao_espacial_clusters.png", "Mapa de Calor por Bairros"),
    ("temperatura_por_%verde.png", "Temperatura vs. Área Verde")
]

for name, legenda in pngs:
    p = ASSETS / name
    if p.exists():
        st.markdown('<div class="img-container">', unsafe_allow_html=True)
        st.image(str(p), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f"**{legenda}**")
        st.write("---")

# 4. DADOS CLIMÁTICOS (CSV)
st.header("📈 Dados Climáticos Otimizados")
csv_path = DADOS / ARQUIVO_CLIMA
if csv_path.exists():
    df_clima = pd.read_csv(csv_path)
    st.write("Resumo Estatístico das Variáveis")
    st.dataframe(df_clima.describe().T, use_container_width=True)
    st.write("Amostra do Dataset Silver")
    st.dataframe(df_clima.head(15), use_container_width=True)
else:
    st.error(f"Arquivo {ARQUIVO_CLIMA} não encontrado.")

# 5. RODAPÉ
st.divider()
st.markdown("""
**Autores:**  
Lucas de Moraes Brandão | Pedro Tonelli da Cunha | Isac Freire | Nargylla Fernanda Cloviel Lima
""")

st.markdown('</div>', unsafe_allow_html=True)
