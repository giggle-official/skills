# TV Avatar voice catalog

Bilingual reference sourced from the `voice_list.md` API payload. Every entry lists **name**, **tags**, English + **Chinese descriptions**, and **`voiceoverId`**.

- **Unique voices after merge**: 88
- **Merge rule**: When the source file contains multiple voice blocks, entries merge on `voiceoverId`; later rows win on duplicates.
- **Tag IDs**: `1` → UGC (user-generated content); `2` → Advertisement; `102` → Cartoon & animals; `103` → Influencer / KOL

### API pagination snapshot

| Idx | total | pageNo | pageSize | rows |
|-----|-------|--------|----------|------|
| 0 | 308 | 1 | 50 | 50 |
| 3 | 848 | 1 | 50 | 50 |

## Field reference

| Field | JSON key | Notes |
|-------|----------|-------|
| Name | `name` | Display label as shown in console |
| Tags | `tags` | Numeric tag id; legend above |
| Description | `voiceoverDesc` | English from API + localized Chinese line |
| Voice ID | `voiceoverId` | Value to pass as `voice_over_id` |

---

### 1. 🇦🇷Sofi

- **voiceoverId** / **Voice ID**:`3zXrTeLKZNHgK2hgp9xbeX4RgJ16R42T`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A 30-something female with an Argentinian accent, suitable for social media
- **Description (ZH)**:
  - 三十多岁的女性，阿根廷口音，适合社交媒体。

### 2. 🇦🇷Valeria

- **voiceoverId** / **Voice ID**:`Mim3O14UTtW7dRqURbZ4zLtmyPrMEgiQ`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - Young feminine woman voice, Spanish with Argentinian accent. Suitable for Social media content.
- **Description (ZH)**:
  - 年轻女性化嗓音，西班牙语阿根廷口音，适合社交媒体内容。

### 3. 🇧🇷Camila

- **voiceoverId** / **Voice ID**:`UF1JLIWqAVm3NMo3lDtzu33Yrcfz8FUG`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - The voice of a young woman in her 20s, with a Brazilian accent, natural timbre and a hint of joy, suitable for sharing real everyday goodies
- **Description (ZH)**:
  - 二十多岁巴西口音女声，音色自然带愉悦感，适合分享真实日常好物。

### 4. 🇧🇷Diego

- **voiceoverId** / **Voice ID**:`ztOBcJEf4ahJp5ZRHmdJcWKCGjjQtkUl`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - Male in his 20s. Young and modern. Brazilian with a dynamic voice. Great for Narration, content creation, and commercial Voice Over.
- **Description (ZH)**:
  - 二十多岁巴西男声，年轻现代，动感有力，适合旁白、内容创作与商业配音。

### 5. 🇧🇷Guestavo Barros

- **voiceoverId** / **Voice ID**:`Emi3eu6Vf4pLicp64BCsYhGDDhAqD0Vm`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A Young Brazilian man with a slightly hoarse voice. Voice works well for TV Ads & other commercials.
- **Description (ZH)**:
  - 年轻的巴西男性，嗓音略带沙哑，适合电视广告及其他商业广告。

### 6. 🇧🇷Keren

- **voiceoverId** / **Voice ID**:`wJWrOuJTW8o64wI6QLMdutbge3SvIWjx`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - Young female with a sweet and pleasant voice, embodying the vibrant energy typical of someone in their twenties. With a perfectly rhythmic tone, the voice is ideal for narrating scripts and stories,
- **Description (ZH)**:
  - 甜美悦耳的年轻女声，富有二十多岁的朝气，节奏感强，适合脚本与故事叙述。（接口文案末尾逗号保留）

### 7. 🇧🇷Leonardo Hamaral

- **voiceoverId** / **Voice ID**:`t5CvF7LX0gZYOXPMctoYUmlmcMc8uekb`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - Medium-low male voice. Great for retail voiceover or perfect for recording commercials.
- **Description (ZH)**:
  - 中低音男声，适合零售画外音或广告录制。

### 8. 🇧🇷Otto de La Luna

- **voiceoverId** / **Voice ID**:`CIcbIVSolW5dDq40YhaeVsVbEI4GOuZG`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young and epic voice. Perfect and excited to record videos talking about anime.
- **Description (ZH)**:
  - 年轻、富有史诗感的声线，适合兴奋地录制动漫相关内容。

