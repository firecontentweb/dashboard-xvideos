import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ─── CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="Fire Content Web — Análise Gratuita",
    page_icon="favicon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

WA_LINK = "https://wa.me/447460364671?text=Oi%20Vanessa!%20Quero%20desbloquear%20todas%20as%20an%C3%A1lises%20do%20meu%20canal%20%F0%9F%94%A5"

# ─── ESTILO ───────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background: #070709;
}}
.main {{ background: #070709; }}
.block-container {{ padding: 2rem 2.5rem; max-width: 1200px; }}

.fire-logo {{
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 32px;
    background: linear-gradient(135deg, #ff6b35, #ff3366);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}}
.fire-tagline {{
    font-size: 13px;
    color: #555;
    margin-top: -4px;
    margin-bottom: 2rem;
}}

div[data-testid="metric-container"] {{
    background: #0f0f12;
    border: 1px solid #1e1e26;
    border-radius: 14px;
    padding: 16px 20px;
}}
div[data-testid="metric-container"] label {{
    color: #444;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}
div[data-testid="metric-container"] [data-testid="metric-value"] {{
    color: #f0f0f0;
    font-size: 24px;
    font-weight: 600;
    font-family: 'Syne', sans-serif;
}}

.sec {{
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #333;
    margin: 2rem 0 0.8rem;
    padding-bottom: 8px;
    border-bottom: 1px solid #131318;
}}

.free-badge {{
    display: inline-block;
    background: #0a1a0a;
    border: 1px solid #2a5a2a;
    color: #4aaa4a;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-left: 10px;
    vertical-align: middle;
}}

.lock-box {{
    background: #0f0f12;
    border: 1px solid #1e1e26;
    border-radius: 14px;
    padding: 40px 30px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 10px;
}}
.lock-box::before {{
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,107,53,0.03), rgba(255,51,102,0.03));
}}
.lock-icon {{ font-size: 32px; margin-bottom: 12px; }}
.lock-title {{
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #f0f0f0;
    margin-bottom: 8px;
}}
.lock-text {{ font-size: 13px; color: #555; line-height: 1.6; margin-bottom: 20px; }}
.lock-items {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-bottom: 24px;
}}
.lock-item {{
    background: #1a1a20;
    border: 1px solid #2a2a36;
    color: #888;
    font-size: 12px;
    padding: 4px 12px;
    border-radius: 20px;
}}

.cta-btn {{
    display: inline-block;
    background: linear-gradient(135deg, #ff6b35, #ff3366);
    color: white !important;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 14px;
    padding: 14px 32px;
    border-radius: 12px;
    text-decoration: none !important;
    letter-spacing: 0.02em;
    transition: opacity 0.2s;
    box-shadow: 0 8px 32px rgba(255,51,102,0.3);
}}
.cta-btn:hover {{ opacity: 0.9; }}

.blur-container {{
    position: relative;
    overflow: hidden;
    border-radius: 14px;
}}
.blur-overlay {{
    position: absolute;
    inset: 0;
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    background: rgba(7,7,9,0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10;
    border-radius: 14px;
    border: 1px solid #1e1e26;
}}

.stFileUploader > div {{
    background: #0f0f12 !important;
    border: 1px dashed #2a2a36 !important;
    border-radius: 14px !important;
}}

.hero-box {{
    background: linear-gradient(135deg, #0f0a08, #0f0810);
    border: 1px solid #2a1a14;
    border-radius: 16px;
    padding: 32px;
    margin-bottom: 2rem;
    text-align: center;
}}
.hero-title {{
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #f0f0f0;
    margin-bottom: 8px;
}}
.hero-text {{ font-size: 14px; color: #666; line-height: 1.6; }}
</style>
""", unsafe_allow_html=True)

FIRE = "#ff6b35"
PINK = "#ff3366"
GRID = "#131318"

def cor():
    return dict(
        plot_bgcolor='#070709',
        paper_bgcolor='#070709',
        font_color='#555',
        xaxis=dict(gridcolor=GRID, zerolinecolor=GRID, color='#444'),
        yaxis=dict(gridcolor=GRID, zerolinecolor=GRID, color='#444'),
    )

def bloco_bloqueado(titulo, itens, texto=""):
    itens_html = "".join([f'<span class="lock-item">🔒 {i}</span>' for i in itens])
    texto_html = f'<div class="lock-text">{texto}</div>' if texto else ''
    return f"""
    <div class="lock-box">
        <div class="lock-icon">🔒</div>
        <div class="lock-title">{titulo}</div>
        {texto_html}
        <div class="lock-items">{itens_html}</div>
        <a href="{WA_LINK}" target="_blank" class="cta-btn">
            🔥 Desbloquear Análises Completas
        </a>
        <div style="font-size:11px;color:#333;margin-top:12px">Falar com @firecontentweb no WhatsApp</div>
    </div>
    """

# ─── HEADER ───────────────────────────────────────────────
st.markdown('<div class="fire-logo">🔥 Fire Content Web</div>', unsafe_allow_html=True)
st.markdown('<div class="fire-tagline">Análise de performance para criadoras de conteúdo adulto</div>', unsafe_allow_html=True)

st.image("banner.png", use_container_width=True)

# Hero
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">Descubra quanto você realmente pode ganhar</div>
    <div class="hero-text">
        Faça upload do seu CSV do XVideos e veja uma análise gratuita do seu canal.<br>
        Ganhos, views, memberships — tudo em segundos.<br><br>
        <strong style="color:#ff6b35">Criadoras que trabalham com dados ganham em média 2-3x mais.</strong>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── UPLOAD ───────────────────────────────────────────────
st.markdown('<div class="sec">seu csv do xvideos <span class="free-badge">grátis</span></div>', unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Arraste o CSV exportado do XVideos (Statistics → Export CSV)",
    type=['csv'],
    help="Exporte em: XVideos → Statistics → Export CSV"
)

if not uploaded:
    st.markdown("""
    <div style="background:#0f0f12;border:1px dashed #1e1e26;border-radius:14px;padding:30px;text-align:center;margin-bottom:1rem">
        <div style="font-size:28px;margin-bottom:10px">📂</div>
        <div style="color:#555;font-size:13px;line-height:1.6">
            Como exportar:<br>
            1. Acesse seu painel no XVideos<br>
            2. Vá em <strong style="color:#888">Statistics</strong><br>
            3. Clique em <strong style="color:#888">Export CSV</strong><br>
            4. Arraste o arquivo aqui
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CTA sem dados
    st.markdown(f"""
    <div class="lock-box" style="margin-top:1rem">
        <div class="lock-icon">🚀</div>
        <div class="lock-title">Quer análise completa com estratégia personalizada?</div>
        <div class="lock-text">
            A Fire Content Web oferece gestão completa do seu canal XVideos, OnlyFans e redes sociais.<br>
            Análises, estratégia de conteúdo, calendário de posts e muito mais.
        </div>
        <a href="{WA_LINK}" target="_blank" class="cta-btn">
            🔥 Falar com a Fire Content Web
        </a>
        <div style="font-size:11px;color:#333;margin-top:12px">WhatsApp · Resposta em até 24h</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── CARREGAR ─────────────────────────────────────────────
try:
    df = pd.read_csv(uploaded)
    df.columns = df.columns.str.strip()
    df['Date'] = pd.to_datetime(df['Date'])
    for col in ['Free videos earnings', 'XVideos RED', 'Total earnings']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df = df.sort_values('Date').reset_index(drop=True)
    df['Mes'] = df['Date'].dt.to_period('M').astype(str)
    df['DiaSemana'] = df['Date'].dt.day_name()
except Exception as e:
    st.error("Não foi possível ler o arquivo. Certifique-se de usar o CSV exportado diretamente do XVideos.")
    st.stop()

st.success(f"✓ {len(df)} dias carregados · {df['Date'].min().strftime('%d/%m/%Y')} até {df['Date'].max().strftime('%d/%m/%Y')}")

# ─── ANÁLISE GRATUITA ─────────────────────────────────────
st.markdown('<div class="sec">resumo do período <span class="free-badge">grátis</span></div>', unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
with c1: st.metric("💰 Ganho Total", f"${df['Total earnings'].sum():.2f}")
with c2: st.metric("📅 Média por dia", f"${df['Total earnings'].mean():.2f}")
with c3: st.metric("👥 Memberships atual", f"{int(df['Active memberships'].iloc[-1])}")
with c4: st.metric("🛒 Compras diretas", f"{int(df['Direct purchases'].sum())}")

st.markdown('<div class="sec">ganhos ao longo do tempo <span class="free-badge">grátis</span></div>', unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['Date'], y=df['Total earnings'],
    fill='tozeroy', fillcolor='rgba(255,107,53,0.08)',
    line=dict(color=FIRE, width=2), name='Ganho diário',
    hovertemplate='%{x|%d/%m}: $%{y:.2f}<extra></extra>'
))
fig.update_layout(**cor(), height=280, margin=dict(l=0,r=0,t=10,b=0),
                  showlegend=False)
fig.update_yaxes(tickprefix='$')
st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="sec">ganho por mês <span class="free-badge">grátis</span></div>', unsafe_allow_html=True)

mensal = df.groupby('Mes')['Total earnings'].sum().reset_index()
fig2 = px.bar(mensal, x='Mes', y='Total earnings',
              color_discrete_sequence=[FIRE],
              text=mensal['Total earnings'].apply(lambda x: f'${x:.0f}'))
fig2.update_layout(**cor(), height=240, margin=dict(l=0,r=0,t=10,b=0))
fig2.update_yaxes(tickprefix='$')
st.plotly_chart(fig2, use_container_width=True)

# ─── BLOCOS BLOQUEADOS ────────────────────────────────────
st.markdown('<div class="sec">análises avançadas</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(bloco_bloqueado(
        "Análise por Dia da Semana",
        ["Melhor dia para postar", "Pior dia do canal", "Padrão semanal", "Estratégia de upload"],
        "Descubra em qual dia da semana seu canal performa melhor e planeje seus uploads para maximizar ganhos."
    ), unsafe_allow_html=True)

with col2:
    st.markdown(bloco_bloqueado(
        "Análise de Frequência de Posts",
        ["Gap ideal entre posts", "Impacto no algoritmo", "Calendário otimizado", "Dias sem post vs receita"],
        "Veja como a frequência dos seus uploads afeta diretamente seus ganhos e memberships."
    ), unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown(bloco_bloqueado(
        "Insights e Projeções",
        ["Projeção do mês atual", "Meta para dobrar ganhos", "Melhor mês — análise", "O que funcionou"],
        "Insights automáticos baseados nos seus dados reais com estratégias concretas para crescer."
    ), unsafe_allow_html=True)

with col4:
    st.markdown(bloco_bloqueado(
        "Análise de Virais e Spikes",
        ["Identificar padrão viral", "Views vs ganho correlação", "Composição da receita", "Estratégia de conteúdo"],
        "Entenda o que causa seus picos de views e como replicar o sucesso dos melhores vídeos."
    ), unsafe_allow_html=True)

# ─── CTA FINAL ────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div style="background:linear-gradient(135deg,#1a0a06,#150610);border:1px solid #3a1a10;border-radius:20px;padding:40px;text-align:center;margin-top:1rem">
    <div style="font-family:'Syne',sans-serif;font-size:24px;font-weight:800;color:#f0f0f0;margin-bottom:10px">
        Pronta para aumentar seu faturamento?
    </div>
    <div style="font-size:14px;color:#666;line-height:1.7;margin-bottom:28px;max-width:500px;margin-left:auto;margin-right:auto">
        A Fire Content Web oferece análise completa, estratégia de conteúdo personalizada 
        e gestão profissional do seu canal XVideos, OnlyFans e redes sociais.
        <br><br>
        <strong style="color:#ff6b35">Criadoras na nossa gestão aumentaram o faturamento em até 3x.</strong>
    </div>
    <a href="{WA_LINK}" target="_blank" class="cta-btn" style="font-size:16px;padding:16px 40px">
        🔥 Falar com a Fire Content Web agora
    </a>
    <div style="font-size:11px;color:#333;margin-top:16px">WhatsApp · @firecontentweb · Resposta em até 24h</div>
</div>
""", unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p style='color:#222;font-size:11px;text-align:center'>🔥 Fire Content Web · Gestão e estratégia para criadoras de conteúdo adulto</p>", unsafe_allow_html=True)
