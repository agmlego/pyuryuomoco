# pylint: disable=logging-fstring-interpolation
import logging
import re
import string

log = logging.getLogger(__name__)

sub_eng_to_ury = {
    "a": "u",
    "b": "v",
    "c": "s",
    "d": "j",
    "e": "o",
    "f": "h",
    "g": "t",
    "h": "f",
    "i": "y",
    "j": "d",
    "k": "p",
    "l": "r",
    "m": "n",
    "n": "m",
    "o": "e",
    "p": "k",
    "qu": "w",
    "r": "l",
    "s": "c",
    "t": "g",
    "u": "a",
    "v": "b",
    "w": "qu",
    "x": "z",
    "y": "i",
    "z": "x",
}
sub_ury_to_eng = {
    "a": "u",
    "b": "v",
    "c": "s",
    "d": "j",
    "e": "o",
    "f": "h",
    "g": "t",
    "h": "f",
    "i": "yu",
    "j": "d",
    "k": "p",
    "l": "r",
    "m": "n",
    "n": "m",
    "o": "e",
    "p": "k",
    "qu": "w",
    "r": "l",
    "s": "c",
    "t": "g",
    "u": "a",
    "v": "b",
    "w": "qu",
    "x": "z",
    "yu": "i",
    "y": "i",
    "z": "x",
}

e2u_end_ui_rule = re.compile(r"(?:ui\b)")
e2u_yu_rule = re.compile(r"y([cglmnr]{1})")
u2e_end_ui_rule = re.compile(r"(?:uyu\b)")
u2e_yu_rule = re.compile(r"yu([cglmnr]{1})")


def substitute_english(phrase: str) -> str:
    """
    Perform only substitutions to make an input English phrase into Uryuomoco

    Args:
        phrase (str): English phrase

    Returns:
        str: Uryuomoco translation
    """
    skip_trans = False
    check_q = False
    output = []
    for c in phrase:
        if c == "[":
            log.debug(f"[cyan bold]{c}[/]: Starting a skip block")
            skip_trans = True
            continue
        if c == "]":
            log.debug(f"[cyan bold]{c}[/]: Ending a skip block")
            skip_trans = False
            continue
        if skip_trans:
            output.append(c)
            log.debug(f"[magenta bold]{c}[/] output because skipping translation")
            continue
        if c == "q":
            log.debug(f"[cyan bold]{c}[/]: Is a q")
            check_q = True
            continue
        if check_q:
            if c == "u":
                out = sub_eng_to_ury["qu"]
                output.append(out)
                log.debug(f"[yellow bold]{out}[/] output because qu")
            else:
                out = "q"
                out += sub_eng_to_ury[c]
                output.append(out)
                log.debug(f"[red bold]{out}[/] output because qu")
            check_q = False
        elif c not in sub_eng_to_ury:
            out = c
            output.append(out)
            log.debug(f"[green bold]{out}[/] output because not in mapping")
        else:
            out = sub_eng_to_ury[c]
            output.append(out)
            log.debug(f"[blue bold]{out}[/] output because in mapping")
    output = "".join(output)
    output = e2u_yu_rule.sub(r"yu\1", output)
    output = e2u_end_ui_rule.sub("uyu", output)
    return output


def substitute_uryuomoco(phrase: str) -> str:
    """
    Perform only substitutions to make an input Uryuomoco phrase into English

    Args:
        phrase (str): Uryuomoco phrase

    Returns:
        str: English translation
    """
    phrase = u2e_yu_rule.sub(r"y\1", phrase)
    phrase = u2e_end_ui_rule.sub("ui", phrase)
    skip_trans = False
    check_q = False
    check_y = False
    output = []
    for c in phrase:
        if c == "[":
            log.debug(f"[cyan bold]{c}[/]: Starting a skip block")
            skip_trans = True
            continue
        if c == "]":
            log.debug(f"[cyan bold]{c}[/]: Ending a skip block")
            skip_trans = False
            continue
        if skip_trans:
            output.append(c)
            log.debug(f"[magenta bold]{c}[/] output because skipping translation")
            continue
        if c == "q":
            log.debug(f"[cyan bold]{c}[/]: Is a q")
            check_q = True
            continue
        if c == "y":
            log.debug(f"[cyan bold]{c}[/]: Is a y")
            check_y = True
            continue
        if check_q:
            if c == "u":
                out = sub_ury_to_eng["qu"]
                output.append(out)
                log.debug(f"[yellow bold]{out}[/] output because qu")
            else:
                out = "q" + sub_ury_to_eng[c]
                output.append(out)
                log.debug(f"[red bold]{out}[/] output because qu")
            check_q = False
        elif check_y:
            if c == "u":
                out = sub_ury_to_eng["yu"]
                output.append(out)
                log.debug(f"[yellow bold]{out}[/] output because yu")
            elif c in sub_ury_to_eng:
                out = sub_ury_to_eng["y"] + sub_ury_to_eng[c]
                output.append(out)
                log.debug(f"[red bold]{out}[/] output because y")
            else:
                out = sub_ury_to_eng["y"] + c
                output.append(out)
                log.debug(f"[green bold]{out}[/] output because y but not in mapping")
            check_y = False
        elif c not in sub_ury_to_eng:
            out = c
            output.append(out)
            log.debug(f"[green bold]{out}[/] output because not in mapping")
        else:
            out = sub_ury_to_eng[c]
            output.append(out)
            log.debug(f"[blue bold]{out}[/] output because in mapping")
    output = "".join(output)
    return output
