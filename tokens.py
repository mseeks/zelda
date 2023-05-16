from threading import Lock
import threading
from domain import CharacterCount, TokenCount
import time

# Constants
GPT_4_TOKEN_RATE_LIMIT = 40000  # 40k Tokens Per Minute (TPM)
SECONDS_IN_MINUTE = 60
GPT_4_TOKEN_REFRESH_RATE = GPT_4_TOKEN_RATE_LIMIT / SECONDS_IN_MINUTE


TOKENS_PER_CHARACTER = 0.25  # 1 token is approximately 4 characters


def manage_gpt_4_token_balance():
    global gpt_4_token_balance_lock
    global gpt_4_token_balance

    gpt_4_token_balance_lock = Lock()
    gpt_4_token_balance = 0

    while True:
        time.sleep(1)  # Sleep for 1 second

        with gpt_4_token_balance_lock:
            if (
                gpt_4_token_balance + GPT_4_TOKEN_REFRESH_RATE > GPT_4_TOKEN_RATE_LIMIT
            ):  # Don't exceed the limit
                gpt_4_token_balance = GPT_4_TOKEN_RATE_LIMIT
            else:
                gpt_4_token_balance = gpt_4_token_balance + GPT_4_TOKEN_REFRESH_RATE


def to_token_count(character_count: CharacterCount) -> TokenCount:
    """Converts a character count to a token count."""
    return TokenCount(character_count * TOKENS_PER_CHARACTER)
