# Giggle Official Skills

[English](./README.md) | [简体中文](./README.zh-CN.md) | [日本語](./README.ja.md) | 한국어 | [繁體中文](./README.zh-TW.md)

[Giggle.pro](https://giggle.pro/) 기반 AI 생성 스킬 라이브러리. 이미지, 비디오, 음악, 음성, 음성 클론, 스크립트 등을 포함합니다.

## `npx skills add`로 설치

```bash
# GitHub 저장소에서 모든 스킬 나열
npx skills add giggle-official/skills --list --full-depth

# GitHub 저장소에서 특정 스킬 설치
npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y

# GitHub 저장소에서 전체 설치
npx skills add giggle-official/skills

# 로컬 개발 (본 저장소 디렉터리에서 실행)
npx skills add . --list --full-depth
```

## 특징

- 🎨 **멀티모달 AI**: 이미지, 비디오, 음악, 음성, 음성 클론, 스크립트 생성을 한 곳에서 처리.
- 🎬 **비디오 제작**: 문생비디오, 도생비디오, 단편, 드라마, MV 전체 워크플로 지원.
- 📝 **스토리와 스크립트**: 강문식 내러티브 스타일로 분장 개요와 대본 생성.
- 🔐 **로컬 우선**: 스킬은 로컬에서 실행되며, API Key는 시스템 환경 변수 `GIGGLE_API_KEY`에서 읽습니다.

## 사용 가능한 스킬

| 이름 | 설명 | 문서 | 설치 명령 |
|------|------|------|----------|
| giggle-generation-image | 문생도와 도생도. Seedream, Midjourney, Nano Banana 지원. 화면 비율과 해상도 커스터마이즈 가능. | [SKILL.md](./skills/giggle-generation-image/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y` |
| giggle-generation-video | 텍스트→비디오 및 이미지→비디오 변환(시작 프레임/종료 프레임) 지원. 텍스트나 이미지를 영상으로 바꿔야 하는 사용자에게 적합. | [SKILL.md](./skills/giggle-generation-video/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-video -y` |
| giggle-seedance2-gen | Giggle API로 Seedance 2.0(Pro/Fast) 영상 생성. 텍스트→영상, 이미지→영상, 옴니(멀티모달). 프롬프트 최적화 가이드 포함. 트리거: Seedance, AI 영상, 문생영상, 도생영상. | [SKILL.md](./skills/giggle-seedance2-gen/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-seedance2-gen -y` |
| giggle-generation-drama | 사용자가 영상을 만들고, 단편을 촬영하거나, 사용 가능한 영상 스타일을 볼 때 사용. 트리거: 단편 영화, 영상 만들기, 숏폼 촬영, AI 영상, 스토리로 영상 만들기, 단편 드라마, 나레이션 영상, 시네마틱 영상, 사용 가능한 영상 스타일 | [SKILL.md](./skills/giggle-generation-drama/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-drama -y` |
| giggle-generation-aimv | AI 뮤직 비디오(MV). 텍스트 프롬프트나 사용자 정의 가사로 음악 생성 후 참조 이미지로 가사 비디오 제작. | [SKILL.md](./skills/giggle-generation-aimv/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-aimv -y` |
| giggle-generation-music | 텍스트 설명, 사용자 정의 가사 또는 순수 악기로 AI 음악 생성. 간소화, 사용자 정의, 순수 악기 세 가지 모드 지원. | [SKILL.md](./skills/giggle-generation-music/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-music -y` |
| giggle-generation-speech | Giggle.pro 문전음을 통해 텍스트를 AI 음성으로 합성. 다양한 음색, 감정, 말속도 지원. | [SKILL.md](./skills/giggle-generation-speech/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-speech -y` |
| giggle-voice-clone | 음성 클론. 참조 오디오 URL에서 음성을 클론하고 해당 음성으로 텍스트 합성. | [SKILL.md](./skills/giggle-voice-clone/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-voice-clone -y` |
| giggle-generation-scripts | 강문식 중국어 스크립트 생성: 줄거리, 인물 소개, 분장 개요, 대사와 연출 포함 분장 극본. | [SKILL.md](./skills/giggle-generation-scripts/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-scripts -y` |

## 빠른 검증

예: 사용 가능한 TTS 음색 확인 (`GIGGLE_API_KEY` 설정 필요):

```bash
cd skills/giggle-generation-speech
python3 scripts/text_to_audio_api.py --list-voices
```

## Giggle API Key (필수)

[Giggle.pro](https://giggle.pro/)에 로그인한 뒤 **왼쪽 사이드바**의 **API Key**(**API 密钥**)에서 키를 생성하거나 복사해 시스템 환경 변수에 설정하세요:

```bash
export GIGGLE_API_KEY=your_api_key
```

모든 스킬은 시스템 환경 변수에서 `GIGGLE_API_KEY`를 읽습니다.

```yaml:skills-data
skills:
  - name: "단편 드라마"
    value: "giggle-generation-drama"
    description: "사용자가 영상을 만들고, 단편을 촬영하거나, 사용 가능한 영상 스타일을 볼 때 사용. 트리거: 단편 영화, 영상 만들기, 숏폼 촬영, AI 영상, 스토리로 영상 만들기, 단편 드라마, 나레이션 영상, 시네마틱 영상, 사용 가능한 영상 스타일"
    category: video
    version: "0.0.1"
  - name: "음악 MV"
    value: "giggle-generation-aimv"
    description: "사용자가 AI 뮤직 비디오(MV) 생성을 원할 때 사용. 텍스트 프롬프트로 음악 생성 또는 사용자 정의 가사 사용. 트리거: MV 생성, 뮤직 비디오, 가사 비디오, AI MV, 가사로 비디오 생성."
    category: video
    version: "0.0.1"
  - name: "이미지 생성"
    value: "giggle-generation-image"
    description: "문생도와 도생도 지원. 사용자가 이미지 생성이 필요할 때 사용. (1) 텍스트 설명으로 생성, (2) 참조 이미지로 생성, (3) 모델, 화면 비율, 해상도 커스터마이즈. 트리거: 이미지 생성, AI 아트."
    category: image
    version: "0.0.1"
  - name: "음악 생성"
    value: "giggle-generation-music"
    description: "사용자가 음악 생성, 작곡을 원할 때 사용. 텍스트 설명, 사용자 정의 가사, 순수 악기 BGM 모두 지원. 트리거: 음악 생성, 작곡, AI 음악, BGM, 가사 음악, beats 제작."
    category: music
    version: "0.0.1"
  - name: "극본 생성"
    value: "giggle-generation-scripts"
    description: "강문 영화의 내러티브 진행과 대사 메커니즘에 기반해 중국어 스크립트 생성. 스크립트 생성, 분장 작성, 대본, 극본 수정 등 의도에 사용. 줄거리, 인물 소개, 분장 개요, 대사·연출 포함 분장 극본 출력. 시대 배경, 인물 관계, 갈등 리듬, 결말 조정 가능."
    category: script
    version: "0.0.1"
  - name: "음성・더빙"
    value: "giggle-generation-speech"
    description: "사용자가 음성 생성, 더빙, 텍스트 음성 변환을 원할 때 사용. Giggle.pro 문전음 API로 텍스트를 AI 음성으로 합성. 트리거: 음성 생성, 문전음, TTS, 더빙, 합성 음성."
    category: voice
    version: "0.0.1"
  - name: "음성 클론"
    value: "giggle-voice-clone"
    description: "사용자가 오디오 샘플에서 음성을 클론할 때 사용. 참조 오디오 URL을 voice-clone에 전달한 후 해당 음성으로 텍스트 합성. 트리거: 음성 클론, 내 음성 클론, 오디오에서 음성 클론."
    category: voice
    version: "0.0.1"
  - name: "비디오 생성"
    value: "giggle-generation-video"
    description: "텍스트→비디오 및 이미지→비디오 변환(시작 프레임/종료 프레임) 지원. 텍스트나 이미지를 영상으로 바꿔야 하는 사용자에게 적합."
    category: video
    version: "0.0.1"
  - name: "영상 생성 (Seedance 2.0)"
    value: "giggle-seedance2-gen"
    description: "Giggle API로 Seedance 2.0(Pro/Fast) 영상 생성: 텍스트→영상, 이미지→영상, 옴니 멀티모달. 사용자 입력 언어에 맞게 프롬프트 최적화 후 API 호출. 트리거: 영상 생성, AI 영상, Seedance, 이미지→영상, 텍스트→영상, 비디오 생성."
    category: video
    version: "1.0.0"
  - name: "이미지 생성 (gpt-image-2)"
    value: "giggle-gpt-image-2"
    description: "GPT-Image-2에 적합한 고품질 프롬프트 생성을 도와주며, 프롬프트 생성 후 Giggle API를 직접 호출하여 `gpt-image-2-fast`로 이미지를 생성합니다."
    category: image
    version: "0.0.1"
```
