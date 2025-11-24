/*
Lab 2, Report
Mohammad Rajabi (mohra735) 
Ahmad Soltani (ahamso698) 
Morteza Miri (mormi475)

Last editted: 2024-04-12
*/

/*
Drop all user created tables that have been created when solving the lab
*/

DROP TABLE IF EXISTS custom_table CASCADE;


/* Have the source scripts in the file so it is easy to recreate!*/

SOURCE company_schema.sql;
SOURCE company_data.sql;
/**********************************************************************************/
/*
Question 1: List all employees, i.e., all tuples in the jbemployee relation.
*/

SELECT * 
FROM  jbemployee;

/*
+------+--------------------+--------+---------+-----------+-----------+
| id   | name               | salary | manager | birthyear | startyear |
+------+--------------------+--------+---------+-----------+-----------+
|   10 | Ross, Stanley      |  15908 |     199 |      1927 |      1945 |
|   11 | Ross, Stuart       |  12067 |    NULL |      1931 |      1932 |
|   13 | Edwards, Peter     |   9000 |     199 |      1928 |      1958 |
|   26 | Thompson, Bob      |  13000 |     199 |      1930 |      1970 |
|   32 | Smythe, Carol      |   9050 |     199 |      1929 |      1967 |
|   33 | Hayes, Evelyn      |  10100 |     199 |      1931 |      1963 |
|   35 | Evans, Michael     |   5000 |      32 |      1952 |      1974 |
|   37 | Raveen, Lemont     |  11985 |      26 |      1950 |      1974 |
|   55 | James, Mary        |  12000 |     199 |      1920 |      1969 |
|   98 | Williams, Judy     |   9000 |     199 |      1935 |      1969 |
|  129 | Thomas, Tom        |  10000 |     199 |      1941 |      1962 |
|  157 | Jones, Tim         |  12000 |     199 |      1940 |      1960 |
|  199 | Bullock, J.D.      |  27000 |    NULL |      1920 |      1920 |
|  215 | Collins, Joanne    |   7000 |      10 |      1950 |      1971 |
|  430 | Brunet, Paul C.    |  17674 |     129 |      1938 |      1959 |
|  843 | Schmidt, Herman    |  11204 |      26 |      1936 |      1956 |
|  994 | Iwano, Masahiro    |  15641 |     129 |      1944 |      1970 |
| 1110 | Smith, Paul        |   6000 |      33 |      1952 |      1973 |
| 1330 | Onstad, Richard    |   8779 |      13 |      1952 |      1971 |
| 1523 | Zugnoni, Arthur A. |  19868 |     129 |      1928 |      1949 |
| 1639 | Choy, Wanda        |  11160 |      55 |      1947 |      1970 |
| 2398 | Wallace, Maggie J. |   7880 |      26 |      1940 |      1959 |
| 4901 | Bailey, Chas M.    |   8377 |      32 |      1956 |      1975 |
| 5119 | Bono, Sonny        |  13621 |      55 |      1939 |      1963 |
| 5219 | Schwarz, Jason B.  |  13374 |      33 |      1944 |      1959 |
+------+--------------------+--------+---------+-----------+-----------+
25 rows in set (0.00 sec)
*/ 
/**********************************************************************************/
/*
Question 2: List the name of all departments in alphabetical order. Note: by “name”
we mean the name attribute in the jbdept relation.
*/

SELECT name 
FROM jbdept 
ORDER BY name ASC;

/*
+------------------+
| name             |
+------------------+
| Bargain          |
| Book             |
| Candy            |
| Children's       |
| Children's       |
| Furniture        |
| Giftwrap         |
| Jewelry          |
| Junior Miss      |
| Junior's         |
| Linens           |
| Major Appliances |
| Men's            |
| Sportswear       |
| Stationary       |
| Toys             |
| Women's          |
| Women's          |
| Women's          |
+------------------+
19 rows in set (0.00 sec)
*/
/**********************************************************************************/
/*
Question 3: What parts are not in store? Note that such parts have the value 0 (zero)
for the qoh attribute (qoh = quantity on hand).
*/

SELECT name 
FROM jbparts 
WHERE qoh = 0;

