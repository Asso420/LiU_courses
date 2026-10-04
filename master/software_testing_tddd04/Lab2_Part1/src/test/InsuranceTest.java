package insurance;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class InsuranceTest {
	
	
		private insurance.InsuranceCalculator insurance;
		private insurance.Client client;

		@BeforeEach
		public void setUp() {
			insurance = new insurance.InsuranceCalculator();
			client = new Client();								
		}

		@Test
		public void testException() throws InvalidClientData {		
			client.numberAccidents = -1;
			Assertions.assertThrows(InvalidClientData.class, ()->insurance.getClientDeductible(client));
		}
		
		@Test 
		public void testInvalidAge() throws InvalidClientData {
			client.age = -1;
			Assertions.assertThrows(InvalidClientData.class, ()->insurance.getClientDeductible(client));
			client.age = 150;
			Assertions.assertThrows(InvalidClientData.class, ()->insurance.getClientDeductible(client));
		}
		
		@Test 
		public void testInvalidYearLicence() throws InvalidClientData {
			client.yearLicence = -1;
			Assertions.assertThrows(InvalidClientData.class, ()->insurance.getClientDeductible(client));
		}
		
		@Test 
		public void testInvalidYearLastAccident() throws InvalidClientData {
			client.yearLastAccident = -1;
			Assertions.assertThrows(InvalidClientData.class, ()->insurance.getClientDeductible(client));
		}
		
		@Test
		public void testDeductibleAge() throws InvalidClientData {
			client.yearLicence = 0;
			client.age = 31;
			Assertions.assertEquals(insurance.getClientDeductible(client), 5000);
			client.age = 30;
			Assertions.assertEquals(insurance.getClientDeductible(client), 5000);
			client.age = 29;
			Assertions.assertEquals(insurance.getClientDeductible(client), 8000);
		}
		
		@Test
		public void testDeductibleLicence() throws InvalidClientData {
			client.age = 20;
			client.yearLicence = 4;
			Assertions.assertEquals(insurance.getClientDeductible(client), 8000);
			client.yearLicence = 5;
			Assertions.assertEquals(insurance.getClientDeductible(client), 5000);
			client.yearLicence = 6;
			Assertions.assertEquals(insurance.getClientDeductible(client), 5000);
		}
		
		@Test
		public void testDeductibleNumberAccidentsLowBase() throws InvalidClientData {
			client.age = 40; //5000 Base deductible.
			int[] deductibles = new int[10];
			for(int i = 0; i < 10; i++) {
				client.numberAccidents = i;
				deductibles[i] = insurance.getClientDeductible(client);
			}
			assertAll("Group multiple number of Accidents",
					() -> assertEquals(5000, deductibles[0], "0 Accidents"),
					() -> assertEquals(6000, deductibles[1], "1 Accidents"),
					() -> assertEquals(7500, deductibles[2], "2 Accidents"),
					() -> assertEquals(9000, deductibles[3], "3 Accidents"),
					() -> assertEquals(15000, deductibles[4], "4 Accidents"),
					() -> assertEquals(15000, deductibles[5], "5 Accidents"),
					() -> assertEquals(15000, deductibles[6], "6 Accidents"),
					() -> assertEquals(15000, deductibles[7], "7 Accidents"),
					() -> assertEquals(15000, deductibles[8], "8 Accidents"),
					() -> assertEquals(15000, deductibles[9], "9 Accidents")
				
			);
		}
		
		@Test
		public void testDeductibleNumberAccidentsHighBase() throws InvalidClientData {
			client.age = 20; //8000 Base deductible.
			int[] deductibles = new int[10];
			for(int i = 0; i < 10; i++) {
				client.numberAccidents = i;
				deductibles[i] = insurance.getClientDeductible(client);
			}
			assertAll("Group multiple number of Accidents",
					() -> assertEquals(8000, deductibles[0], "0 Accidents"),
					() -> assertEquals(9000, deductibles[1], "1 Accidents"),
					() -> assertEquals(10500, deductibles[2], "2 Accidents"),
					() -> assertEquals(12000, deductibles[3], "3 Accidents"),
					() -> assertEquals(18000, deductibles[4], "4 Accidents"),
					() -> assertEquals(18000, deductibles[5], "5 Accidents"),
					() -> assertEquals(18000, deductibles[6], "6 Accidents"),
					() -> assertEquals(18000, deductibles[7], "7 Accidents"),
					() -> assertEquals(18000, deductibles[8], "8 Accidents"),
					() -> assertEquals(18000, deductibles[9], "9 Accidents")
				
			);
		}
		
		@Test
		public void testDeductibleNumberAccidentsGoldMember() throws InvalidClientData {
			client.age = 40; //5000 Base deductible.
			client.isGoldMember = true;
			int[] deductibles = new int[6];
			for(int i = 0; i < 6; i++) {
				client.numberAccidents = i;
				deductibles[i] = insurance.getClientDeductible(client);
			}
			assertAll("Group multiple number of Accidents",
					() -> assertEquals(5000, deductibles[0], "0 Accidents"),
					() -> assertEquals(5000, deductibles[1], "1 Accidents"),
					() -> assertEquals(5000, deductibles[2], "2 Accidents"),
					() -> assertEquals(9000, deductibles[3], "3 Accidents"),
					() -> assertEquals(15000, deductibles[4], "4 Accidents"),
					() -> assertEquals(15000, deductibles[5], "5 Accidents")
				
			);
		}
		
		@Test
		public void testMonthlyCost() throws InvalidClientData {
			client.age = 29; 
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 600);
			client.age = 30; 
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 500);
			client.age = 31; 
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 500);
		}

		@Test
		public void testMonthlyCostLicence() throws InvalidClientData {
			client.yearLicence = 4;
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 600);
			client.yearLicence = 5; 
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 500);
			client.yearLicence = 6; 
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 500);
		}
		
		@Test
		public void testMonthlyCostMultipleCars() throws InvalidClientData {
			client.age = 20;
			client.cars.add(new Car());
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 600);
			client.cars.add(new Car());
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 800);
			client.cars.add(new Car());
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 1000);
		}
		
		@Test
		public void testMonthlyCostRedCars() throws InvalidClientData {
			client.age = 20;
			client.cars.add(new Car());
			client.cars.get(0).isRed = true;
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 700);
			client.cars.add(new Car());
			client.cars.get(1).isRed = true;
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 1000);
		}
		
		@Test
		public void testMonthlyCostDiscount() throws InvalidClientData {
			client.age = 20;
			client.yearInsurance = 0;
			client.yearLastAccident = 0;
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 600);
			
			client.yearInsurance = 1;
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 540);
			
			client.yearLastAccident = 1;
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 600);
			
			client.isGoldMember = true;
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 540);
			
			client.isGoldMember = false;
			Assertions.assertEquals(insurance.MonthlyInsuranceCost(client), 600);
			
		}
}
