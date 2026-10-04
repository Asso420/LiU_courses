package se.liu.ida.InsuranceApp.data;

public class CarData {
	String 		carColor ;
	int			yearOfProduction;
	
	public CarData (String carColor, int yearOfProduction) {
		this.carColor = carColor;
		this.yearOfProduction = yearOfProduction;
	}

	public String getCarColor() {
		return carColor;
	}

	public void setCarColor(String carColor) {
		this.carColor = carColor;
	}

	public int getYearOfProduction() {
		return yearOfProduction;
	}

	public void setYearOfProduction(int yearOfProduction) {
		this.yearOfProduction = yearOfProduction;
	}
}
