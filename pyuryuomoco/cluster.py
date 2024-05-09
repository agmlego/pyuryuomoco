# pylint: disable=logging-fstring-interpolation
import logging
import re

from .substitution import *

log = logging.getLogger(__name__)
cluster_eng_to_ury = {
    "th": "ch",
    "ch": "se",
    "wh": "quo",
    "ing": "ot",
    "gr": "tul",
    "ss": "ais",
    "ll": "ra",
    "sh": "us",
}
cluster_ury_to_eng = {
    "ch": "th",
    "se": "ch",
    "quo": "wh",
    "ot": "ing",
    "tul": "gr",
    "ais": "ss",
    "ra": "ll",
    "us": "sh",
}
end_e_rule = re.compile(r"(?:[e]\b)")
end_j_rule = re.compile(r"(?:[j]\b)")


def cluster_english(phrase: str) -> str:
    """
    Perform all substitution and clustering rules to make the English phrase into Uryuomoco

    Args:
        phrase (str): English phrase

    Returns:
        str: Uryuomoco translation
    """
    mapping = list(zip(range(len(cluster_eng_to_ury)), cluster_eng_to_ury.items()))
    phrase = phrase.lower()
    for idx, (key, value) in mapping:
        cnt = phrase.count(key)
        if cnt:
            log.debug(
                f"Reserving {cnt}x of [cyan bold]{key}[/] to become [yellow bold]{value}[/]"
            )
            phrase = phrase.replace(key, f"<{idx}>")
    log.debug(f"Performing substitution on [magenta bold]{phrase}[/]")
    phrase = substitute_english(phrase)
    log.debug(f"Performing clustering on [green bold]{phrase}[/]")
    for idx, (key, value) in mapping:
        cnt = phrase.count(f"<{idx}>")
        if cnt:
            log.debug(
                f"Replacing {cnt}x of [green bold]<{idx}>[/] to become [yellow bold]{value}[/]"
            )
            phrase = phrase.replace(f"<{idx}>", value)
    phrase = end_e_rule.sub("eh", phrase)
    phrase = end_j_rule.sub("ja", phrase)
    return phrase


def cluster_uryuomoco(phrase: str) -> str:
    """
    Perform all substitution and clustering rules to make the Uryuomoco phrase into English

    Args:
        phrase (str): Uryuomoco phrase

    Returns:
        str: English translation
    """
    mapping = list(zip(range(len(cluster_ury_to_eng)), cluster_ury_to_eng.items()))
    phrase = phrase.lower()
    for idx, (key, value) in mapping:
        cnt = phrase.count(key)
        if cnt:
            log.debug(
                f"Reserving {cnt}x of [yellow bold]{key}[/] to become [cyan bold]{value}[/]"
            )
            phrase = phrase.replace(key, f"<{idx}>")
    log.debug(f"Performing substitution on [green bold]{phrase}[/]")
    phrase = substitute_uryuomoco(phrase)
    log.debug(f"Performing clustering on [magenta bold]{phrase}[/]")
    for idx, (key, value) in mapping:
        cnt = phrase.count(f"<{idx}>")
        if cnt:
            log.debug(
                f"Replacing {cnt}x of [yellow bold]<{idx}>[/] to become [green bold]{value}[/]"
            )
            phrase = phrase.replace(f"<{idx}>", value)
    return phrase
