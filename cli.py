import os
from dotenv import load_dotenv
import argparse
from tqdm import tqdm
import pysrt
import openai


# OpenAI API 키 설정
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# 번역 품질을 높이기 위해 최신 모델을 기본값으로 설정
def translate_text(text, model="gpt-4.1-mini"):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional subtitle translator. "
                    "Translate the following text into natural, fluent Korean. " # 한국어 번역 전용 프롬프트
                    "Keep the meaning accurate and concise, suitable for subtitles."
                )
            },
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()

# TODO: 현재 chunking으로 처리하여 line별로 번역하고 있지만,
# 대화의 맥락을 고려하기 위해 전체 자막을 하나의 덩어리로 번역하는 함수도 개발해야 함
def translate_subtitles(original_texts, model="gpt-4.1-mini"):
    # 3. 자막 전체를 LLM으로 번역 (chunking을 고려)
    translated_texts = [
        translate_text(text, model) for text in tqdm(original_texts, desc="Translating")
    ]
    return translated_texts




def main():
    parser = argparse.ArgumentParser(description="SRT 파일을 처리합니다.")
    parser.add_argument("filename", help="입력할 SRT 파일명")
    args = parser.parse_args()

    # 1. SRT 파일이 존재하는지 확인
    if not os.path.exists(args.filename):
        print(f"파일 '{args.filename}'이(가) 존재하지 않습니다.")
        return
    subs = pysrt.open(args.filename)

    # 2. 영어 자막 텍스트 추출
    original_texts = [sub.text for sub in subs]
    print('영어 자막 텍스트 추출 완료:', len(original_texts), "개 자막")
    
    # 3. 자막 전체를 LLM으로 번역 (chunking을 고려)
    translated_texts = translate_subtitles(original_texts)

    # 4. 기존 자막에 번역된 텍스트 반영
    for i, sub in enumerate(subs):
        sub.text = translated_texts[i]

    # 5. 번역된 자막 저장
    # 'results' 디렉토리가 있으면 그곳에 저장, 없으면 'results' 디렉토리를 생성 후 저장
    output_dir = "results"
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    base_filename = os.path.splitext(os.path.basename(args.filename))[0]
    output_filename = f"{base_filename}_translated.srt"
    output_path = os.path.join(output_dir, output_filename)
    subs.save(output_path, encoding='utf-8')
    print(f"자막 번역이 완료되었습니다. 저장 경로: {output_path}")



if __name__ == "__main__":
    main()