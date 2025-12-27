# ComfyUI-LoadRandomText

ComfyUI custom node that loads a random text file from a folder (optionally including subfolders) and outputs the text as STRING.

![comfy-csm](https://github.com/thezveroboy/ComfyUI-LoadRandomText/raw/main/picture.jpg)

## English
Load Random Text is a ComfyUI node pack that instantly picks a text file from a folder and outputs its contents straight into your workflow—perfect for prompts, negative prompts, styles, scene lists, or any text-driven automation. It turns large prompt libraries into a high-variation generation engine, so every run feels fresh without manual scrolling or copy-pasting.
​
It includes three modes for different production needs:
  - Classic: the simplest “pick a random file” behavior—fast and straightforward.​
  - Seed: deterministic selection driven by a seed—same seed, same file—great for reproducibility, batch runs, and debugging.​
  - Shuffle-Bag: maximum diversity—no repeats until the full list is exhausted, then reshuffles for the next cycle (ideal for huge collections).
​
## Русский
Load Random Text — набор нод для ComfyUI, которые мгновенно подхватывают случайный текстовый файл из выбранной папки и подставляют его в ваш workflow (например, как промпт, негатив, стиль, сцены, варианты описаний). Это идеальный способ превратить “тысячи файлов с идеями” в живую систему вариаций, где каждый прогон даёт новый результат без ручного перебора.
​
В составе три режима под разные задачи:
  - Classic: максимально простой “случайный файл” — быстро, удобно, без лишних настроек.​
  - Seed: выбор файла зависит от seed — получаете воспроизводимость (один и тот же seed → тот же файл), удобно для батчей, дебага и контроля вариативности.​
  - Shuffle-Bag: “честное разнообразие” — перебирает файлы без повторов, пока не пройдёт весь список, затем перемешивает заново (отлично для огромных библиотек).

## Install
1. Copy this repo into:
   `ComfyUI/custom_nodes/ComfyUI-LoadRandomText/`
2. Restart ComfyUI.

## Node
- **Load Random Text**
  - folder (STRING)
  - include_subfolders (BOOLEAN)
  - extensions (STRING), default: `.txt,.prompt,.md`
  - encoding (STRING), default: `utf-8`
  - errors (STRING), default: `replace`

### Outputs
- text (STRING)
- text_path (STRING)




