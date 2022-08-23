"""This module has all of the helper functions needed to merge shards."""
from typing import List

from google.cloud import documentai


def _get_paragraphs(shards: List[documentai.Document]) -> List[str]:
  """Returns a list of text from Document.page.paragraphs ."""
  result = []
  for shard in shards:
    text = shard.text
    for page in shard.pages:
      result.append(_text_from_layout(page.paragraphs, text))

  return result


def _get_lines(shards: List[documentai.Document]) -> List[str]:
  """Returns a list of text from Document.page.lines ."""
  result = []
  for shard in shards:
    text = shard.text
    for page in shard.pages:
      result.append(_text_from_layout(page.lines, text))

  return result


def _get_tokens(shards: List[documentai.Document]) -> List[str]:
  """Returns a list of text from Document.page.tokens ."""
  result = []
  for shard in shards:
    text = shard.text
    for page in shard.pages:
      result.append(_text_from_layout(page.tokens, text))

  return result


def _text_from_layout(page_entities, text: str) -> List[str]:
  """Returns a list of texts from Document.page ."""
  result = []
  # If a text segment spans several lines, it will
  # be stored in different text segments.
  for entity in page_entities:
    result_text = ""
    for text_segment in entity.layout.text_anchor.text_segments:
      start_index = int(text_segment.start_index)
      end_index = int(text_segment.end_index)
      result_text += text[start_index:end_index]
    result.append(text[start_index:end_index])
  return result
