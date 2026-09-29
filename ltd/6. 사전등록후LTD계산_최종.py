import pandas as pd
from kiwipiepy import Kiwi
from tqdm import tqdm
import os

# 1. Kiwi 초기화 및 사용자 사전 등록
kiwi = Kiwi()

def setup_kiwi_with_dict(dict_path):
    if not os.path.exists(dict_path):
        raise FileNotFoundError(f"'{dict_path}' 파일이 없습니다. 먼저 사전 추출 코드를 실행하세요.")
    
    with open(dict_path, "r", encoding="utf-8") as f:
        legal_terms = [line.strip() for line in f if line.strip()]
    
    # Kiwi 사용자 사전에 등록 (NNG: 일반명사 태그 부여)
    
    for term in legal_terms:
        kiwi.add_user_word(term, "NNG")
    
    print(f"{len(legal_terms)}개의 법령 용어가 Kiwi 사전에 등록되었습니다.")
    return set(legal_terms)

# 2. LTD 계산 함수 정의
def calculate_ltd(text, legal_term_set):
    if not isinstance(text, str) or len(text.strip()) < 5:
        return 0.0
    
    # 형태소 분석 (명사 계열 NNG, NNP 등만 추출)
    try:
        result = kiwi.analyze(text)
        
        nouns = [token.form for token in result[0][0] if token.tag.startswith('N')]
        
        if not nouns:
            return 0.0
        
        # 전체 명사 중 사전 수록 단어 수 카운트
        legal_word_count = sum(1 for n in nouns if n in legal_term_set)
        
        # LTD = 법령 용어 수 / 전체 명사 수
        return legal_word_count / len(nouns)
    except:
        return 0.0

# 3. 메인 실행부
if __name__ == "__main__":
    # 파일 경로 설정
    input_csv = "law_exam_clarity_results.csv" # 문장별 명료성 결과가 있는 파일
    dict_txt = "legal_user_dict.txt"           # 법령용어사전에서 추출한 법률용어 전처리 파일
    output_csv = "law_exam_final_metrics.csv"  # 최종 결과 파일
    
    # 사전 로드 및 Kiwi 세팅
    legal_term_set = setup_kiwi_with_dict(dict_txt)
    
    # 데이터 로드
    print(f"데이터를 불러오는 중: {input_csv}")
    df = pd.read_csv(input_csv)
    
    # LTD 계산
    tqdm.pandas(desc="LTD 지표 산출 중")
    df['ltd'] = df['cleaned_text'].progress_apply(lambda x: calculate_ltd(x, legal_term_set))
    
    # 최종 결과 저장
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    
    print("-" * 30)
    print(f"모든 지표 산출 완료!")
    print(f"최종 파일 저장: {os.path.abspath(output_csv)}")
    
    # 결과 확인
    print("\n[급수(Level)별 LTD 평균]")
    print(df.groupby('level')['ltd'].mean())