"""Utility functions for the Better Thermostat."""

def mode_remap(hvac_mode, modes):
	"""Remap HVAC mode to better mode."""
	if modes is None:
		return hvac_mode
	if modes.get(hvac_mode) is not None:
		return modes.get(hvac_mode)
	else:
		return hvac_mode

def reverse_modes(modes):
	"""Reverse HVAC modes."""
	changed_dict = {}
	for key, value in modes.items():
		changed_dict[value] = key
	return changed_dict

def calibration(self, calibration_type):
	"""Select calibration function based on calibration type."""
	if calibration_type == 1:
		return temperature_calibration(self)
	if calibration_type == 0:
		return default_calibration(self)

def default_calibration(self):
	# FIXME: Write docstring
	
	state = self.hass.states.get(self.heater_entity_id).attributes
	new_calibration = float((float(self._cur_temp) - float(state.get('local_temperature'))) + float(state.get('local_temperature_calibration')))
	return convert_decimal(new_calibration)

def temperature_calibration(self):
	# FIXME: Write docstring
	
	state = self.hass.states.get(self.heater_entity_id).attributes
	new_calibration = abs(float(round((float(self._target_temp) - float(self._cur_temp)) + float(state.get('local_temperature')), 2)))
	if new_calibration < float(self._TRV_min_temp):
		new_calibration = float(self._TRV_min_temp)
	if new_calibration > float(self._TRV_max_temp):
		new_calibration = float(self._TRV_max_temp)
	
	return new_calibration


def convert_decimal(decimal_string):
	"""Convert a decimal string to a float."""
	try:
		return float(format(float(decimal_string), '.1f'))
	except ValueError:
		return None
