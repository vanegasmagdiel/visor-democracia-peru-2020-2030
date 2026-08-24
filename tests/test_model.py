from pathlib import Path
import pandas as pd
BASE=Path(__file__).resolve().parents[1]

def test_anchor_2025():
    d=pd.read_csv(BASE/'data/categories_multilevel_2020_2025.csv')
    p=d[d.year==2025].peru_score.mean()
    assert abs(p-5.88)<1e-9

def test_three_scenarios():
    d=pd.read_csv(BASE/'data/scenario_summary_2030.csv')
    assert d.scenario_id.nunique()==3
    assert set(d.scenario_id)=={'recuperacion_institucional','continuidad_hibrida','deriva_restrictiva'}

def test_ordering_2030():
    d=pd.read_csv(BASE/'data/scenario_summary_2030.csv').set_index('scenario_id')
    assert d.loc['recuperacion_institucional','score_2030'] > d.loc['continuidad_hibrida','score_2030'] > d.loc['deriva_restrictiva','score_2030']

def test_scores_in_range():
    d=pd.read_csv(BASE/'data/scenario_trajectories_2025_2030.csv')
    assert d.overall_score.between(0,10).all()
