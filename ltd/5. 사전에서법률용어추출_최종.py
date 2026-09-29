import pdfplumber
import re
from tqdm import tqdm
import os

def extract_legal_headwords(pdf_path, output_path="legal_user_dict.txt"):
    pattern = re.compile(r'^([가-힣]+)\s*\(')
    terms = set()
    
    print(f"파일 분석 시작 (1~463p): {pdf_path}")

    with pdfplumber.open(pdf_path) as pdf:
        # pdf.pages[5:463] 으로 슬라이싱하여 6~463페이지만 추출
        
        target_pages = pdf.pages[5:493] 
        
        for page in tqdm(target_pages, desc="법령용어 본문 추출 중"):
            text = page.extract_text()
            if not text:
                continue
                
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith("【용례】"):
                    continue
                
                match = pattern.match(line)
                if match:
                    word = match.group(1)
                    if len(word) > 1:
                        terms.add(word)

    sorted_terms = sorted(list(terms))
    with open(output_path, "w", encoding="utf-8") as f:
        for term in sorted_terms:
            f.write(term + "\n")
            
    print("-" * 30)
    print(f"추출 성공! 6~463p에서 총 {len(sorted_terms)}개의 핵심 용어를 확보했습니다.")
    return sorted_terms

if __name__ == "__main__":
    target_pdf = "법령용어한영사전(제2판) (1).pdf" 
    headwords = extract_legal_headwords(target_pdf)