### 9. 🇪🇸Enrique M. Nieto

- **voiceoverId** / **Voice ID**:`1TIL3CgoYuc4A46gEUIfgdwYkqQlPm44`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - Natural and authentic male voice with Spanish accent, suitable for social media influencers to share product advertisements
- **Description (ZH)**:
  - 自然真实的西语男声，适合达人分享产品广告。

### 10. 🇪🇸Juan

- **voiceoverId** / **Voice ID**:`tfZ13wa1w41CW2w2PQELAZPwRv33Q1I7`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - The voice of a middle-aged man in his 30s with a Spanish accent. The tone is natural, real and gentle, suitable for real daily sharing
- **Description (ZH)**:
  - 三十多岁西语口音男声，语气自然真实柔和，适合真实日常分享。

### 11. 🇪🇸Oliver

- **voiceoverId** / **Voice ID**:`8zHMRagfQPEKyfWUdSFjh6dohMUQADj4`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - Deep, clear and expressive male voice with a neutral Spanish accent, belonging to a 40-year-old podcaster from Spain who speaks in a standard Castilian.
- **Description (ZH)**:
  - 低沉清晰、表现力强的中性西班牙口音男声，贴近一位 40 岁、标准卡斯蒂利亚语的西班牙播客主播。

### 12. 🇪🇸Ricardo

- **voiceoverId** / **Voice ID**:`BSElOGJTwIrD1BvOwlSdygAziGvEIjOg`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - Mature and magnetic male voice with Spanish accent, suitable for brand advertising
- **Description (ZH)**:
  - 成熟有磁性的西语男声，适合品牌广告。

### 13. 🇪🇸Yolanda

- **voiceoverId** / **Voice ID**:`Pyb03ljV8AndjASQ24Hj301Ga7d0CxHQ`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A youthful, soothing, and calm Spanish female accent, suitable for everyday video sharing content.
- **Description (ZH)**:
  - 年轻轻柔舒缓的西语女声，适合日常视频分享。

### 14. 🇫🇷Adina

- **voiceoverId** / **Voice ID**:`fqGzwUPPMzBREmw2o8TwtDrS5sDlVCdG`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - Clear voice of a young professional French teen girl. Suitable for Social Media.
- **Description (ZH)**:
  - 清晰的专业感法语少女音，适合社交媒体。

### 15. 🇫🇷Clara

- **voiceoverId** / **Voice ID**:`UuvJ1hheF7UfPcDFZpIXdcJRBCmeDRYg`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A middle aged male French voice, with a standard French accent, natural, suitable for the rhythm of short videos
- **Description (ZH)**:
  - 中年法语男声，标准法式口音，自然，契合短视频节奏。

### 16. 🇫🇷Corentin

- **voiceoverId** / **Voice ID**:`xhT7yXc3OmpuB8jfdafE2U2vjPoQteHM`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A dynamic young French male voice. Perfect for short-form videos and social media.
- **Description (ZH)**:
  - 动感年轻的法语男声，适合短视频与社交媒体。

### 17. 🇫🇷Darine

- **voiceoverId** / **Voice ID**:`zOXnCaLxRSOlifwan0ckY8gkwBkjYL6n`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - Middle age female French voice. Perfect for Informative & Educational
- **Description (ZH)**:
  - 中年法语女声，适合资讯与教育类内容。

### 18. 🇫🇷Guillaume

- **voiceoverId** / **Voice ID**:`xeAf373jyJnguJvL5UcMOABfIiyx9xNA`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - The voice of a middle-aged male in his 40s, with a standard French accent, natural, slightly fast speaking speed, suitable for the rhythm of short videos
- **Description (ZH)**:
  - 四十岁左右标准法式口音男声，自然，语速略快，契合短视频节奏。

### 19. 🇫🇷Jeanne

- **voiceoverId** / **Voice ID**:`9YALZum0OVkl6JJA3ADGDogHZiXYJ7m3`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young Parisian French woman's voice, perfect for your narrative, educational, and entertainment projects.
- **Description (ZH)**:
  - 年轻巴黎法语女声，适合叙事、教育与娱乐类项目。

### 20. 🇫🇷Nicolas

