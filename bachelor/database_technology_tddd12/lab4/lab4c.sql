/*
Lab 2, Report
Mohammad Rajabi (mohra735) 
Ahmad Soltani (ahamso698) 
Morteza Miri (mormi475)

Last editted: 2024-05-16
*/

/*
Drop all user created tables that have been created when solving the lab.
*/
SELECT 'Dropping tables' AS 'Message';

DROP TABLE IF EXISTS passenger_reservation CASCADE;
DROP TABLE IF EXISTS payed_reservation CASCADE;
DROP TABLE IF EXISTS is_contact_for CASCADE;
DROP TABLE IF EXISTS passenger CASCADE;
DROP TABLE IF EXISTS booking CASCADE;
DROP TABLE IF EXISTS credit_card CASCADE;
DROP TABLE IF EXISTS reservation CASCADE;
DROP TABLE IF EXISTS flight CASCADE;
DROP TABLE IF EXISTS weekly_schedule CASCADE;
DROP TABLE IF EXISTS week_day CASCADE;
DROP TABLE IF EXISTS route CASCADE;
DROP TABLE IF EXISTS airport CASCADE;
DROP TABLE IF EXISTS yearly_factor CASCADE;

/*
Drop all Procedures.
*/
DROP PROCEDURE IF EXISTS addYear;
DROP PROCEDURE IF EXISTS addDay;
DROP PROCEDURE IF EXISTS addDestination;
DROP PROCEDURE IF EXISTS addRoute;
DROP PROCEDURE IF EXISTS addFlight;
DROP PROCEDURE IF EXISTS addReservation;
DROP PROCEDURE IF EXISTS addPassenger;
DROP PROCEDURE IF EXISTS addContact;
DROP PROCEDURE IF EXISTS addPayment;


/*
Drop all Functions.
*/
DROP FUNCTION IF EXISTS calculateFreeSeats;
DROP FUNCTION IF EXISTS calculatePrice;

/*
Drop all Triggers.
*/
DROP TRIGGER IF EXISTS IssueTicketNumber;
/*
Drop all Views.
*/
DROP VIEW IF EXISTS allFlights;

/*
Create the tables according to Relation Schema.
*/

SELECT 'Creating tables' AS 'Message';

CREATE TABLE airport
(   
   name VARCHAR(30),
   country VARCHAR(30),
   airport_code VARCHAR(3),
   CONSTRAINT pk_Airport PRIMARY KEY(airport_code)
);


CREATE TABLE route
(
   route_id INT AUTO_INCREMENT,
   route_price DOUBLE,
   departure_ap VARCHAR(3),
   arrival_ap VARCHAR(3),
   year INT,
   CONSTRAINT pk_route PRIMARY KEY(route_id)
);

CREATE TABLE yearly_factor
(
   year INT,
   yearly_factor DOUBLE,
   CONSTRAINT pk_yearly_factor PRIMARY KEY(year)
);

CREATE TABLE week_day
(
   year INT,
   day VARCHAR(10),
   day_factor DOUBLE,
   CONSTRAINT pk_week_day PRIMARY KEY(year, day)
);

CREATE TABLE flight
(
   flight_num INT AUTO_INCREMENT,
   week_id INT,
   week_num INT,
   num_of_free_seats INT DEFAULT 40,
   CONSTRAINT pk_flight PRIMARY KEY(flight_num)
);

CREATE TABLE weekly_schedule
(
   id INT AUTO_INCREMENT,
   dep_time TIME,
   year INT,
   day VARCHAR(10),
   route_id INT,
   CONSTRAINT pk_weekly_schedule PRIMARY KEY(id)
);

CREATE TABLE reservation
(
   res_num INT,
   num_of_reserved_seats INT DEFAULT 0,
   flight_num INT,
   CONSTRAINT pk_reservation PRIMARY KEY(res_num)
);

CREATE TABLE booking
(
   booking_id INT AUTO_INCREMENT,
   res_num INT,
   card_num BIGINT,
   total_price INT,
   CONSTRAINT pk_booking PRIMARY KEY(booking_id)
);

CREATE TABLE credit_card
 (
   card_num BIGINT,
   card_holder VARCHAR(30),
   CONSTRAINT pk_credit_card PRIMARY KEY(card_num)
 );

CREATE TABLE passenger
 (
   pass_num INT,
   f_name VARCHAR(30),
   l_name VARCHAR(30),
   CONSTRAINT pk_passenger PRIMARY KEY(pass_num)
 );


