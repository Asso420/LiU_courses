package se.liu.ida.InsuranceApp;



import org.mockito.Mockito;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.context.annotation.Profile;

import se.liu.ida.InsuranceApp.services.InsuranceService;

@Profile("mockInsuranceService")
@Configuration
public class MockInsuranceServiceConfig {
	
	@Bean
	@Primary
	public InsuranceService insuranceService() {
		InsuranceService is =  Mockito.mock(InsuranceService.class);
			
	    
		/** Add mocked behavior */
		Mockito.when(is.clientNumber())
	    	.thenReturn(10);
		
		// ??????????????????????????????????????? 
		Mockito.when(is.MonthlyInsuranceCost(Mockito.anyInt()))
       		.thenReturn(500);
		
		Mockito.when(is.getClientDeductible(Mockito.anyInt()))
       		.thenReturn(5000);

		 return is;
	}

}