- **voiceoverId** / **Voice ID**:`IselOLqVIRC2p5C9QgRkAywf8mqooKBQ`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - The voice of a middle-aged male in his 40s, with a standard French accent, an upward tone, and a hint of happiness, suitable for short video product introductions
- **Description (ZH)**:
  - 四十岁左右标准法式口音男声，语调上扬略带欢快，适合短视频产品介绍。

### 21. 🇬🇧Dave

- **voiceoverId** / **Voice ID**:`b0435ababe614aef9170bb861b3cecd6`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A British man with a deep voice, suitable for explaining digital 3C products
- **Description (ZH)**:
  - 英式低沉男声，适合讲解数码 3C 产品。

### 22. 🇬🇧Leo

- **voiceoverId** / **Voice ID**:`abvFq234SBfPnn4n1zAOx5ZLdqi19Dgy`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - The voice of a young, energetic, cheerful man with a British accent, natural timbre, full of energy, rising tone, and a slight sense of happiness, suitable for short video product introductions
- **Description (ZH)**:
  - 年轻有活力、开朗的英式男声，音色自然，能量足、语调上扬略欢快，适合短视频产品介绍。

### 23. 🇮🇳Alia

- **voiceoverId** / **Voice ID**:`UpL4FwUhE3E8hudb8FJJC3UDCIuVtBSz`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - Muskaan is the pen name of a very experienced financial trainer in India. Her voice is very natural and feels relatable, unlike the corporate tone that often feels disconnected. This voice will be ver
- **Description (ZH)**:
  - Muskaan 是一位资深印度金融培训师使用的笔名。她的声音非常自然、有亲和力，不像常见的疏离「企业腔」。接口返回文案在此处截断为「ver」。

### 24. 🇮🇳Mira

- **voiceoverId** / **Voice ID**:`yM1tlhrAMHD1u6CK5KpJOMGZeLRN1xoW`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young Indian female voice, authentic and natural, suitable for social media
- **Description (ZH)**:
  - 年轻印度女声，真实自然，适合社交媒体。

### 25. 🇮🇳Natasha

- **voiceoverId** / **Voice ID**:`DopuUpxTErIYTaENhlua6HUr4yDpXwRx`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - The Hindi voiceover brings a lively and engaging energy to the narrative, perfectly tailored for the vibrant world of social media, entertainment, and television. It exudes a pleasant and excited tone
- **Description (ZH)**:
  - 印地语配音叙事活泼抓耳，契合社交媒体、娱乐与电视领域；整体语气愉悦、富有兴奋感。接口返回文案在此处截断。

### 26. 🇮🇳Rahul

- **voiceoverId** / **Voice ID**:`p84vvVz523388EBpmDfmoxTywMCh2ECu`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - Confident mature Indian male voice for Audiobooks, podcasts, documentary, advertising and more.
- **Description (ZH)**:
  - 自信成熟的印度男声，适合有声书、播客、纪录片、广告等。

### 27. 🇮🇳Saira

- **voiceoverId** / **Voice ID**:`zaShOIQ90cnYFhv9T7IK4jHUcXDO5YPj`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - Saira is a pen name of a very talented Indian actress. That is why in her voice you will find all emotions, making this voice very natural. Therefore, use cases can include a bot for natural conversat
- **Description (ZH)**:
  - Saira 是一位才华横溢的印度女演员使用的笔名，因此声音情感层次丰富、非常自然；接口文案在此处截断，典型用途包括自然对话类机器人等场景。

### 28. 🇮🇹Francesco

- **voiceoverId** / **Voice ID**:`hRgeoCp52YVHBw2APRiELT8oNZDsa3Sn`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - A premium young Italian male voice, calm and Deep recorded in High quality.
- **Description (ZH)**:
  - 高品质录制的优质年轻意大利男声，沉稳偏低沉。

### 29. 🇮🇹Leandro

- **voiceoverId** / **Voice ID**:`VjH0jJCaRwbSyUlLKSz2lIoz8hPyYbeh`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - Middle aged Italian male voice. Great for social media content.
- **Description (ZH)**:
  - 中年意大利男声，适合社交媒体内容。

### 30. 🇮🇹Linda Fiore

- **voiceoverId** / **Voice ID**:`dHtEl0us5FOO7xYSaVmoyaW8esM2uH4c`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, dynamic and cheerful woman's voice. Perfect for audiobooks, advertising, podcasts.
- **Description (ZH)**:
  - 年轻动感开朗的女声，适合有声书、广告与播客。

