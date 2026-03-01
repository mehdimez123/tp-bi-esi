import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# =============================================================================
# 1. CONFIGURATION DU DASHBOARD (UI/UX)
# =============================================================================
st.set_page_config(page_title="ESI - Business Intelligence Dashboard", layout="wide")

# Style CSS pour un look "High Performance" Dark Mode
st.markdown("""
<style>
    .stApp { background-color: #0F172A; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        border: 1px solid #334155 !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #1E293B; border-radius: 8px;
        color: white; padding: 0 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #3B82F6 !important; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; letter-spacing: -0.025em; color: white !important; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. MOTEUR DE DONNÉES (Extraction & Transformation)
# =============================================================================
@st.cache_data
def get_bi_data():
    # Remplacer par pd.read_csv("ventes.csv") si les fichiers sont sur GitHub
    v_data = """Num_CMD,Date_CMD,Client,Forme_Juridique,Wilaya,Type_Vente,Code_Produit,Produit,Quantite,Montant_HT
SLSD/0001,2024-12-28,SARL ABC,SARL,Alger,Direct,LAP.0120,Laptop HP Probook G4,4,500000
SLSD/0001,2024-12-28,SARL ABC,SARL,Alger,Direct,PRI.0020,Printer Canon 6030,1,49000
SLSD/0001,2024-12-28,SARL ABC,SARL,Alger,Direct,INK.0034,Toner Canon 6030,1,1800
SLSR/0002,2025-02-22,EURL XYZ,EURL,Blida,Revendeur,LAP.0011,Laptop Lenovo 110,1,89000
SLSR/0002,2025-02-22,EURL XYZ,EURL,Blida,Revendeur,PRI.0020,Printer Canon 6030,2,98000
SLSR/0002,2025-02-22,EURL XYZ,EURL,Blida,Revendeur,INK.0004,Toner Canon 6030,2,3600
SLSR/0002,2025-02-22,EURL XYZ,EURL,Blida,Revendeur,SCA.0002,Scanner Epson 1600,1,21000
SLSD/0003,2025-03-15,SARL AGRODZ,SARL,Alger,Direct,PRI.0011,Printer EPSON 3010,2,64000
SLSD/0003,2025-03-15,SARL AGRODZ,SARL,Alger,Direct,LAP.0120,Laptop HP Probook G4,1,125000
SLSG/0004,2025-03-28,SNC Wiffak,SNC,Setif,Grossiste,INK.0001,INK Canon 3210,10,18000
SLSD/0005,2025-03-28,EURL XYZ,EURL,Oran,Direct,LAP.0011,Laptop Lenovo 110,3,267000
SLSD/0005,2025-03-28,EURL XYZ,EURL,Oran,Direct,PRI.0011,Printer EPSON 3010,1,32000
SLSD/0005,2025-03-28,EURL XYZ,EURL,Oran,Direct,INK.0005,INK Epson 110,10,8000
SLSG/0006,2025-05-02,SARL ABC,SARL,Alger,Grossiste,LAP.0120,Laptop HP Probook G4,2,250000
SLSD/0007,2025-05-04,EURL HAMIDI,EURL,Oran,Direct,PRI.0020,Printer Canon 6030,2,98000"""

    a_data = """Num_CMD,Date_CMD,Fournisseur,Type_Achat,Code_Produit,Produit,Quantite,Montant_HT
POL/0001,2024-11-05,SARL IMPORT COMPUTER,Import,LAP.0120,Laptop HP Probook G4,10,1000000
POL/0001,2024-11-05,SARL IMPORT COMPUTER,Import,PRI.0020,Printer Canon 6030,10,390000
POL/0001,2024-11-05,SARL IMPORT COMPUTER,Import,INK.0034,Toner Canon 6030,20,900
POI/0002,2024-12-16,EURL ABM,Local,LAP.0011,Laptop Lenovo 110,500,33500000
POI/0002,2024-12-16,EURL ABM,Local,PRI.0011,Printer EPSON 3010,500,11500000
POI/0002,2024-12-16,EURL ABM,Local,INK.0001,INK Canon 3210,1000,600000
POI/0002,2024-12-16,EURL ABM,Local,SCA.0002,Scanner Epson 1600,200,3000000
POL/0003,2025-02-11,SARL IMPORT COMPUTER,Import,LAP.0120,Laptop HP Probook G4,5,525000
POL/0003,2025-02-11,SARL IMPORT COMPUTER,Import,PRI.0020,Printer Canon 6030,3,123000
POI/0004,2025-02-25,SNC Wiffak,Local,INK.0005,INK Epson 110,1000,600000"""

    df_v = pd.read_csv(io.StringIO(v_data))
    df_a = pd.read_csv(io.StringIO(a_data))

    # Nettoyage & Enrichissement
    for df in [df_v, df_a]:
        df['Date_CMD'] = pd.to_datetime(df['Date_CMD'])
        df['Année'] = df['Date_CMD'].dt.year.astype(str)
        df['Mois_Nom'] = df['Date_CMD'].dt.month_name()
        df['Mois_Annee'] = df['Date_CMD'].dt.strftime('%Y-%m')
        df['Categorie'] = df['Code_Produit'].apply(lambda x: 
            'Informatique' if x.startswith(('LAP','SCA')) else 
            'Impression' if x.startswith('PRI') else 'Consommables')
    
    return df_v.sort_values('Date_CMD'), df_a.sort_values('Date_CMD')

df_v, df_a = get_bi_data()

# =============================================================================
# 3. FILTRES DYNAMIQUES (SIDEBAR)
# =============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/dashboard.png")
    st.title("BI Explorateur")
    st.markdown("---")
    f_year = st.multiselect("Année d'analyse", options=df_v['Année'].unique(), default=df_v['Année'].unique())
    f_cat = st.multiselect("Catégories", options=df_v['Categorie'].unique(), default=df_v['Categorie'].unique())
    f_wilaya = st.multiselect("Wilayas", options=df_v['Wilaya'].unique(), default=df_v['Wilaya'].unique())

# Application des filtres
v_f = df_v[(df_v['Année'].isin(f_year)) & (df_v['Categorie'].isin(f_cat)) & (df_v['Wilaya'].isin(f_wilaya))]
a_f = df_a[(df_a['Année'].isin(f_year)) & (df_a['Categorie'].isin(f_cat))]

# =============================================================================
# 4. DASHBOARD - STRUCTURE EN TABS
# =============================================================================
tab1, tab2, tab3 = st.tabs(["📊 ANALYSE VENTES", "🛒 ANALYSE ACHATS", "💎 RENTABILITÉ (CUMP)"])

# --- PARTIE 01 : VENTES ---
with tab1:
    st.header("Analyse Dynamique des Ventes (Partie 01)")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CA Total (DA)", f"{v_f['Montant_HT'].sum():,.0f}")
    c2.metric("Volume Ventes", f"{v_f['Quantite'].sum()} u")
    top_cat = v_f.groupby('Categorie')['Montant_HT'].sum().idxmax() if not v_f.empty else "N/A"
    c3.metric("Top Catégorie (Q5)", top_cat)
    c4.metric("Panier Moyen", f"{(v_f['Montant_HT'].sum()/len(v_f) if len(v_f)>0 else 0):,.0f} DA")

    with st.expander("🔍 Voir la liste des ventes après le 01 Février 2025 (Exigence Q1)"):
        st.dataframe(v_f[v_f['Date_CMD'] > '2025-02-01'], use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏆 Top Produits par CA & Type (Q2)")
        fig_q2 = px.bar(v_f, x='Produit', y='Montant_HT', color='Type_Vente', 
                        facet_col='Année', template="plotly_dark", barmode='group')
        st.plotly_chart(fig_q2, use_container_width=True)
    with col2:
        st.subheader("📍 Répartition Clients par Wilaya & Forme Juridique (Q3)")
        fig_q3 = px.sunburst(v_f, path=['Wilaya', 'Forme_Juridique', 'Client'], 
                             values='Montant_HT', template="plotly_dark")
        st.plotly_chart(fig_q3, use_container_width=True)

    st.subheader("📈 Évolution Temporelle des Ventes par Catégorie (Q4)")
    fig_q4 = px.area(v_f.groupby(['Mois_Annee', 'Categorie'])['Quantite'].sum().reset_index(), 
                     x='Mois_Annee', y='Quantite', color='Categorie', template="plotly_dark")
    st.plotly_chart(fig_q4, use_container_width=True)

# --- PARTIE 02 : ACHATS ---
with tab2:
    st.header("Analyse Dynamique des Achats (Partie 02)")
    ak1, ak2, ak3, ak4 = st.columns(4)
    ak1.metric("Budget Achats (DA)", f"{a_f['Montant_HT'].sum():,.0f}")
    ak2.metric("Total Unités", f"{a_f['Quantite'].sum()} u")
    top_sup = a_f.groupby('Fournisseur')['Montant_HT'].sum().idxmax() if not a_f.empty else "N/A"
    ak3.metric("Top Fournisseur", top_sup)
    top_cat_a = a_f.groupby('Categorie')['Montant_HT'].sum().idxmax() if not a_f.empty else "N/A"
    ak4.metric("Catégorie Coûteuse (Q4)", top_cat_a)

    with st.expander("📋 Produits achetés en 2024 (Exigence Q1)"):
        st.dataframe(a_f[a_f['Année'] == '2024'], use_container_width=True)

    acol1, acol2 = st.columns(2)
    with acol1:
        st.subheader("📉 Volumes d'Achats par Mois (Q2)")
        fig_aq2 = px.bar(a_f, x='Mois_Annee', y='Quantite', color='Type_Achat', template="plotly_dark")
        st.plotly_chart(fig_aq2, use_container_width=True)
    with acol2:
        st.subheader("🚚 Analyse Fournisseurs par Catégorie (Q3)")
        fig_aq3 = px.histogram(a_f, x='Categorie', y='Montant_HT', color='Fournisseur', 
                               template="plotly_dark", barmode='group')
        st.plotly_chart(fig_aq3, use_container_width=True)

# --- PARTIE 03 : ANALYSE DES MARGES (LOGIQUE PROF : CUMP Vente - CUMP Achat) ---
with tab3:
    st.header("Analyse de la Marge Stratégique (Méthode des Prix Moyens Pondérés)")

    # 1. CALCUL DU CUMP ACHAT (Source : Données d'achats filtrées a_f)
    df_cump_a = a_f.groupby(['Code_Produit', 'Produit', 'Categorie']).agg({
        'Montant_HT': 'sum', 
        'Quantite': 'sum'
    }).reset_index()
    df_cump_a.rename(columns={'Montant_HT': 'Total_Achat', 'Quantite': 'Qté_Achat'}, inplace=True)
    df_cump_a['CUMP_Achat'] = df_cump_a['Total_Achat'] / df_cump_a['Qté_Achat']

    # 2. CALCUL DU CUMP VENTE (Source : Données de ventes filtrées v_f)
    df_cump_v = v_f.groupby(['Code_Produit']).agg({
        'Montant_HT': 'sum', 
        'Quantite': 'sum'
    }).reset_index()
    df_cump_v.rename(columns={'Montant_HT': 'Total_Vente', 'Quantite': 'Qté_Vente'}, inplace=True)
    df_cump_v['CUMP_Vente'] = df_cump_v['Total_Vente'] / df_cump_v['Qté_Vente']

    # 3. FUSION DES DEUX ANALYSES
    df_marge_globale = df_cump_a.merge(df_cump_v, on='Code_Produit', how='inner')

    # 4. CALCUL DE LA MARGE (Formule demandée : CUMP Vente - CUMP Achat)
    df_marge_globale['Marge_Unitaire'] = df_marge_globale['CUMP_Vente'] - df_marge_globale['CUMP_Achat']
    df_marge_globale['Marge_Totale'] = df_marge_globale['Marge_Unitaire'] * df_marge_globale['Qté_Vente']

    # KPIs de la Partie 3
    m1, m2, m3 = st.columns(3)
    total_marge = df_marge_globale['Marge_Totale'].sum()
    m1.metric("Marge Totale Réalisée", f"{total_marge:,.0f} DA")
    m2.metric("Rentabilité Moyenne (%)", f"{(total_marge / df_marge_globale['Total_Vente'].sum() * 100 if not df_marge_globale.empty else 0):.1f}%")
    m3.metric("Produit Star", df_marge_globale.loc[df_marge_globale['Marge_Totale'].idxmax(), 'Produit'] if not df_marge_globale.empty else "N/A")

    # Graphique de comparaison
    st.subheader("📊 Comparaison CUMP Vente vs CUMP Achat par Produit")
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(x=df_marge_globale['Produit'], y=df_marge_globale['CUMP_Vente'], name='CUMP Vente (Prix)', marker_color='#2A9D8F'))
    fig_comp.add_trace(go.Bar(x=df_marge_globale['Produit'], y=df_marge_globale['CUMP_Achat'], name='CUMP Achat (Coût)', marker_color='#E76F51'))
    fig_comp.update_layout(barmode='group', template="plotly_dark")
    st.plotly_chart(fig_comp, use_container_width=True)

    # --- TABLEAU RÉCAPITULATIF (CORRIGÉ POUR ÉVITER L'ERREUR FORMAT) ---
    st.subheader("📋 Tableau Récapitulatif des Marges")
    
    cols_texte = ['Categorie', 'Produit']
    cols_num = ['CUMP_Vente', 'CUMP_Achat', 'Marge_Unitaire', 'Qté_Vente', 'Marge_Totale']
    
    df_final = df_marge_globale[cols_texte + cols_num]
    
    # Formatage sécurisé (on ne formate que les colonnes de nombres)
    st.dataframe(
        df_final.style.format({col: "{:,.2f}" for col in cols_num}), 
        use_container_width=True
    )

st.sidebar.markdown("---")
st.sidebar.caption("Dashboard BI Performant - ESI 2024")