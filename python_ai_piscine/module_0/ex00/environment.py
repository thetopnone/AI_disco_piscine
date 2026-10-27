import math
import sys
import time


def min_temp_monthly(month: int) -> float:
    k = month / 11
    temp_min = round(-5 + (19 / 2) * (1 + math.sin((k * 2 * math.pi)
                     - (math.pi / 2))), 2)
    return temp_min


def max_temp_monthly(month: int) -> float:
    k = month / 11
    temp_max = round(0 + (24 / 2) * (1 + math.sin((k * 2 * math.pi)
                     - (math.pi / 2))), 2)
    return temp_max


def season_temp(season: str) -> None:
    seasons = {
        "winter": (11, 0, 1),
        "spring": (2, 3, 4),
        "summer": (5, 6, 7),
        "autumn": (8, 9, 1)
    }

    season_months = seasons.get(season, None)
    if season_months is None:
        raise Exception("Invalid season input.The options are :"
                        " winter, spring, summer, autumn")

    min_season_temp = 0.0
    max_season_temp = 0.0

    for month in season_months:
        min_season_temp += min_temp_monthly(month)
        max_season_temp += max_temp_monthly(month)

    min_season_temp = round(min_season_temp / 3, 1)
    max_season_temp = round(max_season_temp / 3, 1)

    for day_slice in range(47):
        day_temp = round(min_season_temp + ((max_season_temp - min_season_temp)
                         / 2) * (1 + math.sin(((day_slice / 47) * 2 * math.pi)
                                              - (math.pi / 2))), 1)
        print(day_temp, flush=True)
        time.sleep(1)


def main() -> int:
    try:
        if len(sys.argv) != 2:
            raise Exception("Invalid argument amount. Try the format:"
                            "python3 environment.py season_name")
        season = sys.argv[1]
        season_temp(season)
    except Exception as err:
        print(err.args[0], file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
