import os
import random


def _collect_text_paths(folder: str, include_subfolders: bool, extensions: str):
    if not os.path.isdir(folder):
        raise FileNotFoundError(f"Folder '{folder}' cannot be found.")

    exts = [e.strip().lower() for e in extensions.split(",") if e.strip()]
    if not exts:
        raise ValueError("No extensions specified. Example: .txt,.md")

    def is_valid(name: str) -> bool:
        n = name.lower()
        return any(n.endswith(ext) for ext in exts)

    text_paths = []
    if include_subfolders:
        for root, _, files in os.walk(folder):
            for file in files:
                if is_valid(file):
                    text_paths.append(os.path.join(root, file))
    else:
        for file in os.listdir(folder):
            p = os.path.join(folder, file)
            if os.path.isfile(p) and is_valid(file):
                text_paths.append(p)

    if not text_paths:
        raise FileNotFoundError(
            f"No valid text files found in '{folder}' for extensions: {exts}"
        )

    return text_paths, exts


# 1) Classic: простой random.choice
class LoadRandomTextClassic:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"folder": ("STRING", {"default": ""})},
            "optional": {
                "include_subfolders": ("BOOLEAN", {"default": False}),
                "extensions": ("STRING", {"default": ".txt,.prompt,.md"}),
                "encoding": ("STRING", {"default": "utf-8"}),
                "errors": ("STRING", {"default": "replace"}),
                "debug_info": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("text", "text_path", "debug")
    FUNCTION = "load_random_text"
    CATEGORY = "zveroboy/random"

    @classmethod
    def IS_CHANGED(s, folder, include_subfolders=False, extensions=".txt,.prompt,.md", encoding="utf-8", errors="replace", debug_info=False, **kwargs):
        # Каждый прогон считаем "изменением"
        return random.random()

    def load_random_text(self, folder, include_subfolders=False, extensions=".txt,.prompt,.md",
                         encoding="utf-8", errors="replace", debug_info=False, **kwargs):

        text_paths, exts = _collect_text_paths(folder, include_subfolders, extensions)

        random_text_path = random.choice(text_paths)
        with open(random_text_path, "r", encoding=encoding, errors=errors) as f:
            text = f.read()

        debug = ""
        if debug_info:
            debug = f"Mode: classic | Files: {len(text_paths)} | Selected: {os.path.basename(random_text_path)} | Exts: {exts}"

        return (text, random_text_path, debug)


# 2) Seed: детерминированный выбор от seed
class LoadRandomTextSeed:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder": ("STRING", {"default": ""}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "include_subfolders": ("BOOLEAN", {"default": False}),
                "extensions": ("STRING", {"default": ".txt,.prompt,.md"}),
                "encoding": ("STRING", {"default": "utf-8"}),
                "errors": ("STRING", {"default": "replace"}),
                "debug_info": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("text", "text_path", "debug")
    FUNCTION = "load_random_text_seed"
    CATEGORY = "zveroboy/random"

    @classmethod
    def IS_CHANGED(s, folder, seed, include_subfolders=False, extensions=".txt,.prompt,.md", encoding="utf-8", errors="replace", debug_info=False, **kwargs):
        # Пересчитывать при смене seed/параметров
        return float(hash((folder, int(seed), bool(include_subfolders), str(extensions))))

    def load_random_text_seed(self, folder, seed, include_subfolders=False, extensions=".txt,.prompt,.md",
                              encoding="utf-8", errors="replace", debug_info=False, **kwargs):

        text_paths, exts = _collect_text_paths(folder, include_subfolders, extensions)

        # Не трогаем глобальный random, чтобы не влиять на другие ноды
        rng = random.Random(int(seed))
        random_text_path = rng.choice(text_paths)

        with open(random_text_path, "r", encoding=encoding, errors=errors) as f:
            text = f.read()

        debug = ""
        if debug_info:
            debug = f"Mode: seed | Seed: {int(seed)} | Files: {len(text_paths)} | Selected: {os.path.basename(random_text_path)} | Exts: {exts}"

        return (text, random_text_path, debug)


# 3) Shuffle-bag: без повторов до исчерпания, кэш списка
class LoadRandomTextShuffle:
    def __init__(self):
        self.text_paths_cache = None
        self.cache_key = None
        self.index = 0

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {"folder": ("STRING", {"default": ""})},
            "optional": {
                "include_subfolders": ("BOOLEAN", {"default": False}),
                "extensions": ("STRING", {"default": ".txt,.prompt,.md"}),
                "encoding": ("STRING", {"default": "utf-8"}),
                "errors": ("STRING", {"default": "replace"}),
                "reset_cache": ("BOOLEAN", {"default": False}),
                "reshuffle_on_wrap": ("BOOLEAN", {"default": True}),
                "debug_info": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("text", "text_path", "debug")
    FUNCTION = "load_random_text_shuffle"
    CATEGORY = "zveroboy/random"

    @classmethod
    def IS_CHANGED(s, folder, include_subfolders=False, extensions=".txt,.prompt,.md",
                   encoding="utf-8", errors="replace", reset_cache=False, reshuffle_on_wrap=True, debug_info=False, **kwargs):
        # Тут важно, чтобы reset_cache действительно триггерил пересчёт
        return float(hash((folder, bool(include_subfolders), str(extensions), bool(reset_cache))))

    def load_random_text_shuffle(self, folder, include_subfolders=False, extensions=".txt,.prompt,.md",
                                 encoding="utf-8", errors="replace",
                                 reset_cache=False, reshuffle_on_wrap=True, debug_info=False, **kwargs):

        cache_key = (folder, bool(include_subfolders), str(extensions))

        if reset_cache or self.text_paths_cache is None or cache_key != self.cache_key:
            text_paths, exts = _collect_text_paths(folder, include_subfolders, extensions)
            self.text_paths_cache = text_paths[:]
            random.shuffle(self.text_paths_cache)
            self.index = 0
            self.cache_key = cache_key
        else:
            exts = [e.strip().lower() for e in extensions.split(",") if e.strip()]

        if not self.text_paths_cache:
            raise RuntimeError("Shuffle cache is empty (unexpected).")

        random_text_path = self.text_paths_cache[self.index]
        self.index += 1

        wrapped = False
        if self.index >= len(self.text_paths_cache):
            self.index = 0
            wrapped = True
            if reshuffle_on_wrap:
                random.shuffle(self.text_paths_cache)

        with open(random_text_path, "r", encoding=encoding, errors=errors) as f:
            text = f.read()

        debug = ""
        if debug_info:
            debug = (
                f"Mode: shuffle-bag | Files: {len(self.text_paths_cache)} | "
                f"Index: {self.index}/{len(self.text_paths_cache)} | Wrapped: {wrapped} | "
                f"Selected: {os.path.basename(random_text_path)} | Exts: {exts}"
            )

        return (text, random_text_path, debug)


NODE_CLASS_MAPPINGS = {
    "LoadRandomTextClassic": LoadRandomTextClassic,
    "LoadRandomTextSeed": LoadRandomTextSeed,
    "LoadRandomTextShuffle": LoadRandomTextShuffle,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadRandomTextClassic": "Random Text (Classic)",
    "LoadRandomTextSeed": "Random Text (Seed)",
    "LoadRandomTextShuffle": "Random Text (Shuffle-Bag)",
}