CREATE TABLE is_contact_for
(
   pass_num INT,
   res_num INT,
   email VARCHAR(30),
   phone_number BIGINT,
   CONSTRAINT pk_is_contact_for PRIMARY KEY(res_num)
);

CREATE TABLE payed_reservation
(
   pass_num INT,
   booking_id INT,
   ticket_number INT,
   CONSTRAINT pk_payed_reservation PRIMARY KEY(pass_num, booking_id)
);

CREATE TABLE passenger_reservation
(
   pass_num INT,
   res_num INT,
   CONSTRAINT pk_passenger_reservation PRIMARY KEY(pass_num, res_num)
);

/*
Adding foreign keys to the defined tables.
*/
SELECT 'Creating foreign keys' AS 'Message';
/*FK for rout*/
ALTER TABLE route ADD CONSTRAINT fk_dep_airport FOREIGN KEY (departure_ap) REFERENCES airport(airport_code);
ALTER TABLE route ADD CONSTRAINT fk_arr_airport FOREIGN KEY (arrival_ap) REFERENCES airport(airport_code);
ALTER TABLE route ADD CONSTRAINT fk_route_year FOREIGN KEY (year) REFERENCES yearly_factor(year);

/*FK for week_day*/
ALTER TABLE week_day ADD CONSTRAINT fk_week_day_year FOREIGN KEY (year) REFERENCES yearly_factor(year);

/*FK for flight*/
ALTER TABLE flight ADD CONSTRAINT fk_flight_flight_num FOREIGN KEY (week_id) REFERENCES weekly_schedule(id);

/*weekly_schedule*/
ALTER TABLE weekly_schedule ADD CONSTRAINT fk_ws_year FOREIGN KEY (year) REFERENCES yearly_factor(year);
ALTER TABLE weekly_schedule ADD CONSTRAINT fk_ws_route FOREIGN KEY (route_id) REFERENCES route(route_id);
ALTER TABLE weekly_schedule ADD CONSTRAINT fk_ws_year_day FOREIGN KEY (year, day) REFERENCES week_day(year, day);

/*FK for reservation*/
ALTER TABLE reservation ADD CONSTRAINT fk_flight_num FOREIGN KEY (flight_num) REFERENCES flight(flight_num);

/*FK for booking*/
ALTER TABLE booking ADD CONSTRAINT fk_res_num FOREIGN KEY (res_num) REFERENCES reservation(res_num);
ALTER TABLE booking ADD CONSTRAINT fk_card_num FOREIGN KEY (card_num) REFERENCES credit_card(card_num);

/*FK for is_contact_for*/
ALTER TABLE is_contact_for ADD CONSTRAINT fk_pass_num FOREIGN KEY (pass_num) REFERENCES passenger(pass_num);
ALTER TABLE is_contact_for ADD CONSTRAINT fk_contact_for_res_num FOREIGN KEY (res_num) REFERENCES reservation(res_num);

/*FK for payed reservation*/
ALTER TABLE payed_reservation ADD CONSTRAINT fk_payed_pass_num FOREIGN KEY (pass_num) REFERENCES passenger(pass_num);
ALTER TABLE payed_reservation ADD CONSTRAINT fk_booking_id FOREIGN KEY (booking_id) REFERENCES booking(booking_id);

/*FK for passenger reservation*/
ALTER TABLE passenger_reservation ADD CONSTRAINT fk_passenger_pass_num FOREIGN KEY (pass_num) REFERENCES passenger(pass_num);
ALTER TABLE passenger_reservation ADD CONSTRAINT fk_passenger_res_num FOREIGN KEY (res_num) REFERENCES reservation(res_num);

/*
Defining the procedures.
*/
SELECT "Defining stored procedures." AS "Message";

DELIMITER //
/*----------------------------PROCEDURES-----------------------------*/
CREATE PROCEDURE addYear(IN year INT, IN factor DOUBLE)
BEGIN
   INSERT INTO yearly_factor (year, yearly_factor) 
   VALUES (year, factor);
END//

/*-------------------------------------------------------------------*/
CREATE PROCEDURE addDay(IN year INT, IN day VARCHAR(10), IN day_factor DOUBLE)
BEGIN
   INSERT INTO week_day (year, day, day_factor) 
   VALUES (year, day, day_factor);
END//

/*-------------------------------------------------------------------*/
CREATE PROCEDURE addDestination(IN airport_code VARCHAR(3), IN name VARCHAR(30), IN country VARCHAR(30))
BEGIN
   INSERT INTO airport(name, country, airport_code) 
   VALUES (name, country, airport_code);
END//

