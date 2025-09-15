# ◽ NLP(자연어처리)
## 가상환경 파일은 .gitignore에 추가

```bash
echo "NLP_Lec_env/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".ipynb_checkpoints/" >> .gitignore
echo ".DS_Store" >> .gitignore
```
---
- conda base 접속
    - `conda activate base`
- 가상환경 활성화 명령어
    - `source ~/Desktop/4-1/NLP_PJT/NLP_Lec_env/bin/activate`
- 가상환경 비활성화 명령어
    - `deactivate`
- 패키지 설치 명령어
    - `pip install numpy==1.24.3 tensorflow-macos==2.13.0 spacy==3.6.1`
    - `pip install pandas==1.5.3 scipy==1.10.1 scikit-learn==1.2.2 numba==0.57.1`
    - `pip install tables==3.9.2 cython==0.29.36 blosc2==2.3.0 typing-extensions==4.5.0` (버전 변경)
- ipykernel 설치
    - `pip install jupyter ipykernel`
    - **typing-extensions 버전 충돌남!**
        - tensorflow-macos는 **4.6.0 미만** 버전을 요구하는데,
        - 현재 설치된 typing-extensions는 **4.15.0**이라서 호환되지 않습니다.
        - 아까 설치할 때 `typing-extensions 4.5.0`을 설치 했지만 pip은 패키지 의존성 충돌시 최신 버전을 설치하려고 하기 때문에 최신버전을 설치한 것임 → 그럼 아까 패키지 충돌이 났는데 자동으로 최신버전이 깔린 것임
   - 안정적인 패키지 조합
    
    
    | **패키지** | **버전** | **비고** |
    | --- | --- | --- |
    | numpy | 1.24.3 | TensorFlow 호환 |
    | tensorflow-macos | 2.13.0 | Mac Python 3.9 호환 |
    | spacy | 3.6.1 | Python 3.9 호환 |
    | tables | 3.8.0 | blosc2 2.0.0과 호환 |
    | cython | 0.29.36 | tables 3.8.0용 |
    | blosc2 | 2.0.0 | tables 3.8.0용 |
    | typing-extensions | 4.5.0 | TensorFlow 호환 |
    | exceptiongroup | 1.2.0 | typing-extensions 4.5.0과 호환 |
        
- 사용할 가상환경을 커널에 등록
    - `python3.9 -m ipykernel install --user --name=NLP_Lec_env --display-name "NLP(NLP_Lec_env)"`

## NLTK로 영어 토큰화

- nltk 설치 : 파이썬에서 자연어 처리를 쉽게 할 수 있게 해주는 라이브러리
    - `pip -q install nltk`

## 한국어 형태소 분석(KoNLPy:Okt)

- JPype 설치
    - `pip install JPype1`
- KoNLPy 설치
    - `pip install konlpy`
- transFormers 설치
    - `pip install transformers`

## 서브워드 토큰화(Hugging Face Transformers)

- transformers 설치
    - `pip -q install transformers`

## 영어 품사 태깅(SpaCy)

- spacy 설치
    - `pip -q install spacy`
- en_core_web_sm 설치
    - `python -m spacy download en_core_web_sm`
