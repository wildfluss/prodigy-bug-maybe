# https://prodi.gy/docs/custom-recipes

# autopep8: off

import prodigy
from prodigy.components.preprocess import add_tokens
import pathlib
from typing import Generator, TypedDict
import hashlib
import srsly
import spacy
import benepar  # for add_pipe('benepar'
md_benepar = spacy.load('en_core_web_md')
md_benepar.add_pipe('benepar', config={'model': 'benepar_en3'})

# autopep8: on

# https://docs.python.org/3/library/typing.html#typing.TypedDict


class Example(TypedDict):
    html: str
    text: str


def load_my_custom_stream(source: str) -> Generator:
    stream = [{'text': ex['text'], "_input_hash": ex["_input_hash"],
               "_task_hash": ex["_task_hash"], 'content_a': ex['text']} for ex in srsly.read_jsonl(source)]
    stream = add_tokens(md_benepar, stream, skip=True)
    return stream


blocks = [
    {"view_id": "relations"},
    # https://prodi.gy/docs/custom-interfaces
    {"view_id": "html", "html_template": "<strong>{{content_a}}</strong>"},
]


@prodigy.recipe(
    "numbers-recipe",
    dataset=("Dataset to save answers to", "positional", None, str),
    source=("Source JSONL file", "option", "s", str),
    fix=("Review/fix?", "flag", "x", bool)
)
# TODO remove view_id
def my_custom_recipe(dataset, source, fix):  # ="./et/ABG/2021-12-31.txt"):
    if not fix:
        stream = load_my_custom_stream(source)
    else:
        stream = srsly.read_jsonl(source)

    # https://support.prodi.gy/t/enabling-both-assign-relations-and-select-spans-in-custom-relations-recipe/3647/5?u=ysz
    return {
        "view_id": "blocks",
        "dataset": dataset,  # Name of dataset to save annotations
        "stream": stream,  # Incoming stream of examples
        "config": {"blocks": blocks,
                   "labels": ['G', 'QW', 'QX', 'QN', 'XX', 'CC'],
                   "relations_span_labels": ["Q", "N", "W", "X", "C"],
                   "global_css": ".prodigy-container{max-width: unset;}"
                   },
    }
