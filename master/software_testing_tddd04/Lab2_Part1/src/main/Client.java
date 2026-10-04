package insurance;

import java.util.Vector;

public class Client {

	int id;
	int age;
	int yearLicence;
	int yearInsurance;
	int yearLastAccident;

	boolean isGoldMember;
	
	int numberAccidents; // number of accidents for the calendar year
	
	
	Vector<Car> cars;
	
	public Client () {
		cars = new Vector<Car>();
	}
	
}
