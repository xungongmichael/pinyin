# %%
import os
import json
import numpy as np
from typing import Dict, List, Union, Iterable

CHAR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "char.json")
CHAR = json.load(open(CHAR_PATH, "r", encoding="utf8"))


class PinYin(object):
    def __init__(self, user_dictionary: Dict = None) -> None:
        self.chars = None

        if user_dictionary is not None:
            self.check_user_dictionary(user_dictionary)
            self.chars.update(user_dictionary)

    def convert(self,
                strings: Union[str, Iterable[str]],
                join: bool = True,
                nosplit: bool = False) -> Union[str, List[str]]:
        if isinstance(strings, str):
            if nosplit:
                convert = [self.chars.get(strings, self._unknown)]
            else:
                convert = [self.chars.get(k, self._unknown) for k in strings]
            convert = [
                f"{p['consonant']}{p['vowel']}{p['tone']}" for p in convert
            ]
            if join:
                return " ".join(convert)
            return convert

        return [self.convert(string, join=join) for string in strings]

    def _encode(
        self, codecs: Dict[str, int],
        strings: Union[str,
                       Iterable[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        if isinstance(strings, str):
            return np.array([codecs.get(s, -1) for s in strings])
        return [self._encode(codecs, string) for string in strings]

    def encode_pinyin(
        self, strings: Union[str, List[str], Iterable[List[str]]]
    ) -> Union[np.ndarray, List[np.ndarray]]:
        if isinstance(strings, str):
            return self.pinyin_codes.get(strings, -1)
        elif isinstance(strings, List) and isinstance(strings[0], List):
            return [self.encode_pinyin(string) for string in strings]
        else:
            return np.array(
                [self.pinyin_codes.get(string, -1) for string in strings])

    def encode_hanzi(
        self,
        strings: Union[str,
                       Iterable[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        if isinstance(strings, str):
            print(strings)
            return np.array([self.hanzi_codes.get(s, -1) for s in strings])
        return [self.encode_hanzi(string) for string in strings]

    def encode_pronouce(
        self,
        strings: Union[str,
                       Iterable[str]]) -> Union[np.ndarray, List[np.ndarray]]:
        pinyins = self.convert(strings, join=False)
        return self.encode_pinyin(pinyins)

    @property
    def _unknown(self) -> Dict[str, str]:
        return {"consonant": "un", "vowel": "know", "tone": "n"}

    @property
    def pinyin_codes(self) -> Dict[str, int]:
        if hasattr(self, "_pinyin_codes"):
            return self._pinyin_codes

        pinyins = list(
            set([
                f"{p['consonant']}{p['vowel']}{p['tone']}"
                for p in self.chars.values()
            ]))
        return dict(zip(pinyins, range(len(pinyins))))

    @property
    def hanzi_codes(self) -> Dict[str, int]:
        if hasattr(self, "_hanzi_codes"):
            return self._hanzi_codes
        self._hazi_codes = dict(
            zip(self.chars.keys(), range(len(self.chars.keys()))))
        return self._hazi_codes

    def check_user_dictionary(self, user_dict: Dict):
        for item in user_dict.values():
            assert "consonant" in item.keys(
            ), "user dictionary doesn't have consonant"
            assert "vowel" in item.keys(), "user dictionary doesn't have vowel"
            assert "tone" in item.keys(), "user dictionary doesn't have tone"


if __name__ == "__main__":

    test1 = "你好啊"
    test2 = ["不好", "发到哪"]

    user_dict = {"book": {"consonant": "bu", "vowel": "ke", "tone": "4"}}
    pinyin = PinYin(user_dictionary=user_dict)

    py1 = pinyin.convert(test1)
    py2 = pinyin.convert(test2)

    hzc1 = pinyin.encode_hanzi(test1)
    hzc2 = pinyin.encode_hanzi(test2)

    py1 = pinyin.convert(test1, join=False)
    py2 = pinyin.convert(test2, join=False)
    pyc1 = pinyin.encode_pinyin(py1)
    pyc2 = pinyin.encode_pinyin(py2)
    print(pyc1)
    print(pyc2)

    pr1 = pinyin.encode_pronouce(test1)
    pr2 = pinyin.encode_pronouce(test2)
    print(pr1)
    print(pr2)