### 31. 🇮🇹Luna

- **voiceoverId** / **Voice ID**:`cQaRiNd59fhERdoHkivfcdtAORDLYofQ`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - Young Italian female voice. Perfect for narration.
- **Description (ZH)**:
  - 年轻意大利女声，适合旁白叙事。

### 32. 🇲🇦Amina

- **voiceoverId** / **Voice ID**:`SL85D32MYiZq9AvAZa3h8ECfcbZ48UJ7`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A Moroccan woman in her 20s who speaks French and has a calm tone suitable for social media
- **Description (ZH)**:
  - 二十多岁的摩洛哥女性，说法语，语气沉稳，适合社交媒体。

### 33. 🇲🇦Fatima

- **voiceoverId** / **Voice ID**:`F2WAQuCkOxVmDVmZfAOwDN6ZmwH1gMNI`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A Moroccan woman in her 20s who speaks Arabic and has a calm tone suitable for social media
- **Description (ZH)**:
  - 二十多岁的摩洛哥女性，说阿拉伯语，语气沉稳，适合社交媒体。

### 34. 🇲🇦Yasir

- **voiceoverId** / **Voice ID**:`XATDcuIf6o30I41yAtMBxW1ukOf5WWRW`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young man in his 20s, speaking with a Moroccan accent and an excited tone, introducing products suitable for young people
- **Description (ZH)**:
  - 二十多岁摩洛哥口音男声，语气兴奋，适合面向年轻人的产品介绍。

### 35. 🇲🇽Andromeda

- **voiceoverId** / **Voice ID**:`2NLslhxYEf9h9QQOQlGwVVtI427nls9e`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A middle-aged woman in her 40s with a Mexican accent and a calm tone, introducing and sharing products suitable for household use
- **Description (ZH)**:
  - 四十岁左右墨西哥口音女性，语气沉稳，适合介绍与分享家居类产品。

### 36. 🇲🇽Memo

- **voiceoverId** / **Voice ID**:`z25oIqCmBdS3rklwsSTeyEpeBD9BqKFg`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - Young male with a neutral Elegant Latin-American accent. Great for commercials and advertisements.
- **Description (ZH)**:
  - 中性优雅的拉美口音年轻男声，适合商业广告。

### 37. 🇲🇽Zabra

- **voiceoverId** / **Voice ID**:`ulQJvfwYE6uPQGNF1tx6KSyS9go0CjRi`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - Young Mexican commercial radio host. Voice is suitable for Ads.
- **Description (ZH)**:
  - 年轻墨西哥商业电台主播风格，适合广告。

### 38. 🇳🇱Pieter

- **voiceoverId** / **Voice ID**:`O98Ai5RwBxvkRkTzfdt0MYryAuZrKngn`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - Young male in his early 20s with a Dutch accent, suitable for real buyer show sharing, suitable for formal and serious product sharing
- **Description (ZH)**:
  - 二十岁出头的荷兰口音男声，适合真实买家秀；亦适合正式、严肃向产品讲解。

### 39. 🇸🇦Layla

- **voiceoverId** / **Voice ID**:`s7E3GXpHNh8ffNqKA7mN5L94b9P2haSy`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A 30-something female speaking Arabic, speaking in a fast pace, suitable for social media
- **Description (ZH)**:
  - 三十多岁的女性，阿拉伯语，语速较快，适合社交媒体。

### 40. 🇺🇸 Carson

- **voiceoverId** / **Voice ID**:`LaaHTrXZCVOQmB1wZUhnwmbPTAWDFtW6`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, energetic male voice with an American accent, suitable for social media video content creation.
- **Description (ZH)**:
  - 年轻有活力的美式男声，适合社交媒体视频创作。

### 41. 🇺🇸 Dahlia

- **voiceoverId** / **Voice ID**:`M7qjuXIMHC2rk0K1puvZqmXHT33buTBR`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A vibrant, professional, and confident female American accent, suitable for product sharing and daily video sharing content.
- **Description (ZH)**:
  - 明快、专业且自信的美式女声，适合好物分享与日常视频。

### 42. 🇺🇸 Violet

- **voiceoverId** / **Voice ID**:`zeeTdrCqbhpVKOucLtOKdhytM7rbJx5t`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A vibrant, professional, and confident female American accent, suitable for product sharing and daily video sharing content.
- **Description (ZH)**:
  - 明快、专业且自信的美式女声，适合好物分享与日常视频。

