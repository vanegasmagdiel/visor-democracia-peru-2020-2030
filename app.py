from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from shiny import App, render, ui
from shinywidgets import output_widget, render_widget

BASE=Path(__file__).parent
D=BASE/'data'
overall=pd.read_csv(D/'overall_multilevel_2020_2025.csv')
cats=pd.read_csv(D/'categories_multilevel_2020_2025.csv')
proj=pd.read_csv(D/'scenario_trajectories_2025_2030.csv')
summary=pd.read_csv(D/'scenario_summary_2030.csv')
bands=pd.read_csv(D/'scenario_sensitivity_bands.csv')
evidence=pd.read_csv(D/'post_election_evidence_2026.csv')
coef=pd.read_csv(D/'scenario_coefficients.csv')

SCEN={r.scenario_id:r.scenario_name for _,r in summary.iterrows()}
COL={'recuperacion_institucional':'#26734d','continuidad_hibrida':'#24518a','deriva_restrictiva':'#a93232'}
FILL={'recuperacion_institucional':'rgba(38,115,77,0.12)','continuidad_hibrida':'rgba(36,81,138,0.12)','deriva_restrictiva':'rgba(169,50,50,0.12)'}
CAT_ES=['Proceso electoral y pluralismo','Funcionamiento del gobierno','Participación política','Cultura política','Libertades civiles']
css='''
:root{--bg:#f4f7fb;--card:#fff;--line:#d9e2ec;--ink:#14253a;--muted:#63758a;--accent:#173f70;}
body{background:var(--bg);color:var(--ink);font-family:Segoe UI,Arial,sans-serif}.navbar{box-shadow:0 2px 10px #00000010}
.hero{background:linear-gradient(135deg,#173f70,#356caa);color:#fff;border-radius:22px;padding:28px 34px;margin:14px 0 20px}.hero h1{font-weight:850;font-size:2rem;margin:0 0 10px}.hero p{margin:0;line-height:1.55;color:#eef5fc}
.cardx{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px 20px;margin-bottom:18px}.titlex{font-size:1.1rem;font-weight:850}.subx{color:var(--muted);font-size:.92rem;line-height:1.5;margin:5px 0 12px}
.kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:18px}.kpi{background:#fff;border:1px solid var(--line);border-radius:16px;padding:15px}.kpi .l{color:var(--muted);font-size:.84rem}.kpi .v{font-size:1.45rem;font-weight:850}.kpi .n{font-size:.8rem;color:var(--muted);margin-top:4px}
.warn{background:#fff8e7;border:1px solid #eedb9f;border-radius:14px;padding:12px 14px;font-size:.9rem;line-height:1.45}.ok{background:#eef8f2;border:1px solid #b8ddc5;border-radius:14px;padding:12px 14px;font-size:.9rem;line-height:1.45}
.footer{font-size:.8rem;color:var(--muted);text-align:right;margin:12px 0}@media(max-width:900px){.kpis{grid-template-columns:repeat(2,1fr)}}@media(max-width:520px){.kpis{grid-template-columns:1fr}}
'''

def regime(score):
    if score<=4:return 'Autoritario'
    if score<=6:return 'Híbrido'
    if score<=8:return 'Democracia defectuosa'
    return 'Democracia plena'

def fig_history():
    f=go.Figure()
    for col,name,color in [('peru_score','Perú','#24518a'),('latin_america_score','América Latina y Caribe','#2f7d50'),('world_score','Mundo','#a66b18')]:
        f.add_trace(go.Scatter(x=overall.year,y=overall[col],mode='lines+markers+text',name=name,line=dict(width=3,color=color),marker=dict(size=8,color=color),text=[f'{v:.2f}' if name=='Perú' else '' for v in overall[col]],textposition='top center',hovertemplate=f'<b>{name}</b><br>Año: %{{x}}<br>Puntaje: %{{y:.2f}}<extra></extra>'))
    f.add_hline(y=6,line_dash='dot',line_color='#777',annotation_text='Umbral >6: democracia defectuosa',annotation_position='bottom right')
    f.update_layout(template='plotly_white',height=470,margin=dict(l=50,r=25,t=30,b=50),yaxis=dict(range=[4.7,6.8],title='Puntaje 0–10'),xaxis_title='Año',legend=dict(orientation='h',y=1.05))
    return f

