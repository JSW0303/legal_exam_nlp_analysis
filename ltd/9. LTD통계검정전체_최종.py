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
    print(f" [{sub}] 과목 급수별 LTD 통계 분석 (회귀분석 + ANOVA 사후검정) ")
    print("="*80)
    
    # 과목별 데이터 필터링
    sub_df = df[df['subject'] == sub].copy()
    
    if len(sub_df) == 0:
        print(f"'{sub}' 과목에 해당하는 데이터가 없습니다. 컬럼명을 확인하세요.")
        continue
        
    
    # 다중 선형 회귀 분석
    
    X_dummies = pd.get_dummies(sub_df['level'], prefix='level', drop_first=True, dtype=int)
    y = sub_df['ltd']
    
    X = sm.add_constant(X_dummies)
    regression_model = sm.OLS(y, X).fit()
    
    print("\n[1] 다중 선형 회귀분석 요약")
    print(regression_model.summary())
    print("-" * 80)
    
   
    # ANOVA 및 Tukey HSD
    
    print("\n일원배치 분산분석 (One-way ANOVA) 결과")
    #일방향 ANOVA
    anova_model = ols('ltd ~ C(level)', data=sub_df).fit()
    anova_table = sm.stats.anova_lm(anova_model, typ=2)
    print(anova_table)
    print("-" * 80)
    
    print("\n5급 vs 7급 / 7급 vs 9급 단계별 사후검정 (Tukey HSD)")
    # Tukey HSD를 통해 (5급vs7급), (7급vs9급), (5급vs9급) 3가지 조합을 전부 일대일 검정
    tukey = pairwise_tukeyhsd(endog=sub_df['ltd'],     # 종속변수 (LTD)
                              groups=sub_df['level'],   # 독립변수 (급수)
                              alpha=0.05)               # 유의수준
    print(tukey)
    print("="*80)