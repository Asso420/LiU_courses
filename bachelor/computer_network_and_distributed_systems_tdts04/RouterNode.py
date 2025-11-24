#!/usr/bin/env python
import GuiTextArea, RouterPacket, F
from copy import deepcopy

class RouterNode():
    myID = None
    myGUI = None
    sim = None
    costs = None # We see this as distance vector for this router

    # --------------------------------------------------
    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea("  Output window for Router #" + str(ID) + "  ")
        self.myGUI.println("Running init for router {}".format(self.myID))
        self.costs = deepcopy(costs)
        self.neighborsCosts = {} # cost to my neighbors
        self.distanceTable = {self.myID: self.costs} # Contains my and my neighbors costs
        self.nextRouter = {} # A dictionary which contains next router to each destination 
        

        # A dictionary for saving neighbors and corresponding cost
        for j, cost in enumerate(self.sim.connectcosts[self.myID]):
            if j != self.myID and cost != self.sim.INFINITY and cost != 0:
                self.neighborsCosts[j] = cost

        
        # Building distanceTable containing my and my neighbors distance vector
        for neighbor in self.neighborsCosts:
                self.distanceTable[neighbor] = [0 if node == neighbor else self.sim.INFINITY 
                                      for node in range(self.sim.NUM_NODES)]

                    
        self.myGUI.println("Distance vectors in router {} is.".format(self.myID))
        for i in sorted(self.distanceTable):
            self.myGUI.println( str(i) + " : " + str(self.distanceTable[i]))

        # Finds next router for every destination. If destination is not known yet it is '-' for now.
        for i in range(self.sim.NUM_NODES):
            self.nextRouter[i] = i if i in self.neighborsCosts and i != self.myID else '?'

    
        # Sending updates to neighbors after initializing
        self.update_all()
        
    # --------------------------------------------------
    # Receiving the updates and calculating after that
    def recvUpdate(self, packet):
        source_id = packet.sourceid
        min_cost = packet.mincost
        self.myGUI.println(f"\nReceived packet - Source: {source_id} Data: {min_cost}")
        if self.distanceTable[source_id] != min_cost:
            self.distanceTable[source_id] = min_cost
            self.bellman_ford()
        

    # --------------------------------------------------
    def sendUpdate(self, pkt):
        self.sim.toLayer2(pkt)
    
    # --------------------------------------------------
    def update_all(self):
        for n in self.neighborsCosts:
            if(n != self.myID):
                pkt = RouterPacket.RouterPacket(self.myID, n, deepcopy(self.costs))
                self.sendUpdate(pkt)
    
    # --------------------------------------------------
    def printTableStart(self):
        self.myGUI.print("     dst\t|") 
        for n in range(self.sim.NUM_NODES):
            self.myGUI.print('\t' + str(n))
        self.myGUI.print("\n--------")
        for n in range(self.sim.NUM_NODES):
            self.myGUI.print("---------")
        self.myGUI.print("\n")
    # --------------------------------------------------
    def printDistanceTable(self):
        self.myGUI.println("Current table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime()))

        # Print distance table
        self.myGUI.println("Distancetable:")
        self.printTableStart()

        # Print distance vectors for neighbors
        sorted_distanceTable = sorted(self.distanceTable.items())

# Print distance vectors for neighbors
        for neighbor, distances in sorted_distanceTable:
            self.myGUI.print(" nbr {}  |".format(neighbor))
            self.myGUI.print("".join("{:>8}".format(distance) for distance in distances))
            self.myGUI.println()

        # Print our distance vector and routes
        self.myGUI.println("Our distance vector and routes:")
        self.printTableStart()
        # Print cost line
        self.myGUI.print(" cost   |")
        self.myGUI.print("".join("{:>8}".format(cost) for cost in self.costs))

        # Print route line
        self.myGUI.println()
        self.myGUI.print(" route  |")
        self.myGUI.print("".join("{:>8}".format(self.nextRouter[i]) for i in range(self.sim.NUM_NODES)))
        self.myGUI.println()

       
    # --------------------------------------------------
    def updateLinkCost(self, destination, new_cost):
        self.myGUI.println("Destination is {} and the new cost is {}".format(destination, new_cost))
        self.neighborsCosts[destination] = new_cost

        if self.sim.POISONREVERSE:
        # If Poison Reverse is enabled, set infinite cost for neighbors using this route
            for neighbor, cost in self.neighborsCosts.items():
                if neighbor != destination and self.sim.nodes[neighbor].nextRouter[destination] == self.myID:
                    self.distanceTable[neighbor][destination] = self.sim.INFINITY

        self.bellman_ford()
        
    # --------------------------------------------------
    def bellman_ford(self):
        changed = False

        # Iterate over each destination node
        for n in range(self.sim.NUM_NODES):
            if n == self.myID:
                continue

            # Initialize minimum cost for this destination
            min_cost = self.sim.INFINITY

            # Find the minimum cost to reach the destination
            for neighbor, neighbor_cost in self.neighborsCosts.items():
                # Calculate the cost to reach the destination through the neighbor
                total_cost = neighbor_cost + self.distanceTable[neighbor][n]

                # Update the minimum cost if the new route is cheaper
                if total_cost < min_cost:
                    min_cost = total_cost
                    self.nextRouter[n] = neighbor

            # Update the cost for this destination if it has changed
            if self.costs[n] != min_cost:
                self.costs[n] = min_cost
                changed = True

        # If there is any change in costs, inform neighbors
        if changed:
            self.update_all()


            CREATE PROCEDURE addReservation(IN departure_airport_code VARCHAR(3), arrival_airport_code VARCHAR(3), flight_year INT,
                                flight_week INT, flight_day VARCHAR(30), time TIME, number_of_passengers INT,
                                OUT output_reservation_nr INT)
BEGIN
    SET @RouteID = (SELECT ID
                    FROM Route
                    WHERE `To` = arrival_airport_code
                      AND `From` = departure_airport_code
                      AND `Year` = flight_year);

    IF (@RouteID IS NULL) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Route does not exist';
    END IF;

    SET @WeeklyFlightID = (SELECT ID
                           FROM WeeklySchedule
                           WHERE `Route` = @RouteID
                             AND `TimeOfDeparture` = time
                             AND `Weekday` = flight_day
                             AND `Year` = flight_year);

    IF (@WeeklyFlightID IS NULL) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Weekly flight does not exist';
    END IF;

    SET @FlightNumber = (SELECT FlightNumber
                         FROM Flight
                         WHERE `WeeklyFlight` = @WeeklyFlightID
                           AND `Week` = flight_week);

    IF (@FlightNumber IS NULL) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Flight does not exist';
    END IF;

    /* If there are enough seats on the flight, generate a reservation number and insert into reservation */
    IF (calculateFreeSeats(@FlightNumber) >= number_of_passengers) THEN
        SET @ReservationNumberExists = 1;

        /* If ReservationNumber already exists, generate new one */
        WHILE @ReservationNumberExists
            DO
                /* Random number 1 to integer limit */
                SET output_reservation_nr = FLOOR(RAND() * 2147483647);
                SET @ReservationNumberExists = (SELECT COUNT(1)
                                                FROM Reservation
                                                WHERE `ReservationNumber` = output_reservation_nr);
            END WHILE;

        /* Insert reservation to flight in Reservation */
        INSERT INTO Reservation (`ReservationNumber`, `FlightNumber`)
        VALUES (output_reservation_nr, @FlightNumber);
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not enough seats on flight';
    END IF;
END//
