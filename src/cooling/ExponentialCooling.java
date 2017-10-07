package cooling;

public class ExponentialCooling implements CoolingFunction {
	@Override
	public double coolingRate(double deltaTemperature, int counter) {
		return deltaTemperature;
	}
}
