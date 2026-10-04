package insurance;

public class InsuranceCalculator {
	/**
	 * Calculate the deductible for the client
	 * Base cost is 5000 SEK if the client is above 30 or has had a driving licence for more that 5 years and 8000 SEK otherwise
	 * With every accident for that calendar the deductible increases:
	 * 1 accident 	: by 1000 SEK
	 * 2 accidents  : by 2500 SEK
	 * 3 accidents	: by 4000 SEK
	 * 4 accidents and more by : 10000 SEK
	 * If the client if a gold member, then for the first 2 accidents, there is no increase
	 * but for 3 accidents and more normal rates apply
	 * 
	 * @param clientId
	 * @return the ammount of the deductible
	 * @throws InvalidClientData 
	 */
	int getClientDeductible (Client cl) throws InvalidClientData {
		
		int baseDeduct = 8000;
		
		if (cl.numberAccidents < 0)
			throw new InvalidClientData();
		if (cl.age < 0 || cl.age > 125)
			throw new InvalidClientData();
		if (cl.yearLicence < 0 || cl.yearLicence > cl.age)
			throw new InvalidClientData();
		if (cl.yearLastAccident < 0)
			throw new InvalidClientData();
		
		if (cl.age >= 30 || cl.yearLicence >= 5)
			baseDeduct = 5000;
		
		switch (cl.numberAccidents) {
		case 0:
			return baseDeduct;
		
		case 1:
			if (cl.isGoldMember)
				return baseDeduct;
			return baseDeduct + 1000;
		
		case 2:
			if (cl.isGoldMember)
				return baseDeduct;
			return baseDeduct + 2500;
			
		case 3:
			return baseDeduct + 4000;
		
		default:
			return baseDeduct + 10000;
			
		}
		
	}
	
	
	/**
	 * Calculate the monthly cost for the service for the client
	 * First year rate is 500SEK if the client is above 30 or has had a driving licence for more that 5 years and 600 SEK otherwise
	 * If the car is red the cost goes up by 100SEK
	 * Each additional car adds 200 SEK unless it is red then it adds 300SEK
	 * After the first year, there is a 10% discount if there were 0 accidents that year or if the client is a gold member
	 * @param clientId
	 * @return
	 */
	int MonthlyInsuranceCost(Client cl) {
		
		int baseCost = 600;
		
		if (cl.age >= 30 || cl.yearLicence >= 5)
			baseCost = 500;
		
		if (!cl.cars.isEmpty())	
			if (cl.cars.get(0).isRed)
				baseCost += 100;
			
			for (int i = 1; i < cl.cars.size(); i++) {
				if (cl.cars.get(i).isRed)
					baseCost += 300;
				else
					baseCost += 200;
			}
		
		if (cl.yearInsurance >= 1)
			if (cl.yearLastAccident == 0 || cl.isGoldMember)
				baseCost *= 0.9;
			
		return baseCost;
	}
}
