import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pysrt
import time
from cli import translate_text, translate_subtitles


OPENAI_MODELS = [
    "gpt-4.1",          # 최고 수준의 정확도와 문맥 이해, 공식 문서 및 전문 번역에 적합
    "gpt-4o",           # 빠르고 유창한 멀티모달 처리, 실시간 및 다용도 번역에 적합
    "gpt-4.5",          # 자연스러운 문장 구성, 감성/창의성 반영에 탁월 (문학, 마케팅 번역에 유리)
    "gpt-4.1-mini",     # 경제적이고 빠른 번역 작업에 적합 (대량 자동화 번역)
    "gpt-3.5-turbo",    # 저비용 대량 번역, 내부 문서/비공식 번역에 활용 가능
    "gpt-3.5-turbo-16k" # 긴 문맥을 요구하는 문서 번역 (매뉴얼, 논문 등)에 적합
] # 영어 ↔ 한국어, 일본어, 중국어 등 주요 언어쌍에 대해서는 최신 GPT-4.1/4o 계열이 매우 높은 품질을 보입니다.

TEST_SRT = "test.srt"  # 테스트할 SRT 파일명
RESULT_FILE = "model_speed_results.txt"

def measure_subtitle_translation_time(original_texts, model):
    start = time.time()
    translate_subtitles(original_texts, model=model)
    elapsed = time.time() - start
    return elapsed



def main():
    subs = pysrt.open(TEST_SRT)
    original_texts = [sub.text for sub in subs]
    print('영어 자막 텍스트 추출 완료:', len(original_texts), "개 자막")

    results = []
    for model in OPENAI_MODELS:
        print(f"Testing model: {model}")
        try:
            elapsed = measure_subtitle_translation_time(original_texts, model)
            results.append(f"{model}: {elapsed:.2f} seconds\n")
        except Exception as e:
            results.append(f"{model}: ERROR - {str(e)}\n")
        print(results[-1].strip())

    with open(RESULT_FILE, "w") as f:
        f.writelines(results)

if __name__ == "__main__":
    main()