### 43. 🇺🇸Addison

- **voiceoverId** / **Voice ID**:`WRr1XhwJEv22qUhWD1zJapNCQH2pn6gv`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A youthful, soothing, and calm American female accent, suitable for everyday video sharing content
- **Description (ZH)**:
  - 年轻轻柔舒缓的美式女声，适合日常视频分享。

### 44. 🇺🇸Alex

- **voiceoverId** / **Voice ID**:`izUpv1NNORS4rDDi1CUdtfDtMfrJEDw8`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - Older American male voice. American accent, natural voice, suitable for short video product introduction and daily short video sharing.
- **Description (ZH)**:
  - 偏年长的美式男声，自然音色，适合短视频产品介绍与日常分享。

### 45. 🇺🇸Amelia

- **voiceoverId** / **Voice ID**:`vkyikkoPImGofMUHKrjV9VF9Peu7ICfR`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A youthful, bright, and exuberant female American accent, suitable for product sharing content
- **Description (ZH)**:
  - 年轻明亮、外放的美式女声，适合好物分享。

### 46. 🇺🇸Andre

- **voiceoverId** / **Voice ID**:`7X8AdxHX8Kkskjmjy3ZIyzj5FXklkNT5`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - Young male in his early 20s with an American accent and a slight hip-hop style, suitable for real buyer show sharing
- **Description (ZH)**:
  - 二十岁出头、略带嘻哈风格的美式男声，适合真实买家秀分享。

### 47. 🇺🇸Arnold

- **voiceoverId** / **Voice ID**:`63858aac525540e9aaa6bce4c1c05633`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - An emotional middle-aged male voice, very powerful, very suitable for short videos
- **Description (ZH)**:
  - 富有情绪感染力的中年男声，力量感强，很适合短视频。

### 48. 🇺🇸Arnold(new)

- **voiceoverId** / **Voice ID**:`OxyLonkDSRb9eSH6T8KYlfgoeHQsyl0t`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - An emotional middle-aged male voice, very powerful, very suitable for short videos
- **Description (ZH)**:
  - 富有情绪感染力的中年男声，力量感强，很适合短视频。

### 49. 🇺🇸Brendan

- **voiceoverId** / **Voice ID**:`7735cabc62b240cd960b26b23a964f8f`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - A very youthful and energetic male voice, very suitable for making digital 3C short videos
- **Description (ZH)**:
  - 非常年轻有活力的男声，很适合数码 3C 类短视频。

### 50. 🇺🇸Caleb

- **voiceoverId** / **Voice ID**:`yFC4BhutK8zN6sLtLKf0kGEL9Mh3neYR`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, steady American male voice, suitable for creating content for social media videos.
- **Description (ZH)**:
  - 年轻稳健的美式男声，适合社交媒体视频创作。

### 51. 🇺🇸Casey

- **voiceoverId** / **Voice ID**:`2XudKVbLKn1BVywjYgKEGFuZD1Zx3v77`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young male voice with a standard American accent, confident and full of energy. Perfect for social media content.
- **Description (ZH)**:
  - 标准美式年轻男声，自信有活力，适合社交媒体内容。

### 52. 🇺🇸Charles

- **voiceoverId** / **Voice ID**:`N6k2uunugb50fQg0v4A3Ij6mU1T5IvRP`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, brisk and energetic male voice with an American accent, suitable for sharing good products and promotional content.
- **Description (ZH)**:
  - 轻快有活力的美式年轻男声，适合好物分享与促销类内容。

### 53. 🇺🇸Cole

- **voiceoverId** / **Voice ID**:`ElpEYEDy0u5WkMohrtVm1WC3HXkZeQvB`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A dynamic young male voice with an American accent and a natural timbre, perfect for storytelling and creating social media video content.
- **Description (ZH)**:
  - 美式口音、音色自然的年轻动感男声，适合讲故事与社交媒体视频创作。

### 54. 🇺🇸Eamon

- **voiceoverId** / **Voice ID**:`9lV3fRxvTpVxtJA6qSReBquOzScpeDEy`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, enthusiastic, and energetic standard American male voice, suitable for daily video sharing content, with an empty indoor echo.
- **Description (ZH)**:
  - 年轻热情有活力的标准美式男声，适合日常分享；带空旷室内混响感。

