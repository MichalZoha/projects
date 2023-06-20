#!/usr/bin/env python3

"""
Skript vytvoří testovací data pro zadanou úlohu.
"""

import datetime
import json
import logging
import pathlib
import random
import sys
from typing import Generator, Iterable, Tuple
from dataclasses import dataclass, asdict

from tqdm import tqdm


logging.basicConfig(level=logging.INFO, format="%(message)s")


@dataclass
class Output:
    """
    The output exported as JSON.
    """
    date: datetime.date
    text: str
    count: int
    status: bool


def make_random_sentence() -> str:
    nouns = ["puppy", "rabbit", "cat", "monkey", "dog"]
    verbs = ["runs", "hits", "jumps"]
    adv = ["crazily", "dutifully", "foolishly", "merrily", "occasionally"]
    adj = ["adorable", "clueless", "odd"]

    random_entry = lambda x: x[random.randrange(len(x))]

    return " ".join(
        [random_entry(nouns), random_entry(verbs), random_entry(adv), random_entry(adj)]
    )


def make_test_data(dates: Iterable[datetime.date]) -> Generator[Tuple[datetime.date, Output], None, None]:
    """
    Make a randomised test data from the given dates.
    """
    for date in dates:
        for i in range(1, random.choice([1, 2, 3, 4, 5, 6])):
            text = make_random_sentence()
            result = Output(date=date, text=text, count=i, status=True)
            # Randomly change date.
            if date.month % 2 == random.choice(
                [1, 0]
            ) and date.day % 2 != random.choice([1, 0]):
                delta = random.choice([-1, 0, 1])
                if delta != 0 and bool(random.choice([0, 1])):
                    date_orig = result.date
                    result.date += datetime.timedelta(days=delta)
                    result.status = False
                    logging.debug(f"\t{result}")
            yield date, result


def save_test_data(date, data: Output, root: pathlib.Path) -> None:
    """Save randomised test data to the file."""
    output_path = root / f"{date}_{data.count}.json"
    output_path.parent.mkdir(exist_ok=True, parents=True)

    with open(output_path, mode="w") as file:
        file.write(json.dumps(asdict(data), indent=4, sort_keys=True, default=str))


def delete_folder(path) -> None:
    for sub in path.iterdir():
        if sub.is_dir():
            delete_folder(sub)
        else:
            sub.unlink()
    path.rmdir()


def main() -> None:
    ROOT = pathlib.Path("./source")

    if ROOT.exists():
        delete_folder(ROOT)

    date_i = datetime.date(year=2021, month=1, day=1)
    date_f = datetime.datetime.now().date()

    dates = [date_i + datetime.timedelta(days=i) for i in range((date_f - date_i).days)]

    infos = []  # Some information for a log file: date, index, status

    # Make test data files.
    logging.info("Saving files...")

    for date, data in (bar := tqdm(make_test_data(dates))):
        try:
            bar.set_description_str(f"{data.date}_{data.count}.json saved", refresh=True) # type: ignore
            save_test_data(date, data, ROOT)
            infos.append([data.date, data.count, data.status])
        except IOError as ex:
            logging.error(f"Could not save file {data.date}_{data.count}.json!")
            sys.exit(1)
        else:
            pass

    logging.info(f"Saved {len(infos)} files.")

    # Make a log file with dates.
    with open(ROOT / "data.log", "w") as file:
        file.write(
            "\n".join(
                [f"{info[0]},{info[1]},{info[2]}" for date, info in zip(dates, infos)]
            )
        )


if __name__ == "__main__":
    main()
