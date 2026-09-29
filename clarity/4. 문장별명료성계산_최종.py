import torch
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
import pandas as pd
import numpy as np
from tqdm import tqdm
import os

# 1. 모델 로드
print(" KoGPT2 모델 로드 중.")
model_name = "skt/kogpt2-base-v2"
tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name, 
    bos_token='</s>', eos_token='</s>', unk_token='<unk>', 
    pad_token='<pad>', mask_token='<mask()'
)
model = GPT2LMHeadModel.from_pretrained(model_name)
model.eval()

# 2. 명료성 정의 함수
def get_clarity_score(sentence):
    if not isinstance(sentence, str) or len(sentence.strip()) < 5:
        return np.nan, np.nan
    
    try:
        inputs = tokenizer(sentence, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model(**inputs, labels=inputs["input_ids"])
            loss = outputs.loss.item()
            
        ppl = np.exp(loss)
        clarity = 1 / ppl
        return ppl, clarity
    except:
        return np.nan, np.nan

# 3. 데이터 로드
df = pd.read_csv("law_exam_total_data.csv")
output_file = "law_exam_clarity_results.csv"

# 중간에 끊기면 남은 부분만 처리
if os.path.exists(output_file):
    processed_df = pd.read_csv(output_file)
    start_idx = len(processed_df)
    df = pd.concat([processed_df, df.iloc[start_idx:]], ignore_index=True)
    print(f"기존 데이터에 이어 {start_idx}번 행부터 다시 시작합니다.")
else:
    df['ppl'] = np.nan
    df['clarity'] = np.nan
    start_idx = 0

# 4. 루프 가동
print(f"총 {len(df) - start_idx}개의 문장 분석을 시작합니다.")

for i in tqdm(range(start_idx, len(df)), desc="Clarity 연산 중"):
    ppl, clarity = get_clarity_score(df.loc[i, 'cleaned_text'])
    df.loc[i, 'ppl'] = ppl
    df.loc[i, 'clarity'] = clarity
    
    # 100개마다 CSV로 중간 저장 (Checkpoint)
    if i % 100 == 0:
        df.to_csv(output_file, index=False, encoding='utf-8-sig')

# 최종 저장
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"\n완료! 결과가 {output_file}에 저장되었습니다.")