### 55. 🇺🇸Elysia

- **voiceoverId** / **Voice ID**:`cQdKhMsrc9orx2BPnVigdndufXUx7sxS`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - Young, bright, and enthusiastic standard American female voice with an empty outdoor echo, suitable for daily video sharing content.
- **Description (ZH)**:
  - 年轻明亮热情的标准美式女声，带空旷室外混响感，适合日常分享。

### 56. 🇺🇸Ethan

- **voiceoverId** / **Voice ID**:`roGysrT2aTH2MhftOhDdFuZfUdZCcV8H`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young American male with an American accent, natural voice and a hint of joy, suitable for sharing real daily good things and short video product introductions
- **Description (ZH)**:
  - 年轻美式男声，自然带一丝愉悦，适合真实日常好物分享与短视频产品介绍。

### 57. 🇺🇸Eulalia

- **voiceoverId** / **Voice ID**:`gPVnZSTBT3FlP9ltDSE94Zfp0jNnNDgn`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - An older, cheerful American female voice. American accent, natural and confident, suitable for daily video sharing and product video introductions
- **Description (ZH)**:
  - 偏年长但开朗的美式女声，自然自信，适合日常分享与产品介绍视频。

### 58. 🇺🇸Fin

- **voiceoverId** / **Voice ID**:`0f90fb5bad58446f95e18960cdec21a5`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - A middle-aged and humorous male voice, sounds very suitable for funny stories
- **Description (ZH)**:
  - 中年幽默男声，很适合搞笑故事类内容。

### 59. 🇺🇸Frank

- **voiceoverId** / **Voice ID**:`nUoSlBV5r5VzhaccnD70owPV1fgn4pzz`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - A young, stable male voice with an American accent, suitable for creating content for social media videos.
- **Description (ZH)**:
  - 年轻沉稳的美式男声，适合社交媒体视频创作。

### 60. 🇺🇸Haroldo

- **voiceoverId** / **Voice ID**:`rkEVRNGky8HOKR0vit5L0pqzkXkUCrR8`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - Middle aged male with a Mexican Spanish accent. Perfect for Narrations.
- **Description (ZH)**:
  - 墨西哥西语口音的中年男声，适合叙事旁白。

### 61. 🇺🇸Harper

- **voiceoverId** / **Voice ID**:`2r69IyOA7qyj1TKr11LiCXUGcPhsSYTW`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A youthful, professional, confident, and natural American accent, suitable for daily video sharing.
- **Description (ZH)**:
  - 年轻专业、自信自然的美式口音，适合日常短视频分享。

### 62. 🇺🇸Jorja

- **voiceoverId** / **Voice ID**:`aM7j6BScW3cl5cxCzshNBMcNuwmuX7Ym`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, enthusiastic, and friendly standard American female voice with an empty outdoor echo, suitable for social media video creation content.
- **Description (ZH)**:
  - 年轻热情友好的标准美式女声，带空旷室外混响感，适合社交媒体视频创作。

### 63. 🇺🇸Kayla

- **voiceoverId** / **Voice ID**:`u92i4JU2cqSU9HKY0PemWE6JnEPyAXJ4`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - Young, energetic American female voice, suitable for daily video sharing and product video introduction
- **Description (ZH)**:
  - 年轻有活力的美式女声，适合日常分享与产品介绍视频。

### 64. 🇺🇸Kenneth

- **voiceoverId** / **Voice ID**:`lDDkm84w1VQbZDAtse5coMu62jg3gbZk`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, relaxed and cheerful male voice with an American accent, suitable for selling leisure and entertainment content.
- **Description (ZH)**:
  - 年轻松弛开朗的美式男声，适合休闲与娱乐向带货/内容。

### 65. 🇺🇸Kian

- **voiceoverId** / **Voice ID**:`pM1nkshNlKbjAmaA56kKvADnC8MZCHRE`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, enthusiastic, and friendly standard American male voice, similar to the style of a short video introducing a product. There is an empty indoor echo.
- **Description (ZH)**:
  - 年轻热情友好的标准美式男声，风格接近短视频带货讲解；带空旷室内混响感。

### 66. 🇺🇸Kiara