/*
+-------------------+
| name              |
+-------------------+
| card reader       |
| card punch        |
| paper tape reader |
| paper tape punch  |
+-------------------+
4 rows in set (0.00 sec)
*/
/**********************************************************************************/
/*
Question 4: List all employees who have a salary between 9000 (included) and
10000 (included)?
*/

SELECT name 
FROM jbemployee 
WHERE 9000 <= salary AND salary <= 10000;

/*
+----------------+
| name           |
+----------------+
| Edwards, Peter |
| Smythe, Carol  |
| Williams, Judy |
| Thomas, Tom    |
+----------------+
4 rows in set (0.00 sec)
*/
/**********************************************************************************/
/*
Question 5: List all employees together with the age they had when they started
working? Hint: use the startyear attribute and calculate the age in the
SELECT clause.S
*/

SELECT name, (startyear - birthyear) AS age_at_start 
FROM jbemployee;

/*
+--------------------+--------------+
| name               | age_at_start |
+--------------------+--------------+
| Ross, Stanley      |           18 |
| Ross, Stuart       |            1 |
| Edwards, Peter     |           30 |
| Thompson, Bob      |           40 |
| Smythe, Carol      |           38 |
| Hayes, Evelyn      |           32 |
| Evans, Michael     |           22 |
| Raveen, Lemont     |           24 |
| James, Mary        |           49 |
| Williams, Judy     |           34 |
| Thomas, Tom        |           21 |
| Jones, Tim         |           20 |
| Bullock, J.D.      |            0 |
| Collins, Joanne    |           21 |
| Brunet, Paul C.    |           21 |
| Schmidt, Herman    |           20 |
| Iwano, Masahiro    |           26 |
| Smith, Paul        |           21 |
| Onstad, Richard    |           19 |
| Zugnoni, Arthur A. |           21 |
| Choy, Wanda        |           23 |
| Wallace, Maggie J. |           19 |
| Bailey, Chas M.    |           19 |
| Bono, Sonny        |           24 |
| Schwarz, Jason B.  |           15 |
+--------------------+--------------+
25 rows in set (0.00 sec)
*/
/**********************************************************************************/
/*
Question 6: List all employees who have a last name ending with “son”.
*/

SELECT name 
FROM jbemployee 
WHERE name LIKE '%son,%';

/*
+---------------+
| name          |
+---------------+
| Thompson, Bob |
+---------------+
1 row in set (0.01 sec)
*/
/**********************************************************************************/
/*
Question 7: Which items (note items, not parts) have been delivered by a supplier
called Fisher-Price? Formulate this query by using a subquery in the
WHERE clause.
*/

SELECT name 
FROM jbitem 
WHERE supplier = 
(SELECT id 
FROM jbsupplier 
WHERE name = 'Fisher-Price');

/*
+-----------------+
| name            |
+-----------------+
| Maze            |
| The 'Feel' Book |
| Squeeze Ball    |
+-----------------+
3 rows in set (0.01 sec)
*/
/**********************************************************************************/
/*
Question 8: Formulate the same query as above, but without a subquery
*/

SELECT I.name, S.name 
FROM jbitem AS I, jbsupplier AS S 
WHERE (I.supplier = S.id) AND (S.name = 'Fisher-Price');

/*
+-----------------+--------------+
| name            | name         |
+-----------------+--------------+
| Maze            | Fisher-Price |
| The 'Feel' Book | Fisher-Price |
| Squeeze Ball    | Fisher-Price |
+-----------------+--------------+
3 rows in set (0.00 sec)
*/

/**********************************************************************************/
/*
Question 9: List all cities that have suppliers located in them.
Formulate this query using a subquery in the WHERE clause.
*/

SELECT name 
FROM jbcity 
WHERE id IN (SELECT city FROM jbsupplier);

/*
+----------------+
| name           |
+----------------+
| Amherst        |
| Boston         |
| New York       |
| White Plains   |
| Hickville      |
| Atlanta        |
| Madison        |
| Paxton         |
| Dallas         |
| Denver         |
| Salt Lake City |
| Los Angeles    |
| San Diego      |
| San Francisco  |
| Seattle        |
+----------------+
15 rows in set (0.00 sec)
*/
/**********************************************************************************/
/*
Question 10: What is the name and the color of the parts that are heavier than a card
reader? Formulate this query using a subquery in the WHERE clause.
(The query must not contain the weight of the card reader as a constant;
instead, the weight has to be retrieved within the query.)
*/