/*-------------------------------------------------------------------*/
CREATE PROCEDURE addRoute(IN departure_airport_code VARCHAR(3), IN arrival_airport_code VARCHAR(3),
                          IN year INT, IN routeprice DOUBLE)
BEGIN
   INSERT INTO route(route_price, departure_ap, arrival_ap, year) 
   VALUES (routeprice, departure_airport_code, arrival_airport_code, year);
END//

/*-------------------------------------------------------------------*/
CREATE PROCEDURE addFlight(IN departure_airport_code VARCHAR(3), IN arrival_airport_code VARCHAR(3),
                           IN year INT,IN day VARCHAR(10), IN departure_time TIME)
BEGIN
   /*Inserting information into weekly_schedule:*/
   DECLARE route_id_1 INT;
   DECLARE week_id_1 INT;

   SELECT route.route_id INTO route_id_1 FROM route WHERE((departure_airport_code = route.departure_ap)
                                                AND(arrival_airport_code = route.arrival_ap)
                                                AND(route.year = year));

   INSERT INTO weekly_schedule(dep_time, year, day, route_id) 
   VALUES (departure_time, year, day, route_id_1);

   /*Inserting information into flight:*/
   

   SELECT weekly_schedule.id  INTO week_id_1 FROM weekly_schedule
                                            WHERE((weekly_schedule.dep_time = departure_time)
                                                AND(weekly_schedule.year = year)
                                                AND(weekly_schedule.day = day)
                                                AND(weekly_schedule.route_id = route_id_1));
   FOR i IN 1..52
      DO
         INSERT INTO flight(week_id, week_num) 
         VALUES (week_id_1, i);
   END FOR;
END//

/*----------------------------FUNCTIONS-----------------------------*/
SELECT "Defining Functions." AS "Message"//

CREATE FUNCTION calculateFreeSeats(flightnumber INT)
RETURNS INT
BEGIN
   DECLARE free_seats INT;

   SELECT num_of_free_seats INTO free_seats FROM flight WHERE (flight_num = flightnumber);
   RETURN free_seats;
END//

/*-------------------------------------------------------------------*/
CREATE FUNCTION calculatePrice(flightnumber INT)
RETURNS DOUBLE
BEGIN
   DECLARE seat_price DOUBLE;
   DECLARE week_id INT;
   DECLARE route_id INT;
   DECLARE route_price DOUBLE;
   DECLARE flight_year INT;
   DECLARE flight_day VARCHAR(10);
   DECLARE yearly_factor DOUBLE;
   DECLARE daily_factor DOUBLE;
   DECLARE num_of_free_seats INT;
   DECLARE num_of_booked_seats INT;


   SELECT flight.week_id INTO week_id FROM flight WHERE (flight.flight_num = flightnumber);
   SELECT flight.num_of_free_seats INTO num_of_free_seats FROM flight WHERE (flight.flight_num = flightnumber);
   SELECT weekly_schedule.route_id INTO route_id FROM weekly_schedule WHERE (week_id = id);
   SELECT weekly_schedule.day INTO flight_day FROM weekly_schedule WHERE (week_id = id);
   SELECT route.route_price INTO route_price FROM route WHERE (route_id = route.route_id);
   SELECT route.year INTO flight_year FROM route WHERE (route_id = route.route_id);
   SELECT yearly_factor.yearly_factor INTO yearly_factor FROM yearly_factor WHERE (yearly_factor.year = flight_year);
   SELECT week_day.day_factor INTO daily_factor FROM week_day WHERE ((week_day.year = flight_year) 
                                                              AND (week_day.day = flight_day));                                                           
   SET num_of_booked_seats = 40 - num_of_free_seats;
   SET seat_price = ROUND((route_price * daily_factor * ((num_of_booked_seats+1)/40) * yearly_factor), 3);
   
   RETURN seat_price;
END//

/*-----------------------------Triggers----------------------------*/

SELECT "Defining tiggers." AS "Message"//

CREATE TRIGGER IssueTicketNumber AFTER INSERT ON booking
FOR EACH ROW
BEGIN
   DECLARE done INT DEFAULT FALSE;
   DECLARE pass_num_1 INT;
   DECLARE generated_ticket_num INT;
   DECLARE pass_cur CURSOR FOR SELECT pass_num FROM passenger_reservation
   WHERE (passenger_reservation.res_num = NEW.res_num);
   DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
   
   OPEN pass_cur;
   generate_ticket: LOOP
      FETCH pass_cur INTO pass_num_1;
      IF done THEN
         LEAVE generate_ticket;
      END IF;
      SET generated_ticket_num = FLOOR(RAND()*10000);

      /*check if the generated ticket number is unique*/
      WHILE EXISTS (SELECT * FROM payed_reservation 
                     WHERE payed_reservation.ticket_number = generated_ticket_num) DO
         SET generated_ticket_num = FLOOR(RAND()*10000);
      END WHILE;
      
      INSERT INTO payed_reservation(pass_num, booking_id, ticket_number)
      VALUES (pass_num_1, NEW.booking_id, generated_ticket_num);
   END LOOP;
   CLOSE pass_cur;
