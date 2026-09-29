import os
import re
import html
import kss
from pykospacing import Spacing
from tqdm import tqdm  # 진행률 표시용

# 띄어쓰기 모델 로드
spacing = Spacing()

path = r"C:\Users\pacin\Desktop\lab\자연어처리 기술을 이용한 법률시험 특성 분석\기출문제\헌법\test"

def refine_and_fix_spacing(text):
    # 1. 기초 정제: HTML 엔티티 및 불필요한 줄바꿈 제거
    text = html.unescape(text)
    text = re.sub(r'\s+', '', text)  # 모든 공백을 일단 제거
    
    # 2. 자동 띄어쓰기 적용 (PyKoSpacing)
    # 500자 단위로 끊어서 처리
    chunk_size = 500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    spaced_text = ""
    for chunk in chunks:
        spaced_text += spacing(chunk)
    
    # 3. 문장 분절 (KSS)
    sentences = kss.split_sentences(spaced_text)
    
    return sentences

# 메인 루프
for root, dirs, files in os.walk(path):
    txt_files = [f for f in files if f.endswith(".txt")]
    
    for file in tqdm(txt_files, desc="파일 처리 중"):
        filepath = os.path.join(root, file)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_text = f.read()
            
        # 전처리 및 띄어쓰기 교정 실행
        refined_sentences = refine_and_fix_spacing(raw_text)
        
        # 결과 저장 (한 줄에 한 문장)
        with open(filepath, 'w', encoding='utf-8') as f:
            for sent in refined_sentences:
                # 기호 주변의 불필요한 공백 정리
                clean_sent = re.sub(r'\s+([,.)])', r'\1', sent.strip())
                f.write(clean_sent + "\n")

print("띄어쓰기 교정 및 문장 분절이 완료되었습니다.")