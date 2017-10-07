package cooling;

public class LogarithmicalCooling implements CoolingFunction {
	@Override
	public double coolingRate(double deltaTemperature, int counter) {
		return (1 + deltaTemperature * Math.log(counter)) / (1 + deltaTemperature * Math.log(counter + 1));
	}
}
