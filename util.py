import ast
from typing import List
import re

import requests


def download_answers() -> List[str]:
    wordle_base_url = "https://www.nytimes.com/games/wordle"

    # Download the index page and find the Javascript script name
    wordle_index_url = f"{wordle_base_url}/index.html"
    wordle_index_download_response = requests.get(wordle_index_url)
    if wordle_index_download_response.status_code != requests.codes["ok"]:
        raise RuntimeError("Failed to download the Wordle index page")
    javascript_script_name_re_results = re.findall(r'<script src="(main.[a-z\d]+.js)"></script>',
                                                   wordle_index_download_response.text)
    if not javascript_script_name_re_results:
        raise RuntimeError("Failed to parse the Javascript script name from the downloaded Wordle index page")
    if len(javascript_script_name_re_results) != 1:
        raise RuntimeError(f"Expected to find exactly 1 Javascript script name in the downloaded Wordle index page"
                           f"but found {len(javascript_script_name_re_results)}")
    wordle_javascript_url = f"{wordle_base_url}/{javascript_script_name_re_results[0]}"

    # Download the Javascript script and find the answers list
    wordle_javascript_download_response = requests.get(wordle_javascript_url)
    if wordle_javascript_download_response.status_code != requests.codes["ok"]:
        raise RuntimeError("Failed to download the Wordle Javascript script")
    word_lists_re_results = re.findall(r'[A-Za-z]+\s*=\s*(\[\s*(\"[a-z]{5}\"\s*,\s*)*\"[a-z]{5}\"\s*])',
                                       wordle_javascript_download_response.text)
    if not word_lists_re_results:
        raise RuntimeError("Failed to parse the word lists from the downloaded Wordle Javascript script")
    # We expect there to be 2 word lists found: (1) the answers (2) the valid guesses.
    # We are interested only in the answers list, but will still perform sanity checks for the valid guesses list,
    # which will be longer and in alphabetical order.
    word_lists = sorted([ast.literal_eval(re_result[0]) for re_result in word_lists_re_results],
                        key=lambda word_list: len(word_list))
    if len(word_lists) != 2:
        raise RuntimeError(f"Expected to find exactly 2 word lists in the downloaded Wordle Javascript script"
                           f"but found {len(word_lists)}")
    if sorted(word_lists[1]) != word_lists[1]:
        raise RuntimeError(f"Expected the valid guesses list from the downloaded Wordle Javascript script to be sorted")
    return word_lists[0]
