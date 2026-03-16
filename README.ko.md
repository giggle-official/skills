# Giggle Official Skills

[English](./README.md) | [简体中文](./README.zh-CN.md) | [日本語](./README.ja.md) | 한국어 | [繁體中文](./README.zh-TW.md)

[Giggle.pro](https://giggle.pro/) 기반 AI 생성 스킬 라이브러리. 이미지, 비디오, 음악, 음성, 스크립트 등을 포함합니다.

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

- 🎨 **멀티모달 AI**: 이미지, 비디오, 음악, 음성, 스크립트 생성을 한 곳에서 처리.
- 🎬 **비디오 제작**: 문생비디오, 도생비디오, 단편, 드라마, MV 전체 워크플로 지원.
- 📝 **스토리와 스크립트**: 강문식 내러티브 스타일로 분장 개요와 대본 생성.
- 🔐 **로컬 우선**: 스킬은 로컬에서 실행되며, API Key는 시스템 환경 변수 `GIGGLE_API_KEY`에서 읽습니다.

## 사용 가능한 스킬

| 이름 | 설명 | 문서 | 설치 명령 |
|------|------|------|----------|
| giggle-generation-image | 문생도와 도생도. Seedream, Midjourney, Nano Banana 지원. 화면 비율과 해상도 커스터마이즈 가능. | [SKILL.md](./skills/giggle-generation-image/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y` |
| giggle-generation-video | 문생비디오와 도생비디오(시작/종료 프레임). Grok, Sora2, Veo, Kling 등 지원. 모델, 길이, 화면 비율 커스터마이즈 가능. | [SKILL.md](./skills/giggle-generation-video/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-video -y` |
| giggle-generation-drama | 스토리로부터 단편, 드라마, 해설 비디오 생성. 에피소드, 해설, 단편 세 가지 모드 지원. | [SKILL.md](./skills/giggle-generation-drama/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-drama -y` |
| giggle-generation-aimv | AI 뮤직 비디오(MV). 텍스트 프롬프트나 사용자 정의 가사로 음악 생성 후 참조 이미지로 가사 비디오 제작. | [SKILL.md](./skills/giggle-generation-aimv/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-aimv -y` |
| giggle-generation-music | 텍스트 설명, 사용자 정의 가사 또는 순수 악기로 AI 음악 생성. 간소화, 사용자 정의, 순수 악기 세 가지 모드 지원. | [SKILL.md](./skills/giggle-generation-music/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-music -y` |
| giggle-generation-speech | Giggle.pro 문전음을 통해 텍스트를 AI 음성으로 합성. 다양한 음색, 감정, 말속도 지원. | [SKILL.md](./skills/giggle-generation-speech/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-speech -y` |
| giggle-generation-scripts | 강문식 중국어 스크립트 생성: 줄거리, 인물 소개, 분장 개요, 대사와 연출 포함 분장 극본. | [SKILL.md](./skills/giggle-generation-scripts/SKILL.md) | `npx skills add giggle-official/skills --full-depth --skill giggle-generation-scripts -y` |

## 빠른 검증

예: 사용 가능한 TTS 음색 확인 (`GIGGLE_API_KEY` 설정 필요):

```bash
cd skills/giggle-generation-speech
python3 scripts/text_to_audio_api.py --list-voices
```

## Giggle API Key (필수)

[Giggle.pro](https://giggle.pro/)에서 API Key를 받아 시스템 환경 변수에 설정하세요:

```bash
export GIGGLE_API_KEY=your_api_key
```

모든 스킬은 시스템 환경 변수에서 `GIGGLE_API_KEY`를 읽습니다.

```yaml:skills-data
skills:
  - name: giggle-generation-drama
    description: 사용자가 비디오 생성, 단편 촬영, 사용 가능한 비디오 스타일 확인을 원할 때 사용. 트리거: 단편, 비디오 제작, AI 비디오, 스토리로 비디오 생성, 단편 드라마, 해설 비디오, 영화감 비디오.
    category: video
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-drama -y"
  - name: giggle-generation-aimv
    description: 사용자가 AI 뮤직 비디오(MV) 생성을 원할 때 사용. 텍스트 프롬프트로 음악 생성 또는 사용자 정의 가사 사용. 트리거: MV 생성, 뮤직 비디오, 가사 비디오, AI MV, 가사로 비디오 생성.
    category: video
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-aimv -y"
  - name: giggle-generation-image
    description: 문생도와 도생도 지원. 사용자가 이미지 생성이 필요할 때 사용. (1) 텍스트 설명으로 생성, (2) 참조 이미지로 생성, (3) 모델, 화면 비율, 해상도 커스터마이즈. 트리거: 이미지 생성, AI 아트.
    category: image
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-image -y"
  - name: giggle-generation-music
    description: 사용자가 음악 생성, 작곡을 원할 때 사용. 텍스트 설명, 사용자 정의 가사, 순수 악기 BGM 모두 지원. 트리거: 음악 생성, 작곡, AI 음악, BGM, 가사 음악, beats 제작.
    category: music
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-music -y"
  - name: giggle-generation-scripts
    description: 강문 영화의 내러티브 진행과 대사 메커니즘에 기반해 중국어 스크립트 생성. "스크립트 생성", "분장 작성", "대본", "극본 수정" 등 의도에 사용. 줄거리, 인물 소개, 분장 개요, 대사·연출 포함 분장 극본 출력. 시대 배경, 인물 관계, 갈등 리듬, 결말 조정 가능.
    category: script
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-scripts -y"
  - name: giggle-generation-speech
    description: 사용자가 음성 생성, 더빙, 텍스트 음성 변환을 원할 때 사용. Giggle.pro 문전음 API로 텍스트를 AI 음성으로 합성. 트리거: 음성 생성, 문전음, TTS, 더빙, 합성 음성.
    category: voice
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-speech -y"
  - name: giggle-generation-video
    description: 문생비디오와 도생비디오(시작/종료 프레임) 지원. 사용자가 비디오 생성, 숏폼 제작, 문전비디오가 필요할 때 사용. (1) 텍스트 설명으로 비디오 생성, (2) 참조 이미지를 시작/종료 프레임으로 비디오 생성, (3) 모델, 화면 비율, 길이, 해상도 커스터마이즈. 트리거: 비디오 생성, 문생비디오, 도생비디오, AI 비디오, text-to-video, image-to-video.
    category: video
    version: "0.0.1"
    value: "npx skills add giggle-official/skills --full-depth --skill giggle-generation-video -y"
```
