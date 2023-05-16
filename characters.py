from domain import CharacterCount, TokenCount
from tokens import TOKENS_PER_CHARACTER


def to_character_count(token_count: TokenCount) -> CharacterCount:
    """Converts a token count to a character count."""
    return CharacterCount(token_count / TOKENS_PER_CHARACTER)
