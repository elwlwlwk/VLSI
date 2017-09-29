package cooling;

public class LinearCooling implements CoolingFunction {
	@Override
	public double coolingRate(double deltaTemperature, int counter) {
		return (1 + deltaTemperature * (counter - 1)) / (1 + deltaTemperature * counter);
	}
}
