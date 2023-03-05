import random
from dataclasses import dataclass
from typing import List


@dataclass
class GameWords:
    team_a: List[str]
    team_b: List[str]
    neutral: List[str]
    unrevealed: List[str]

    def __str__(self):
        ret = ""
        ret += "team_a: " + ", ".join(self.team_a) + "\n"
        ret += "team_b: " + ", ".join(self.team_b) + "\n"
        ret += "neutral: " + ", ".join(self.neutral) + "\n"
        ret += "unrevealed: " + ", ".join(self.unrevealed)

        return ret


class WordListSource:
    def get_word_list(self) -> List[str]:
        with open("list_a.txt", "r", encoding="utf8") as handle:
            return [line.lower().strip() for line in handle]


def _make_test_game_words() -> GameWords:

    team_a = [
        "post",
        "horn",
        "calf",
        "dress",
        "ball",
        "pistol",
        "aliea",
        "center",
        "pin",
    ]
    team_b = [
        "honey",
        "scorpion",
        "boot",
        "horseshoe",
        "fair",
        "cycle",
        "fighter",
        "litter",
    ]
    neutral = ["luck", "london", "life", "model", "buck", "saturn", "pan", "fence"]
    game_words = GameWords(
        team_a=team_a,
        team_b=team_b,
        neutral=neutral,
        unrevealed=[],
    )
    return game_words


def _make_game_words(word_list: List[str]) -> GameWords:

    local_list = list(word_list)
    random.shuffle(local_list)
    team_a = local_list[0:9]
    team_b = local_list[9:17]
    neutral = local_list[17:25]
    game_words = GameWords(
        team_a=team_a,
        team_b=team_b,
        neutral=neutral,
        unrevealed=[],
    )
    return game_words


def get_game_words() -> GameWords:
    # source = WordListSource()
    # return _make_game_words(word_list = source.get_word_list())
    return _make_test_game_words()


if __name__ == "__main__":
    print(get_game_words())

# end