- **voiceoverId** / **Voice ID**:`XQlMoBzYt0XUS1wYF2PfNGXldYlMZ6ef`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - Young, passionate and energetic American female voice, suitable for daily video sharing content.
- **Description (ZH)**:
  - 年轻热情有活力的美式女声，适合日常短视频分享。

### 67. 🇺🇸Lila

- **voiceoverId** / **Voice ID**:`gWaWEitU81Wmq9xWXjiCUaj6jgkQRBaX`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, energetic and cheerful female voice. American accent, upbeat tone, slightly happy, suitable for short video product introductions.
- **Description (ZH)**:
  - 年轻有活力、开朗的美式女声，语调上扬略欢快，适合短视频产品介绍。

### 68. 🇺🇸Logan

- **voiceoverId** / **Voice ID**:`biYUiHb9HqzXFgLNsVFnrBzSelnBcji7`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, cheerful male voice with an American accent and a natural tone, suitable for sharing real, everyday good things,
- **Description (ZH)**:
  - 年轻开朗的美式男声，音色自然，适合分享真实日常好物。（接口文案末尾逗号保留）

### 69. 🇺🇸Madison

- **voiceoverId** / **Voice ID**:`LA8DztCo3qNml4gFHuGBstcJ0gvubWiO`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, energetic and cheerful female voice. Confident, perfect for storytelling and narration
- **Description (ZH)**:
  - 年轻有活力、开朗的女声，自信，适合讲故事与旁白叙事。

### 70. 🇺🇸Malik

- **voiceoverId** / **Voice ID**:`N9YwabFpX0nHEBG19UMbpLBUEjeBfLgA`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A relaxed and pleasant American male accent, suitable for daily video sharing content.
- **Description (ZH)**:
  - 放松悦耳的美式男声，适合日常短视频分享。

### 71. 🇺🇸Natalie

- **voiceoverId** / **Voice ID**:`b8tXrVy7RjiuEuQYkepLg3Q0Ygo4GKgA`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A passionate and vibrant American accent, suitable for regular video sharing content
- **Description (ZH)**:
  - 热情饱满的美式口音，适合常规短视频分享。

### 72. 🇺🇸Nerys

- **voiceoverId** / **Voice ID**:`r17sGQcUxUpJk1A1VCFrngCIcW5tggzt`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, energetic, standard American female voice, suitable for product sharing content, with an empty outdoor echo.
- **Description (ZH)**:
  - 年轻有活力的标准美式女声，适合好物分享；带空旷室外混响感。

### 73. 🇺🇸Nolan

- **voiceoverId** / **Voice ID**:`RxfBoU8b9MwEmhVX2pzvZrOtypxjbqEj`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - An American emotional middle-aged male voice with an American accent, very powerful, confident, natural timbre, perfect for sharing real everyday good things
- **Description (ZH)**:
  - 富有戏剧张力的美式中年男声，浑厚有力、自信、音色自然，适合分享真实日常好物。

### 74. 🇺🇸Nora

- **voiceoverId** / **Voice ID**:`AOgdCkt5Cofb6y8nmgGhGW5peAKPU4d0`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A youthful, passionate, and energetic female American accent, suitable for product sharing content.
- **Description (ZH)**:
  - 年轻热情有活力的美式女声，适合好物分享。

### 75. 🇺🇸Paul

- **voiceoverId** / **Voice ID**:`fufMzXAuSuQz6Tv9XgfSPZj9tSYcRDyl`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, deep, and powerful male voice with an American accent, conveying a sense of stability and trustworthiness, suitable for product sharing content.
- **Description (ZH)**:
  - 年轻偏低沉、有力的美式男声，稳重可信，适合好物分享类内容。

### 76. 🇺🇸Percival

- **voiceoverId** / **Voice ID**:`qYGtNjPssAzPPwQYhzcBj2htLCXJ9Okq`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - The voice of an older, confident American male. American accent, natural voice, suitable for short video product introductions and daily short video sharing.
- **Description (ZH)**:
  - 自信稳重的美式年长男声，音色自然，适合短视频产品介绍与日常分享。

### 77. 🇺🇸Poppy

- **voiceoverId** / **Voice ID**:`RUveaY2EgpkFrilk3YbL0rznFNAkKw4k`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young female voice with a American accent, natural timbre and a hint of joy, suitable for sharing the real beauty of everyday life, can be used for narration
- **Description (ZH)**:
  - 年轻美式女声，音色自然带愉悦感，适合分享日常生活之美，也可用于旁白。

