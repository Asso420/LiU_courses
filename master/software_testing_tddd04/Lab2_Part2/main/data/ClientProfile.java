package se.liu.ida.InsuranceApp.data;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Date;

public class ClientProfile {
	
	private int 		clientId;
	private String 		lastName;
	private String 		firstName;
	private int 		yearOfBirth;
	private int 		yearOfLicence;
	private int			yearBecameClient;
	private int 		numberOfAccidentsThisYear;
	private int			yearsWithoutAccidents;
	private Boolean 	goldMember;
	private Date		insuranceExpiryDate;
	private ArrayList<CarData> carsInsured;
	

	public ClientProfile(int clientId, String lastName, String firstName,
			int yearOfBirth, int yearOfLicence) {
		this.setClientId(clientId);
		this.lastName = lastName;
		this.firstName = firstName;
		this.yearOfBirth = yearOfBirth;
		this.yearOfLicence = yearOfLicence;
		yearBecameClient = LocalDate.now().getYear();
		numberOfAccidentsThisYear = 0;
		yearsWithoutAccidents = 0;
		goldMember = false;
		carsInsured = new ArrayList<CarData>();
	}
	public void addCarInsured(CarData newCar) {
		this.carsInsured.add(newCar);
	}
	public int getClientId() {
		return clientId;
	}
	public void setClientId(int clientId) {
		this.clientId = clientId;
	}
	public String getLastName() {
		return lastName;
	}
	public void setLastName(String lastName) {
		this.lastName = lastName;
	}
	public String getFirstName() {
		return firstName;
	}
	public void setFirstName(String firstName) {
		this.firstName = firstName;
	}
	public int getYearOfBirth() {
		return yearOfBirth;
	}
	public void setYearOfBirth(int yearOfBirth) {
		this.yearOfBirth = yearOfBirth;
	}
	public int getYearOfLicence() {
		return yearOfLicence;
	}
	public void setYearOfLicence(int yearOfLicence) {
		this.yearOfLicence = yearOfLicence;
	}
	public int getYearBecameClient() {
		return yearBecameClient;
	}
	public void setYearBecameClient(int yearBecameClient) {
		this.yearBecameClient = yearBecameClient;
	}
	public int getNumberOfAccidentsThisYear() {
		return numberOfAccidentsThisYear;
	}
	public void setNumberOfAccidentsThisYear(int numberOfAccidentsThisYear) {
		this.numberOfAccidentsThisYear = numberOfAccidentsThisYear;
	}
	public int getYearsWithoutAccidents() {
		return yearsWithoutAccidents;
	}
	public void setYearsWithoutAccidents(int yearsWithoutAccidents) {
		this.yearsWithoutAccidents = yearsWithoutAccidents;
	}
	public Boolean getGoldMember() {
		return goldMember;
	}
	public void setGoldMember(Boolean goldMember) {
		this.goldMember = goldMember;
	}
	public Date getInsuranceExpiryDate() {
		return insuranceExpiryDate;
	}
	public void setInsuranceExpiryDate(Date insuranceExpiryDate) {
		this.insuranceExpiryDate = insuranceExpiryDate;
	}
	public ArrayList<CarData> getCarsInsured() {
		return carsInsured;
	}
	public void setCarsInsured(ArrayList<CarData> carsInsured) {
		this.carsInsured = carsInsured;
	}
	
		
}
