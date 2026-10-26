import sys

class Thermostat:
	current_temp = 0.0
	target_temp = 0.0
	heating_threshold = 0.5
	cooling_threshold = 0.5
	heating = False
	cooling = False
	starting_up = False

	def __init__(self, _target_temp: float, _heating_threshold: float, 
	             _cooling_threshold: float):
		self.target_temp = _target_temp
		self.heating_threshold = _heating_threshold
		self.cooling_threshold = _cooling_threshold


	def __str__(self) -> str:
		if self.heating == True:
			return f" - heating - {self.current_temp}"
		elif self.cooling == True:
			return f" - cooling - {self.current_temp}"
		else:
			return f" - nothing - {self.current_temp}"


	def open_ac(self) -> None:
		if self.heating == True or self.cooling == True:
			return
		if  self.current_temp < self.target_temp - self.heating_threshold:
			self.heating = True
		elif self.current_temp > self.target_temp + self.cooling_threshold:
			self.cooling = True


	def close_ac(self) -> None:
		if self.heating == False and self.cooling == False:
			return
		if self.current_temp >= self.target_temp:
			self.heating = False
		elif self.current_temp <= self.target_temp:
			self.cooling = False


	def ambient_loss(self, outside_temp: float) -> None:
		if self.current_temp > outside_temp:
			self.current_temp -= 0.25
		elif self.current_temp < outside_temp:
			self.current_temp += 0.25


	def temp_regulator(self, outside_temp: float) -> None:
		if self.starting_up == False:
			self.current_temp = outside_temp
			self.starting_up = True
		
		if self.heating == False and self.cooling == False:
			self.ambient_loss(outside_temp)
			self.open_ac()
		else:
			self.close_ac()

		if self.heating == True:
			self.current_temp += 0.5
		elif self.cooling == True:
			self.current_temp -= 0.5
		
def main() -> int:
	try:
		if len(sys.argv) != 4:
			raise Exception("Invalid amount of argumets! Try the format: "
			                "python3 expert_system.py target_temperature "
							"heating_threshold cooling_threshold")
		ac = Thermostat(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))

		for line in sys.stdin:
			ac.temp_regulator(float(line.strip()))
			print(float(line.strip()), ac)
	except Exception as err:
		print(err.args[0])
		return 1
	return 0

if __name__ == "__main__":
	sys.exit(main())

		
