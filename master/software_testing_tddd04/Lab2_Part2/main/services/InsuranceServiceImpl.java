package se.liu.ida.InsuranceApp.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import se.liu.ida.InsuranceApp.data.ClientProfile;

@Service
public class InsuranceServiceImpl implements InsuranceService {

	@Autowired
	private ClientDataManagementService clientDB;
	private int counter;
	
	
	public InsuranceServiceImpl(ClientDataManagementService clientDB) {
		this.clientDB = clientDB;
		counter = 0;
	}
	
	@Override
	public Integer clientNumber() {
		return counter;
	}

	@Override
	public Boolean isClientGoldMember(int clientId) {
		ClientProfile cl = clientDB.findById(clientId);
		return cl.getGoldMember();
	}
	
	@Override
	public Boolean registerNewMember(String lastName, String firstName, int yearOfBirth,
			int yearOfLicence) {
		ClientProfile new_c = new ClientProfile(counter++, lastName, firstName, yearOfBirth, yearOfLicence);
		clientDB.addClientProfile(new_c);
		return true;
	}
	
	@Override
	public int registerNewAccident(int clientId) {
		// TODO Auto-generated method stub
		return 0;
	}
	@Override
	public Boolean updateDatabase() {
		// TODO Auto-generated method stub
		return null;
	}
	@Override
	public int getClientDeductible(int clientId) {
		// TODO Auto-generated method stub
		return 0;
	}
	@Override
	public int MonthlyInsuranceCost(int clientId) {
		// TODO Auto-generated method stub
		return 0;
	}
	
	@Override
	public Boolean addNewCarToMember(int id, String color, int year) {
		// TODO Auto-generated method stub
		return null;
	}
	@Override
	public ClientProfile getClientProfile(int id) {
		// TODO Auto-generated method stub
		return null;
	}

}