def fig_categories(year):
    d=cats[cats.year==year].copy()
    f=go.Figure()
    for col,name,color in [('peru_score','Perú','#24518a'),('latin_america_score','América Latina','#2f7d50'),('world_score','Mundo','#a66b18')]:
        f.add_trace(go.Bar(x=d.category.map(lambda x: x.replace('Categoría: ','')),y=d[col],name=name,marker_color=color,hovertemplate='<b>%{x}</b><br>%{y:.2f}<extra></extra>'))
    f.update_layout(barmode='group',template='plotly_white',height=480,margin=dict(l=45,r=20,t=25,b=100),yaxis=dict(range=[0,10],title='Puntaje'),legend=dict(orientation='h',y=1.04))
    return f

def fig_scenarios():
    f=go.Figure()
    # observed line
    f.add_trace(go.Scatter(x=overall.year,y=overall.peru_score,mode='lines+markers',name='Perú observado',line=dict(color='#111f35',width=4),marker=dict(size=8)))
    for sid,name in SCEN.items():
        d=proj[proj.scenario_id==sid]
        b=bands[bands.scenario_id==sid]
        c=COL[sid]
        f.add_trace(go.Scatter(x=list(b.year)+list(b.year[::-1]),y=list(b.p90)+list(b.p10[::-1]),fill='toself',fillcolor=FILL[sid],line=dict(color='rgba(255,255,255,0)'),hoverinfo='skip',showlegend=False,name=name+' sensibilidad'))
        f.add_trace(go.Scatter(x=d.year,y=d.overall_score,mode='lines+markers+text',name=name,line=dict(color=c,width=3),marker=dict(size=8),text=[f'{v:.2f}' if y==2030 else '' for y,v in zip(d.year,d.overall_score)],textposition='middle right',hovertemplate='<b>'+name+'</b><br>Año: %{x}<br>Puntaje: %{y:.2f}<extra></extra>'))
    f.add_hline(y=6,line_dash='dot',line_color='#777')
    f.update_layout(template='plotly_white',height=520,margin=dict(l=50,r=40,t=25,b=55),yaxis=dict(range=[4.8,6.6],title='Puntaje 0–10'),xaxis_title='Año',legend=dict(orientation='h',y=1.10))
    return f

def fig_scenario_categories(sid):
    d=proj[(proj.scenario_id==sid)&(proj.year.isin([2025,2030]))]
    f=go.Figure()
    for y,color in [(2025,'#a7bad0'),(2030,COL[sid])]:
        r=d[d.year==y].iloc[0]
        f.add_trace(go.Bar(x=CAT_ES,y=[r[c] for c in CAT_ES],name=str(y),marker_color=color,text=[f'{r[c]:.2f}' for c in CAT_ES],textposition='outside'))
    f.update_layout(barmode='group',template='plotly_white',height=470,margin=dict(l=45,r=20,t=25,b=105),yaxis=dict(range=[0,10],title='Puntaje'),legend=dict(orientation='h',y=1.05))
    return f

