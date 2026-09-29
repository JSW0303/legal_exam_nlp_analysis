import os
from pyhwpx import Hwp

path = r"C:\Users\pacin\Desktop\lab\자연어처리 기술을 이용한 법률시험 특성 분석\기출문제\행정법\9급 국가직"

hwp_files = []
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".hwp"):
            hwp_files.append(os.path.join(root, file))

# 한글 객체 생성
hwp = Hwp()

for file in hwp_files:
    # 경로 정규화 (역슬래시 문제 방지)
    abs_file_path = os.path.abspath(file)
    txt_filename = abs_file_path[:-4] + ".txt"
    
    print(f"변환 중: {file}")
    
    try:
        # 파일 열기
        hwp.open(abs_file_path)
        
        # 텍스트 파일로 직접 저장
        # 표 내부의 텍스트까지 모두 포함하여 텍스트 파일로 저장
        hwp.save_as(txt_filename, "TEXT")
        
    except Exception as e:
        print(f"오류 발생 ({file}): {e}")

hwp.quit()
print("모든 변환이 완료되었습니다.")