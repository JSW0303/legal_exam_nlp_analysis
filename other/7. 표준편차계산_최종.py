import pandas as pd

# 데이터 로드 
df = pd.read_csv('law_exam_final_metrics.csv')

# 과목별, 급수별로 그룹화하여 LTD의 평균과 표준편차를 한 번에 계산
ltd_stats = df.groupby(['subject', 'level'])['clarity'].agg(['count', 'mean', 'std']).reset_index()

# 컬럼명 변경
ltd_stats.columns = ['과목', '급수', '문항 수(N)', 'LTD 평균', 'LTD 표준편차(std)']

print("="*60)
print(" 과목 및 급수별 LTD 기술통계량 (평균 및 표준편차) ")
print("="*60)
print(ltd_stats.to_string(index=False))
print("="*60)