END//


/*-----------------------------Procedures(6)----------------------------*/
/*-----------------------------addReservation---------------------------*/
CREATE PROCEDURE addReservation(IN departure_airport_code VARCHAR(3), IN arrival_airport_code VARCHAR(3),
                                 IN year INT, IN week INT, IN day VARCHAR(10),IN time TIME, 
                                    IN number_of_passengers INT,OUT output_reservation_nr INT)

BEGIN
   DECLARE route_id_1 INT;
   DECLARE week_id_1 INT;
   DECLARE flight_num_1 INT;

    -- Find route_id
   SET route_id_1 = (SELECT route_id 
                     FROM route 
                     WHERE route.departure_ap = departure_airport_code 
                     AND route.arrival_ap = arrival_airport_code 
                     AND route.year = year);
   
    -- Find week_id
   SET week_id_1 = (SELECT id 
                  FROM weekly_schedule 
                  WHERE weekly_schedule.route_id = route_id_1 
                  AND weekly_schedule.day = day 
                  AND weekly_schedule.year = year 
                  AND weekly_schedule.dep_time = time);

    -- Find flight number
   SET flight_num_1 = (SELECT flight_num 
                     FROM flight 
                     WHERE flight.week_id = week_id_1 
                     AND flight.week_num = week);
-- Det finns en test där dem ange en felaktig flight
   IF flight_num_1 IS NULL THEN 
      SELECT "There exist no flight for the given route, date and time." AS "Message";
   ELSEIF (number_of_passengers <= calculateFreeSeats(flight_num_1)) THEN
   -- Check if the number of passengers can be accommodated
      SET output_reservation_nr = FLOOR(RAND() * 10000);
      
      -- Ensure unique reservation number
      WHILE EXISTS (SELECT 1 FROM reservation WHERE reservation.res_num = output_reservation_nr) DO
         SET output_reservation_nr = FLOOR(RAND() * 10000);
      END WHILE;
      INSERT INTO reservation (res_num, flight_num)
      VALUES (output_reservation_nr, flight_num_1);
   ELSE
      SET output_reservation_nr = FLOOR(RAND() * 10000);
      -- Ensure unique reservation number
      WHILE EXISTS (SELECT 1 FROM reservation WHERE reservation.res_num = output_reservation_nr) DO
         SET output_reservation_nr = FLOOR(RAND() * 10000);
      END WHILE;
      INSERT INTO reservation (res_num, flight_num)
      VALUES (output_reservation_nr, flight_num_1);

      SELECT "There are not enough seats available on the chosen flight." AS "Message";
   END IF;
END //
/*----------------------------------------addPassenger----------------------------------------*/
CREATE PROCEDURE addPassenger (IN reservation_nr INT, IN passport_number INT, IN name VARCHAR(30))
BEGIN
   DECLARE first_name VARCHAR(30);
   DECLARE last_name VARCHAR(30);
   /*Vi måste kolla om res_num finns i reservation tables samt att pass_num finns ej i booking. */

   IF EXISTS (SELECT 1 FROM reservation WHERE res_num = reservation_nr) AND
   NOT EXISTS (SELECT 1 FROM booking WHERE booking.res_num = reservation_nr) THEN
      IF EXISTS (SELECT 1 FROM passenger WHERE passenger.pass_num = passport_number) THEN
         INSERT INTO passenger_reservation (pass_num, res_num)
         VALUES (passport_number, reservation_nr);
      ELSE 
         SET first_name = SUBSTRING_INDEX(name, ' ', 1);
         SET last_name = SUBSTRING_INDEX(name, ' ', -1);
         INSERT INTO passenger (pass_num, f_name, l_name)
         VALUES (passport_number, first_name, last_name);
         INSERT INTO passenger_reservation (pass_num, res_num)
         VALUES (passport_number, reservation_nr);
      END IF;
      UPDATE reservation
      SET num_of_reserved_seats = num_of_reserved_seats + 1
      WHERE res_num = reservation_nr;
      
   ELSE
      SELECT "reservation_nr does not exist in the reservation table or the reservation is already paid!!!" AS "Message";
   END IF;