latest=overall.iloc[-1]
app_ui=ui.page_navbar(
    ui.nav_panel('Serie 2020–2025',
        ui.div(ui.h1('Democracia en el Perú: serie integrada 2020–2025'),ui.p('Actualización del Democracy Index 2025 con comparación multinivel y trazabilidad explícita entre datos observados y calibrados.'),class_='hero'),
        ui.div(
            ui.div(ui.div('Perú 2025',class_='l'),ui.div(f"{latest.peru_score:.2f}",class_='v'),ui.div('Régimen híbrido · rank 76',class_='n'),class_='kpi'),
            ui.div(ui.div('Cambio 2024→2025',class_='l'),ui.div(f"+{latest.peru_score-overall.iloc[-2].peru_score:.2f}",class_='v'),ui.div('reversión parcial del descenso',class_='n'),class_='kpi'),
            ui.div(ui.div('LatAm 2025',class_='l'),ui.div(f"{latest.latin_america_score:.2f}",class_='v'),ui.div('vs. 5.61 en 2024',class_='n'),class_='kpi'),
            ui.div(ui.div('Mundo 2025',class_='l'),ui.div(f"{latest.world_score:.2f}",class_='v'),ui.div('vs. 5.17 en 2024',class_='n'),class_='kpi'),class_='kpis'),
        ui.div(ui.div('Trayectoria comparada',class_='titlex'),ui.div('Perú recupera 0.19 puntos en 2025, pero permanece por debajo del umbral >6.',class_='subx'),output_widget('history'),class_='cardx'),
        ui.div(ui.input_slider('year','Año para comparar categorías',2020,2025,2025,sep=''),output_widget('category_compare'),class_='cardx'),
        ui.div(ui.strong('Nota de calidad de datos 2025: '),'el puntaje total del Perú (5.88) se trata como observado; los cinco subpilares Perú-2025 son una calibración latente cuya media es 5.88 porque el resumen EIU suministrado no publica la tabla país. No deben citarse como subpilares oficiales EIU.',class_='warn')
    ),
    ui.nav_panel('Escenarios 2026–2030',
        ui.div(ui.h1('Tres escenarios prospectivos post-elecciones 2026'),ui.p('Escenarios condicionados por el resultado presidencial, observación electoral internacional, polarización, gobernabilidad bicameral, seguridad y libertades civiles. Son escenarios cuantificados, no probabilidades.'),class_='hero'),
        ui.div(ui.div('Comparación de trayectorias',class_='titlex'),ui.div('Las franjas son bandas de sensibilidad p10–p90 de 10,000 simulaciones; no son intervalos de confianza.',class_='subx'),output_widget('scenario_compare'),class_='cardx'),
        ui.div(ui.input_select('scenario','Escenario para inspección',SCEN,selected='continuidad_hibrida'),class_='cardx'),
        ui.output_ui('scenario_kpis'),
        ui.div(ui.div('Composición categorial 2025 vs 2030',class_='titlex'),output_widget('scenario_categories'),class_='cardx'),
        ui.output_ui('scenario_text')
    ),
    ui.nav_panel('Evidencia y método',
        ui.div(ui.h1('Trazabilidad, evidencia y límites del modelo'),ui.p('La integración distingue datos EIU observados, verificación secundaria, calibración categorial y proyección prospectiva.'),class_='hero'),
        ui.div(ui.div('Evidencia post-electoral incorporada',class_='titlex'),ui.output_data_frame('evidence_table'),class_='cardx'),
        ui.div(ui.div('Coeficientes por escenario',class_='titlex'),ui.output_data_frame('coef_table'),class_='cardx'),
        ui.div(ui.strong('Principio de uso: '),'las trayectorias sirven para comparar mecanismos y condiciones de cambio. No sustituyen una nueva medición EIU ni deben presentarse como pronóstico probabilístico.',class_='ok')
    ),
    ui.nav_spacer(),ui.nav_control(ui.a('README / DOI',href='README.md',target='_blank')),
    title='Visor integrado de democracia del Perú',header=ui.tags.style(css),fillable=False
)

def server(input,output,session):
    @render_widget
    def history(): return fig_history()
    @render_widget
    def category_compare(): return fig_categories(int(input.year()))
    @render_widget
    def scenario_compare(): return fig_scenarios()
    @render_widget
    def scenario_categories(): return fig_scenario_categories(input.scenario())
    @render.ui
    def scenario_kpis():
        sid=input.scenario(); r=summary[summary.scenario_id==sid].iloc[0]
        return ui.div(
            ui.div(ui.div('2026',class_='l'),ui.div(f"{r.score_2026:.2f}",class_='v'),ui.div(regime(r.score_2026),class_='n'),class_='kpi'),
            ui.div(ui.div('2030',class_='l'),ui.div(f"{r.score_2030:.2f}",class_='v'),ui.div(regime(r.score_2030),class_='n'),class_='kpi'),
            ui.div(ui.div('Cambio 2025→2030',class_='l'),ui.div(f"{r.score_2030-5.88:+.2f}",class_='v'),ui.div('puntos',class_='n'),class_='kpi'),
            ui.div(ui.div('Tipo',class_='l'),ui.div(str(r.scenario_type).title(),class_='v'),ui.div('escenario estructurado',class_='n'),class_='kpi'),class_='kpis')
    @render.ui
    def scenario_text():
        r=summary[summary.scenario_id==input.scenario()].iloc[0]
        return ui.div(ui.div(str(r.description),class_='subx'),ui.tags.ul(ui.tags.li(ui.strong('Disparadores: '),str(r.triggers)),ui.tags.li(ui.strong('Advertencias: '),str(r.warnings))),class_='cardx')
    @render.data_frame
    def evidence_table():
        return render.DataGrid(evidence[['date','source','title','signal','model_dimensions','weight']],filters=True,height='520px')
    @render.data_frame
    def coef_table():
        return render.DataGrid(coef[['scenario_name','category_es','shock_2026','annual_structural_rate']],filters=True,height='430px')

app=App(app_ui,server)
