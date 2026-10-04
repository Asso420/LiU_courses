package se.liu.ida.InsuranceApp.services;

import org.springframework.stereotype.Service;

import se.liu.ida.InsuranceApp.data.ClientProfile;

@Service
public interface ClientDataManagementService {
	ClientProfile findById(int id);
	Boolean updateClientProfile(int id, ClientProfile c);
	Boolean addClientProfile(ClientProfile c);
	Boolean removeClientProfile(int id);
}
