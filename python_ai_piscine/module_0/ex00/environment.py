import math
import sys
import time

def min_temp_monthly(month: int)->float:
	k = month / 11
	temp_min = round(-5 + 19 * math.sin(k * math.pi), 2)
	print(f"temp_min: {temp_min}")
	return temp_min

def max_temp_monthly(month: int) -> float:
	k = month/ 11
	temp_max = round (0 + 20 * math.sin(k * math.pi), 2)
	print(f"temp_max: {temp_max}")
	return temp_max


def season_temp(season: str) -> int:
	seasons = {
		"winter": [11, 0, 1],
		"spring": [2, 3, 4],
		"summer": [5, 6, 7],
		"autumn": [8, 9 , 10]
	}

	season_months = seasons.get(season, None)
	if season_months is None:
		print("Invalid season input. The options are : winter, spring, summer, autumn")
		return -1

	min_season_temp = 0.0
	max_season_temp = 0.0
	
	for index, month in enumerate(season_months):
		min_season_temp += min_temp_monthly(month)
		max_season_temp += max_temp_monthly(month)
		print(f"Min_season_temp: {min_season_temp}")
		print(f"Max_season_temp: {max_season_temp}")
	min_season_temp = round (min_season_temp / 3, 2)
	max_season_temp = round (max_season_temp / 3, 2)
	print(f"Min_season_temp: {min_season_temp}")
	print(f"Max_season_temp: {max_season_temp}")
	

	for day_slice in range(47):
		day_temp = round(min_season_temp + (max_season_temp - min_season_temp) * math.sin ((day_slice / 47) * math.pi), 2)
		print(day_temp)
		time.sleep(1)
	return 0

def main() -> int:
	if len(sys.argv) != 2:
		print("Invalid argument amount. Try the format: python3 environment.py season_name")
		return 1

	season = sys.argv[1]
	if season_temp(season) == -1:
		return 1
	
	
if __name__  == "__main__":
	sys.exit(main())




	