SELECT name, color 
FROM jbparts 
WHERE weight > 
(SELECT weight 
FROM jbparts 
WHERE name = 'card reader');

/*
+--------------+--------+
| name         | color  |
+--------------+--------+
| disk drive   | black  |
| tape drive   | black  |
| line printer | yellow |
| card punch   | gray   |
+--------------+--------+
4 rows in set (0.00 sec)
*/
/**********************************************************************************/
 /*
 Question 11:Formulate the same query as above, but without a subquery. Again, the
query must not contain the weight of the card reader as a constant.
 */

SELECT Table_1.name, Table_1.color 
FROM jbparts AS Table_1, jbparts AS Table_2 
WHERE (Table_2.name = 'card reader') AND (Table_1.weight > Table_2.weight);
 /*
 +--------------+--------+
| name         | color  |
+--------------+--------+
| disk drive   | black  |
| tape drive   | black  |
| line printer | yellow |
| card punch   | gray   |
+--------------+--------+
4 rows in set (0.00 sec)
 */
/**********************************************************************************/
/*
Question 12: What is the average weight of all black parts?
*/

SELECT AVG(weight) AS avergae_weight 
FROM jbparts 
WHERE color = 'black';

 /*
+----------------+
| avergae_weight |
+----------------+
|       347.2500 |
+----------------+
1 row in set (0.00 sec)
*/
/**********************************************************************************/
/*
Question 13: For every supplier in Massachusetts (“Mass”), retrieve the name and the
total weight of all parts that the supplier has delivered? Do not forget to
take the quantity of delivered parts into account. Note that one row
should be returned for each supplier.
*/
SELECT supplier_part.name, SUM(jbparts.weight*supplier_part.quan) AS total_weight_delivered 
FROM jbparts 
INNER JOIN
(SELECT jbsupply.supplier, supplier_in_mass.name, jbsupply.part, jbsupply.quan 
FROM
(SELECT jbsupplier.id, jbsupplier.name 
FROM jbsupplier 
INNER JOIN jbcity 
ON jbsupplier.city=jbcity.id 
WHERE jbcity.state ='Mass') AS supplier_in_mass INNER JOIN jbsupply 
ON supplier_in_mass.id = jbsupply.supplier) 
AS supplier_part ON jbparts.id = supplier_part.part
GROUP BY name;

/*
+--------------+------------------------+
| name         | total_weight_delivered |
+--------------+------------------------+
| DEC          |                   3120 |
| Fisher-Price |                1135000 |
+--------------+------------------------+
2 rows in set (0,00 sec)
*/

/**********************************************************************************/
/*
Question 14: Create a new relation with the same attributes as the jbitems relation by
using the CREATE TABLE command where you define every attribute
explicitly (i.e., not as a copy of another table). Then, populate this new
relation with all items that cost less than the average price for all items.
Remember to define the primary key and foreign keys in your table!
*/

CREATE TABLE jbitem_2_q14 ( id int, name varchar(20), dept int NOT NULL, price int, qoh int unsigned, supplier int NOT NULL,
CONSTRAINT 
pk_id PRIMARY KEY(id),
CONSTRAINT fk_supplier FOREIGN KEY (supplier) REFERENCES jbsupplier(id),
CONSTRAINT fk_dept FOREIGN KEY (dept) REFERENCES jbdept(id));

/*
Query OK, 0 rows affected, 1 warning (0.02 sec)
*/

INSERT INTO jbitem_2_q14
(SELECT * 
FROM jbitem 
WHERE price < 
(SELECT AVG(price) 
FROM jbitem));
/*
Query OK, 14 rows affected (0.02 sec)
Records: 14  Duplicates: 0  Warnings: 0
*/

