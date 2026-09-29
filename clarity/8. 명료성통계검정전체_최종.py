import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# 데이터 로드
df = pd.read_csv('law_exam_final_metrics.csv')

subjects = ['헌법', '행정법']

for sub in subjects:
    print("\n" + "="*80)
    print(f" [{sub}] 과목 급수별 명료성 통계 분석 (회귀분석 + ANOVA 사후검정) ")
    print("="*80)
    
    # 과목별 데이터 필터링
    sub_df = df[df['subject'] == sub].copy()
    
    if len(sub_df) == 0:
        print(f"'{sub}' 과목에 해당하는 데이터가 없습니다. 컬럼명을 확인하세요.")
        continue
        
    
    # 다중 선형 회귀 분석
    
    X_dummies = pd.get_dummies(sub_df['level'], prefix='level', drop_first=True, dtype=int)
    y = sub_df['clarity']  
    
    X = sm.add_constant(X_dummies)
    regression_model = sm.OLS(y, X).fit()
    
    print("\n[1] 다중 선형 회귀분석 요약")
    
    
    summary_str = regression_model.summary().as_text()
    summary_str = summary_str.replace('const      ', 'level_5    ')
    
    print(summary_str)
    print("-" * 80)
    
    
    # ANOVA 및 Tukey HSD
    
    print("\n일원배치 분산분석 (One-way ANOVA) 결과")
    # 명료성 변수에 대한 급수별 차이 검정
    anova_model = ols('clarity ~ C(level)', data=sub_df).fit()
    anova_table = sm.stats.anova_lm(anova_model, typ=2)
    print(anova_table)
    print("-" * 80)
    
    print("\n단계별 사후검정 (Tukey HSD) 결과")
    tukey = pairwise_tukeyhsd(endog=sub_df['clarity'], 
                              groups=sub_df['level'], 
                              alpha=0.05)
    print(tukey)
    print("="*80)