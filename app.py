import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# =============================================================================
# 1. CONFIGURATION DU DASHBOARD (UI/UX)
# =============================================================================
st.set_page_config(page_title="ESI - Business Intelligence Pro", layout="wide")

# Custom CSS pour un look "High Performance"
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
    h1, h2, h3 { font-family: 'Inter', sans-serif; letter-spacing: -0.025em; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. MOTEUR DE DONNÉES (Extraction & Transformation)
# =============================================================================
@st.cache_data
def get_bi_data():
    # Tableau 01 : Ventes
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

    # Tableau 02 : Achats
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

    # Nettoyage & Feature Engineering
    for df in [df_v, df_a]:
        df['Date_CMD'] = pd.to_datetime(df['Date_CMD'])
        df['Année'] = df['Date_CMD'].dt.year.astype(str)
        df['Mois_Nom'] = df['Date_CMD'].dt.month_name()
        df['Mois_Num'] = df['Date_CMD'].dt.month
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

# Application des filtres sur les données de travail
v_f = df_v[(df_v['Année'].isin(f_year)) & (df_v['Categorie'].isin(f_cat)) & (df_v['Wilaya'].isin(f_wilaya))]
a_f = df_a[(df_a['Année'].isin(f_year)) & (df_a['Categorie'].isin(f_cat))]

# =============================================================================
# 4. DASHBOARD - STRUCTURE EN TABS
# =============================================================================
st.title("🚀 Business Intelligence - CS 2ème Année")
tab1, tab2, tab3 = st.tabs(["📊 ANALYSE VENTES", "🛒 ANALYSE ACHATS", "💎 RENTABILITÉ & FUSION"])

# --- PARTIE 01 : VENTES ---
with tab1:
    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CA Total (DA)", f"{v_f['Montant_HT'].sum():,.0f}")
    c2.metric("Volume Ventes", f"{v_f['Quantite'].sum()} u")
    c3.metric("Panier Moyen", f"{(v_f['Montant_HT'].sum()/len(v_f) if len(v_f)>0 else 0):,.0f} DA")
    top_cat = v_f.groupby('Categorie')['Montant_HT'].sum().idxmax() if not v_f.empty else "N/A"
    c4.metric("Top Catégorie (Q5)", top_cat)

    # Q1 : Liste après 01/02/2025
    with st.expander("🔍 Voir la liste des ventes après le 01 Février 2025 (Exigence Q1)"):
        st.dataframe(v_f[v_f['Date_CMD'] > '2025-02-01'], use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏆 Classement Produits par CA (Q2)")
        fig_q2 = px.bar(v_f, x='Produit', y='Montant_HT', color='Type_Vente', 
                        facet_col='Année', template="plotly_dark", barmode='group')
        st.plotly_chart(fig_q2, use_container_width=True)

    with col2:
        st.subheader("📍 Répartition Clients par Wilaya (Q3)")
        fig_q3 = px.sunburst(v_f, path=['Wilaya', 'Forme_Juridique', 'Client'], 
                             values='Montant_HT', color='Montant_HT', template="plotly_dark")
        st.plotly_chart(fig_q3, use_container_width=True)

    st.subheader("📈 Évolution Temporelle des Ventes par Catégorie (Q4)")
    fig_q4 = px.area(v_f.groupby(['Mois_Annee', 'Categorie'])['Quantite'].sum().reset_index(), 
                     x='Mois_Annee', y='Quantite', color='Categorie', template="plotly_dark")
    st.plotly_chart(fig_q4, use_container_width=True)

# --- PARTIE 02 : ACHATS ---
with tab2:
    # KPIs
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
        st.subheader("📉 Volumes d'Achats par Mois & Type (Q2)")
        fig_aq2 = px.bar(a_f, x='Mois_Annee', y='Quantite', color='Type_Achat', 
                         template="plotly_dark", barmode='stack')
        st.plotly_chart(fig_aq2, use_container_width=True)

    with acol2:
        st.subheader("🚚 Analyse Fournisseurs par Catégorie (Q3)")
        fig_aq3 = px.histogram(a_f, x='Categorie', y='Montant_HT', color='Fournisseur', 
                               template="plotly_dark", barmode='group')
        st.plotly_chart(fig_aq3, use_container_width=True)

# --- PARTIE 03 : FUSION & MARGES ---
with tab3:
    st.header("Analyse de la Marge (Fusion T1 + T2)")
    
    # LOGIQUE DE FUSION
    # On calcule le prix d'achat moyen unitaire par produit depuis les achats
    df_a['Prix_Achat_Unit'] = df_a['Montant_HT'] / df_a['Quantite']
    prix_achat_ref = df_a.groupby('Code_Produit')['Prix_Achat_Unit'].mean().reset_index()

    # Fusion avec les ventes filtrées
    df_m = v_f.merge(prix_achat_ref, on='Code_Produit', how='left')
    df_m['Prix_Vente_Unit'] = df_m['Montant_HT'] / df_m['Quantite']
    df_m['Marge_Unit'] = df_m['Prix_Vente_Unit'] - df_m['Prix_Achat_Unit']
    df_m['Marge_Totale'] = df_m['Marge_Unit'] * df_m['Quantite']

    # KPIs Marges
    m1, m2, m3, m4 = st.columns(4)
    marge_totale = df_m['Marge_Totale'].sum()
    m1.metric("Marge Bénéficiaire (DA)", f"{marge_totale:,.0f}")
    m2.metric("Taux de Marge", f"{(marge_totale/v_f['Montant_HT'].sum()*100 if not v_f.empty else 0):.1f}%")
    best_p = df_m.groupby('Produit')['Marge_Totale'].sum().idxmax() if not df_m.empty else "N/A"
    m3.metric("Produit Star", best_p)
    m4.metric("ROI Moyen", f"{(df_m['Marge_Totale'].sum()/df_m['Prix_Achat_Unit'].sum()*10 if not df_m.empty else 0):.1f}%")

    st.subheader("🔍 Analyse Dynamique des Marges (Partie 03)")
    param_m = st.selectbox("Choisir l'axe d'analyse des marges :", 
                           ["Produit", "Categorie", "Wilaya", "Mois_Nom", "Année"])
    
    fig_marge = px.bar(df_m.groupby(param_m)['Marge_Totale'].sum().reset_index().sort_values('Marge_Totale'), 
                       x='Marge_Totale', y=param_m, orientation='h', 
                       color='Marge_Totale', color_continuous_scale='RdYlGn', template="plotly_dark")
    st.plotly_chart(fig_marge, use_container_width=True)

    # TABLEAU DE SYNTHÈSE FUSIONNÉ
    with st.expander("📄 Voir la table fusionnée complète"):
        st.write(df_m[['Date_CMD', 'Produit', 'Quantite', 'Prix_Achat_Unit', 'Prix_Vente_Unit', 'Marge_Totale']])

st.sidebar.markdown("---")
st.sidebar.caption("Dashboard développé pour le module Business Intelligence - CS2")