SELECT * 
FROM jbitem_2_q14;
/*
+-----+-----------------+------+-------+------+----------+
| id  | name            | dept | price | qoh  | supplier |
+-----+-----------------+------+-------+------+----------+
|  11 | Wash Cloth      |    1 |    75 |  575 |      213 |
|  19 | Bellbottoms     |   43 |   450 |  600 |       33 |
|  21 | ABC Blocks      |    1 |   198 |  405 |      125 |
|  23 | 1 lb Box        |   10 |   215 |  100 |       42 |
|  25 | 2 lb Box, Mix   |   10 |   450 |   75 |       42 |
|  26 | Earrings        |   14 |  1000 |   20 |      199 |
|  43 | Maze            |   49 |   325 |  200 |       89 |
| 106 | Clock Book      |   49 |   198 |  150 |      125 |
| 107 | The 'Feel' Book |   35 |   225 |  225 |       89 |
| 118 | Towels, Bath    |   26 |   250 | 1000 |      213 |
| 119 | Squeeze Ball    |   49 |   250 |  400 |       89 |
| 120 | Twin Sheet      |   26 |   800 |  750 |      213 |
| 165 | Jean            |   65 |   825 |  500 |       33 |
| 258 | Shirt           |   58 |   650 | 1200 |       33 |
+-----+-----------------+------+-------+------+----------+
14 rows in set (0.00 sec)
*/
DROP TABLE jbitem_2_q14;

/**********************************************************************************/
 /*
Question 15: Create a view that contains the items that cost less than the average
price for items.
*/

CREATE VIEW jbitem_view_q15 AS 
SELECT * FROM jbitem 
WHERE price < 
(SELECT AVG(price) 
FROM jbitem);

/*Query OK, 0 rows affected (0.00 sec)*/

SELECT * 
FROM jbitem_view_q15;

/*
+-----+-----------------+------+-------+------+----------+
| id  | name            | dept | price | qoh  | supplier |
+-----+-----------------+------+-------+------+----------+
|  11 | Wash Cloth      |    1 |    75 |  575 |      213 |
|  19 | Bellbottoms     |   43 |   450 |  600 |       33 |
|  21 | ABC Blocks      |    1 |   198 |  405 |      125 |
|  23 | 1 lb Box        |   10 |   215 |  100 |       42 |
|  25 | 2 lb Box, Mix   |   10 |   450 |   75 |       42 |
|  26 | Earrings        |   14 |  1000 |   20 |      199 |
|  43 | Maze            |   49 |   325 |  200 |       89 |
| 106 | Clock Book      |   49 |   198 |  150 |      125 |
| 107 | The 'Feel' Book |   35 |   225 |  225 |       89 |
| 118 | Towels, Bath    |   26 |   250 | 1000 |      213 |
| 119 | Squeeze Ball    |   49 |   250 |  400 |       89 |
| 120 | Twin Sheet      |   26 |   800 |  750 |      213 |
| 165 | Jean            |   65 |   825 |  500 |       33 |
| 258 | Shirt           |   58 |   650 | 1200 |       33 |
+-----+-----------------+------+-------+------+----------+
14 rows in set (0.00 sec)
*/
DROP VIEW jbitem_view_q15;

/**********************************************************************************/
/*
Question 16: What is the difference between a table and a view? One is static and the
other is dynamic. Which is which and what do we mean by static
respectively dynamic?
Answer: A table is static, which means that when a table is created, the data in the table remains unchanged until 
someone explicitly changes the table data, for example, by inserting or updating records.
On the other hand, a view is dynamic, meaning its data changes in real-time based on the underlying table(s), 
which implies that any changes in the source table immediately affect the view's data.
*/
/**********************************************************************************/
/*
Question 17: Create a view that calculates the total cost of each debit, by considering
price and quantity of each bought item. (To be used for charging
customer accounts). The view should contain the sale identifier (debit)
and the total cost. In the query that defines the view, capture the join
condition in the WHERE clause (i.e., do not capture the join in the
FROM clause by using keywords inner join, right join or left join).
*/
 
CREATE VIEW debit_view_q17 AS 
SELECT jbsale.debit, SUM(quantity*price) AS total_cost 
FROM jbsale, jbitem 
WHERE jbsale.item = jbitem.id 
GROUP BY debit;

SELECT * 
FROM debit_view_q17;

