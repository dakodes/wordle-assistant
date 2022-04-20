import ast
from typing import List
import re

import requests


def download_answers() -> List[str]:
    wordle_js_url = "https://www.nytimes.com/games/wordle/main.4d41d2be.js"
    wordle_js_download_response = requests.get(wordle_js_url)
    if wordle_js_download_response.status_code != requests.codes["ok"]:
        raise RuntimeError("Failed to download list of answers")
    re_result = re.search(r'Ma\s*=\s*(\[\s*(\"[a-z]{5}\"\s*,\s*)*\"[a-z]{5}\"\s*])', wordle_js_download_response.text)
    if re_result is None:
        raise RuntimeError("Failed to parse downloaded list of answers")
    vocabulary_list_str = re_result.group(1)
    return ast.literal_eval(vocabulary_list_str)
