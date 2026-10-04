package insurance;

public class Main {
	public static void main () {
		InsuranceCalculator insurance = new InsuranceCalculator();
		Client client = new Client();
		
		client.numberAccidents = 2;
		
		try {
			insurance.getClientDeductible(client);
		} catch (InvalidClientData e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
}