/*
+--------+------------+
| debit  | total_cost |
+--------+------------+
| 100581 |       2050 |
| 100582 |       1000 |
| 100586 |      13446 |
| 100592 |        650 |
| 100593 |        430 |
| 100594 |       3295 |
+--------+------------+
6 rows in set (0.00 sec)
*/

DROP VIEW debit_view_q17;
/**********************************************************************************/
/*
Question 18: Do the same as in the previous point, but now capture the join conditions
in the FROM clause by using only left, right or inner joins. Hence, the
WHERE clause must not contain any join condition in this case. Motivate
why you use type of join you do (left, right or inner), and why this is the
correct one (in contrast to the other types of joins).
*/
CREATE VIEW debit_view_join_q18 AS 
SELECT debit, SUM(jbsale.quantity*jbitem.price) AS total_cost
FROM jbsale INNER JOIN jbdebit ON jbsale.debit = jbdebit.id INNER JOIN jbitem ON jbsale.item = jbitem.id 
GROUP BY debit;

/*
Query OK, 0 rows affected (0.00 sec)
*/

SELECT * FROM debit_view_join_q18;

/*
+--------+------------+
| debit  | total_cost |
+--------+------------+
| 100581 |       2050 |
| 100582 |       1000 |
| 100586 |      13446 |
| 100592 |        650 |
| 100593 |        430 |
| 100594 |       3295 |
+--------+------------+
6 rows in set (0.00 sec)

Why INNER JOIN?
In this case, an inner join is the best option because we only need matching records between tables, 
and an inner join ensures that only those rows are included in the result and filtering out irrelevant rows from `jbsale`, `jbitem`, and ` jbbit`. 
*/
DROP VIEW debit_view_join_q18;
/**********************************************************************************/
/*
Question 19:
a) Remove all suppliers in Los Angeles from the jbsupplier table. This
will not work right away. Instead, you will receive an error with error
code 23000 which you will have to solve by deleting some other
LINKÖPING UNIVERSITY
DEPT. OF COMPUTER AND INFORMATION SCIENCE (IDA)
DIVISION FOR DATABASE AND INFORMATION TECHNIQUES (ADIT)
3(10)
related tuples. However, do not delete more tuples from other tables
than necessary, and do not change the structure of the tables (i.e.,
do not remove foreign keys). Also, you are only allowed to use “Los
Angeles” as a constant in your queries, not “199” or “900”.
*/

DELETE FROM jbsupply 
WHERE jbsupply.supplier = 
(SELECT jbsupplier.id AS supplier_LA_ID 
FROM jbcity INNER JOIN jbsupplier 
ON (jbsupplier.city = jbcity.id AND jbcity.name = 'Los Angeles'));

/*
Query OK, 0 rows affected (0.00 sec)
*/

DELETE FROM jbsale 
WHERE jbsale.item IN 
(SELECT jbitem.id 
FROM jbitem 
WHERE jbitem.supplier = 
(SELECT jbsupplier.id AS supplier_LA_ID 
FROM jbcity INNER JOIN jbsupplier 
ON (jbsupplier.city = jbcity.id AND jbcity.name ='Los Angeles')));
/*
Query OK, 1 row affected (0.00 sec)
*/

DELETE FROM jbitem 
WHERE jbitem.supplier = 
(SELECT jbsupplier.id AS supplier_LA_ID 
FROM jbcity INNER JOIN jbsupplier 
ON (jbsupplier.city = jbcity.id AND jbcity.name = 'Los Angeles'));

DELETE FROM jbsupplier 
WHERE id = 
(SELECT jbsupplier.id AS supplier_LA_ID 
FROM jbcity INNER JOIN jbsupplier 
ON (jbsupplier.city = jbcity.id AND jbcity.name = 'Los Angeles'));
/*
Query OK, 2 rows affected (0.00 sec)
*/