### 78. 🇺🇸Riley

- **voiceoverId** / **Voice ID**:`at7bM2qL7U2qZuiCFs2QTAjSEAZBECKs`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - A young male voice with a standard American accent and a vibrant sound. Great for voice-overs, social media content.
- **Description (ZH)**:
  - 标准美式年轻男声，音色有活力，适合画外音与社交媒体内容。

### 79. 🇺🇸Sam

- **voiceoverId** / **Voice ID**:`4V2v0y8O3WI5WF4r3EXZJVL1p1UXMZjJ`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young American male with a positive voice. Professional, relaxed, confident
- **Description (ZH)**:
  - 积极向上的年轻美式男声：专业、松弛、自信。

### 80. 🇺🇸Saniya

- **voiceoverId** / **Voice ID**:`oj1dLrhp897XlhVnv4vCZzFoJTa4oDE5`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, passionate, and energetic standard American black female voice with a positive tone, suitable for regular video sharing and product video introductions. There is an empty outdoor echo.
- **Description (ZH)**:
  - 年轻热情有活力的标准美式黑人女声，语气积极；适合常规分享与产品介绍；带空旷室外混响感。

### 81. 🇺🇸Scarlett

- **voiceoverId** / **Voice ID**:`c3MbOazKNxKKD865CUj4hutwsU3yQUpU`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, cheerful American woman with an American accent. Her voice is professional, confident and natural, suitable for daily video sharing.
- **Description (ZH)**:
  - 年轻开朗的美式女声，专业、自信、自然，适合日常短视频分享。

### 82. 🇺🇸Scott

- **voiceoverId** / **Voice ID**:`QPx43v6oAg3HOTDEegoBriykdwQjumN1`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A young, vibrant, and passionate voice with an American accent, suitable for product sharing and social media video creation content.
- **Description (ZH)**:
  - 年轻明亮、富有激情的美式声音，适合好物分享与社交媒体视频创作。

### 83. 🇺🇸Shaniqua

- **voiceoverId** / **Voice ID**:`iT55BMKlWaVm8cZvADMJFdhZcaQeMpvR`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A relaxed and cheerful American female voice, suitable for daily video sharing content.
- **Description (ZH)**:
  - 轻松愉快的美式女声，适合日常短视频分享。

### 84. 🇺🇸Sloane

- **voiceoverId** / **Voice ID**:`Psl17vOzyQFtYFP0tJu7FIwSgLyjVquH`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A relaxed and cheerful American female voice, suitable for social media video creation content.
- **Description (ZH)**:
  - 轻松愉快的美式女声，适合社交媒体视频创作。

### 85. 🇺🇸Stella

- **voiceoverId** / **Voice ID**:`GIwQzNuCBl4wvGeKbUwWQkE2yDYEivb4`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - The voice of a young American woman, with an American accent, full of energy, a slightly faster tone, and a natural timbre, suitable for sharing the real beauty of everyday life
- **Description (ZH)**:
  - 年轻美式女声，充满活力，语速略快，音色自然，适合分享日常生活的真实美好。

### 86. 🇺🇸Valley

- **voiceoverId** / **Voice ID**:`ef416a782ac74be1b682f99e5b9f4a6d`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - A valley girl female voice. Great for shorts.
- **Description (ZH)**:
  - 美式「山谷女孩」风格女声，很适合短视频。

### 87. 🇺🇸William

- **voiceoverId** / **Voice ID**:`jdyPMRaNJaLmvXF6iIU1t1hUHMLBOxuI`
- **Tags**:`2` — Advertisement
- **Description (EN)**:
  - A young male voice with a standard American accent and a slightly magnetic voice. Very suitable for storytelling narration and commercial dubbing.
- **Description (ZH)**:
  - 标准美式年轻男声，略带磁性，很适合叙事旁白与商业配音。

### 88. 🇺🇸Zuri

- **voiceoverId** / **Voice ID**:`3mTAYb1gDp85Sni0yTIsdjRIejWPFLTy`
- **Tags**:`1` — UGC (user-generated content)
- **Description (EN)**:
  - Young, enthusiastic, relaxed and cheerful American female voice, suitable for daily video sharing content.
- **Description (ZH)**:
  - 年轻热情、松弛开朗的美式女声，适合日常短视频分享。

