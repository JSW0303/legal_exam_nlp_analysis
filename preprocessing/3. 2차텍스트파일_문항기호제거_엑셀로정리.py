import os
import re
import html
import pandas as pd
from tqdm import tqdm

# 1. 환경 설정
# 헌법/행정법 폴더가 모두 포함된 최상위 폴더 경로
base_path = r"C:\Users\pacin\Desktop\lab\자연어처리 기술을 이용한 법률시험 특성 분석\기출문제\텍스트파일" 
output_name = "law_exam_total_data.csv"

# 2. 전처리 함수 (노이즈 제거)
def final_cleaning(sentence):
    # 문항 번호 및 선택지 기호 제거
    clean_sent = re.sub(r'【문\s?\d+】', '', sentence)
    clean_sent = re.sub(r'[①②③④⑤]', '', clean_sent)
    # 한자 병기 제거 (예: 제한(制限) -> 제한)
    clean_sent = re.sub(r'\([가-힣\s]*[一-龥]+[가-힣\s]*\)', '', clean_sent)
    clean_sent = re.sub(r'[一-龥]', '', clean_sent)
    return clean_sent.strip()

all_data = []

# 3. 폴더 트리 순회 시작
for root, dirs, files in os.walk(base_path):
    txt_files = [f for f in files if f.endswith(".txt")]
    if not txt_files:
        continue
    
    # [과목/급수 라벨링 정보 추출]
    # root 경로에 포함된 단어로 과목 식별
    subject = "헌법" if "헌법" in root else "행정법" if "행정법" in root else "미분류"
    # 현재 폴더명을 grade로 사용
    grade_folder = os.path.basename(root)
    
    # 행정사 및 5급을 동일 그룹으로 묶기
    level = "미분류"
    if any(x in grade_folder for x in ["5급", "행정사"]):
        level = "5"
    elif "7급" in grade_folder:
        level = "7"
    elif "9급" in grade_folder:
        level = "9"

    for file in tqdm(txt_files, desc=f"처리 중: {grade_folder}"):
        filepath = os.path.join(root, file)
        
        # [인코딩 쉴드] UTF-8 시도 후 실패 시 CP949로 재시도
        lines = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='cp949') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"\nSkipping {file} due to error: {e}")
            continue

        for line in lines:
            original_sentence = line.strip()
            if not original_sentence: continue
            
            # 최종 클리닝 적용
            cleaned_sentence = final_cleaning(original_sentence)
            
            # 분석 가치가 있는 문장만 저장 (10자 이상)
            if len(cleaned_sentence) > 10:
                all_data.append({
                    "file_name": file,
                    "subject": subject,
                    "grade": grade_folder,
                    "level": level,
                    "raw_text": original_sentence,
                    "cleaned_text": cleaned_sentence
                })

# 4. 데이터프레임 변환 및 저장
if all_data:
    df = pd.DataFrame(all_data)
    # 엑셀에서 바로 열 수 있도록 utf-8-sig로 저장
    df.to_csv(output_name, index=False, encoding='utf-8-sig')
    print(f"\n 작업 완료! 총 {len(df)}개의 문장이 '{output_name}'에 통합되었습니다.")
    print("\n[급수별 수집 현황]")
    print(df['grade'].value_counts())
else:
    print("수집된 데이터가 없습니다. 경로를 다시 확인해주세요.")