/*
Question 19:
b) The reason we need to remove some rows in other tables is that some of these tables have foreign keys that referes to the 
row we want to delete. The foreign key constraint says that for each foreign key, there should be a value in the table it referes to.
So in order to delete the supplier from Los Angeles we need to first delete all the rows in other tables that through some relation 
refere to this supplier in jbsupplier table. The steps are as follow!


Filter out the supplier id who lives from LA:
SELECT jbsupplier.id AS supplier_LA_ID FROM jbcity INNER JOIN jbsupplier ON (jbsupplier.city = jbcity.id AND jbcity.name = 'Los Angeles');

step1: Delete all rows in jbsupply who may have a supplier from LA:
DELETE FROM jbsupply 
WHERE jbsupply.supplier = (SELECT jbsupplier.id AS supplier_LA_ID 
                           FROM jbcity INNER JOIN jbsupplier ON (jbsupplier.city = jbcity.id AND jbcity.name = 'Los Angeles'));

Filter out the item IDs which are delivered by a supplier from LA:
SELECT jbitem.id 
FROM jbitem 
WHERE jbitem.supplier = (SELECT jbsupplier.id AS supplier_LA_ID 
                         FROM jbcity INNER JOIN jbsupplier 
                         ON (jbsupplier.city = jbcity.id AND jbcity.name = 'Los Angeles'));

step2: Delete all the rows in jbsale that have a part that is delivered by a supplier in LA:
DELETE FROM jbsale 
WHERE jbsale.item IN (SELECT jbitem.id 
                      FROM jbitem 
                      WHERE jbitem.supplier = (SELECT jbsupplier.id AS supplier_LA_ID 
                                               FROM jbcity INNER JOIN jbsupplier 
                                               ON (jbsupplier.city = jbcity.id AND jbcity.name ='Los Angeles')));

step3: Delete all the items in jbitem that have a supplier in LA:
DELETE FROM jbitem 
WHERE jbitem.supplier = (SELECT jbsupplier.id AS supplier_LA_ID FROM jbcity INNER JOIN jbsupplier 
                         ON (jbsupplier.city = jbcity.id AND jbcity.name = 'Los Angeles'));

step4: Delete the supplier from LA:
DELETE FROM jbsupplier 
WHERE id = (SELECT jbsupplier.id AS supplier_LA_ID 
            FROM jbcity INNER JOIN jbsupplier 
            ON (jbsupplier.city = jbcity.id AND jbcity.name = 'Los Angeles'));
*/
/**********************************************************************************/
/*
Question 20:
*/

CREATE VIEW jbsale_supply(supplier, item, quantity) AS
SELECT suppliers.sName, suppliers.iName, jbsale.quantity 
FROM 
(SELECT jbsupplier.name AS sName, jbitem.name AS iName, jbitem.id 
FROM jbsupplier, jbitem 
WHERE jbsupplier.id = jbitem.supplier) 
AS suppliers 
LEFT JOIN jbsale ON suppliers.id = jbsale.item;

SELECT * FROM jbsale_supply;
/*
+--------------+-----------------+----------+
| supplier     | item            | quantity |
+--------------+-----------------+----------+
| Cannon       | Wash Cloth      |     NULL |
| Levi-Strauss | Bellbottoms     |     NULL |
| Playskool    | ABC Blocks      |     NULL |
| Whitman's    | 1 lb Box        |        2 |
| Whitman's    | 2 lb Box, Mix   |     NULL |
| Fisher-Price | Maze            |     NULL |
| White Stag   | Jacket          |        1 |
| White Stag   | Slacks          |     NULL |
| Playskool    | Clock Book      |        2 |
| Fisher-Price | The 'Feel' Book |     NULL |
| Cannon       | Towels, Bath    |        5 |
| Fisher-Price | Squeeze Ball    |     NULL |
| Cannon       | Twin Sheet      |        1 |
| Cannon       | Queen Sheet     |     NULL |
| White Stag   | Ski Jumpsuit    |        3 |
| Levi-Strauss | Jean            |     NULL |
| Levi-Strauss | Shirt           |        1 |
| Levi-Strauss | Boy's Jean Suit |     NULL |
+--------------+-----------------+----------+
18 rows in set (0.01 sec)
*/

SELECT supplier, sum(quantity) AS sum
FROM jbsale_supply 
GROUP BY supplier;

/*
+--------------+------+
| supplier     | sum  |
+--------------+------+
| Cannon       |    6 |
| Fisher-Price | NULL |
| Levi-Strauss |    1 |
| Playskool    |    2 |
| White Stag   |    4 |
| Whitman's    |    2 |
+--------------+------+
6 rows in set (0.00 sec)
*/

DROP VIEW jbsale_supply;