END //
/*----------------------------------------addContact----------------------------------------*/
CREATE PROCEDURE addContact(IN reservation_nr INT, IN passport_number INT, IN email VARCHAR(30),IN  phone BIGINT)
BEGIN
   IF NOT EXISTS (SELECT 1 FROM reservation WHERE res_num = reservation_nr) THEN
      SELECT "The given reservation number does not exist" as "Message";
   ELSEIF NOT EXISTS (SELECT 1 FROM passenger WHERE passenger.pass_num = passport_number) THEN
      SELECT "The person is not a passenger of the reservation" as "Message";
   ELSE
      INSERT INTO is_contact_for(pass_num, res_num, email, phone_number)
      VALUES(passport_number, reservation_nr, email, phone);
   END IF;
END //
/*----------------------------------------addPayment----------------------------------------*/

CREATE PROCEDURE addPayment (IN reservation_nr INT,
                             IN cardholder_name VARCHAR(30),
                             IN credit_card_number BIGINT)
BEGIN
   DECLARE flight_number INT;
   DECLARE number_of_passengers_on_res INT;
   DECLARE total_price_to_pay INT;

   SET flight_number = (SELECT flight_num 
                        FROM reservation 
                        WHERE reservation.res_num = reservation_nr);
   SET number_of_passengers_on_res = (SELECT num_of_reserved_seats
                                     FROM reservation 
                                     WHERE reservation.res_num = reservation_nr);
   SET total_price_to_pay = number_of_passengers_on_res * calculatePrice(flight_number);

   IF NOT EXISTS (SELECT 1 FROM reservation WHERE reservation.res_num = reservation_nr) THEN
      SELECT "The given reservation number does not exist" as "Message";
   ELSEIF NOT EXISTS(SELECT 1 FROM is_contact_for WHERE is_contact_for.res_num = reservation_nr) THEN
      SELECT "The reservation has no contact yet" as "Message";
   ELSEIF EXISTS (SELECT 1 FROM booking WHERE booking.res_num = reservation_nr) THEN
      SELECT "The booking has already been payed and no futher passengers can be added" as "Message";
   ELSEIF (number_of_passengers_on_res > calculateFreeSeats(flight_number)) THEN
      -- Delete all the reservations due to overbooking.
      DELETE FROM passenger_reservation 
      WHERE (passenger_reservation.res_num = reservation_nr);
      DELETE FROM is_contact_for
      WHERE (is_contact_for.res_num = reservation_nr);
      DELETE FROM reservation
      WHERE (reservation.res_num = reservation_nr);
      SELECT "There is not enough seats in the chosen flight, deleting resevation" as "Message";
   
   ELSE
      /*
      Uncomment the following row if you wish to have an overbooking in question 10.   
      */
      -- SELECT SLEEP(5);

      IF EXISTS (SELECT 1 FROM credit_card WHERE credit_card.card_num = credit_card_number) THEN
         INSERT INTO booking(res_num, card_num, total_price)
         VALUES (reservation_nr, credit_card_number, total_price_to_pay);
         UPDATE flight
        SET num_of_free_seats = num_of_free_seats - number_of_passengers_on_res
        WHERE flight.flight_num = flight_number;
      ELSE
         INSERT INTO credit_card(card_num, card_holder)
         VALUES(credit_card_number, cardholder_name);
         INSERT INTO booking(res_num, card_num, total_price)
         VALUES (reservation_nr, credit_card_number, total_price_to_pay);
         UPDATE flight
        SET num_of_free_seats = num_of_free_seats - number_of_passengers_on_res
        WHERE flight.flight_num = flight_number;
      END IF;
     
   END IF;
END //
/*-----------------------------Create View(7)----------------------------*/

CREATE VIEW allFlights AS
SELECT
   dep_airport.name AS departure_city_name,
   arr_airport.name AS destination_city_name,
   weekly_schedule.dep_time AS departure_time,
   weekly_schedule.day AS departure_day,
   flight.week_num AS departure_week,
   weekly_schedule.year AS departure_year,
   flight.num_of_free_seats AS nr_of_free_seats,
   calculatePrice(flight.flight_num) AS current_price_per_seat
FROM flight
JOIN weekly_schedule ON flight.week_id = weekly_schedule.id
JOIN route ON weekly_schedule.route_id = route.route_id
JOIN airport dep_airport ON route.departure_ap = dep_airport.airport_code
JOIN airport arr_airport ON route.arrival_ap = arr_airport.airport_code//
DELIMITER ;

