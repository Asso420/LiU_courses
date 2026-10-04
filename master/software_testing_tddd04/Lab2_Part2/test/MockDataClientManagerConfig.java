package se.liu.ida.InsuranceApp;

import java.util.HashMap;
import java.util.Vector;

import org.mockito.Mockito;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.stubbing.Answer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.context.annotation.Profile;

import se.liu.ida.InsuranceApp.data.ClientProfile;
import se.liu.ida.InsuranceApp.services.ClientDataManagementService;

@Profile("mockClientManager")
@Configuration
public class MockDataClientManagerConfig {
	
	@Bean
	@Primary
	public ClientDataManagementService clientDataManagementService() {
		ClientDataManagementService cs =  Mockito.mock(ClientDataManagementService.class);		
		ClientProfile Client = new ClientProfile(1, "Jo", "Smith", 1980, 2000);
	    
		/** Add mocked behavior */
		Mockito.when(cs.findById(1))
			.thenReturn(Client);

		return cs;
	}
}
