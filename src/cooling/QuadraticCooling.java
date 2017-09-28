package cooling;

public class QuadraticCooling implements CoolingFunction {
	@Override
	public double coolingRate(double deltaTemperature, int counter) {
		return (1 + deltaTemperature * Math.pow(counter - 1, 2)) / (1 + deltaTemperature * Math.pow(counter, 2));
	}
}
