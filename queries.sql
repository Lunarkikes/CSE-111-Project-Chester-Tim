--Customer wants to see what cars are for sale with a budget <$25k
SELECT *
FROM Vehicle
WHERE v_MSRP < '25000' AND v_status = 'FOR SALE';

--Customer comes in with vehicle that needs a new set of tires
INSERT INTO Customer(c_name, c_phone) 
    VALUES ('Bob Smith', '2095554893');

INSERT INTO Vehicle
    VALUES ('WBAVT735284KVXY6H','2008','BMW','M3','','Silver','','FOR REPAIR');

INSERT INTO Service(sv_serviceType,sv_date,sv_VIN,sv_partKey,sv_equipmentKey,sv_cID,sv_mID,sv_partCost,sv_partQty,sv_totalCost)
    VALUES ('Tire Change','2022-07-12','WBAVT735284KVXY6H','6','3','9','8','150','4','650');

--Dealership takes shipment of five new vehicles to sell
INSERT INTO Vehicle
    VALUES ('5FNYF284163H6Y9SC','2020','Honda' ,'CR-V'   ,'Luxury' ,'Gray'  ,'35400','FOR SALE'),
           ('WAUHA84AXVS8GXM9K','2020','Audi'  ,'TT'     ,'Base'   ,'Silver','34900','FOR SALE'),
           ('5FNTF1H34BRRTJK3Z','2020','Honda' ,'Civic'  ,'Premium','Red'   ,'29200','FOR SALE'),
           ('JT3BU17R43VWND9BU','2020','Toyota','Corolla','Base'   ,'Red'   ,'26200','FOR SALE');

--Dealership has two vehicles in inventory that need repairs (oil changes)
UPDATE Vehicle
SET v_status = 'FOR REPAIR'
WHERE v_VIN = 'JT3MU52N953RRH1PA';

UPDATE Vehicle
SET v_status = 'FOR REPAIR'
WHERE v_VIN = 'WBADM6343XHEL29DB';

INSERT INTO Service(sv_serviceType,sv_date,sv_VIN,sv_partKey,sv_equipmentKey,sv_cID,sv_mID,sv_partCost,sv_partQty,sv_totalCost)
    VALUES ('Oil Change','2022-07-13','JT3MU52N953RRH1PA','1','1','','13','50','1','70'),
           ('Oil Change','2022-07-13','WBADM6343XHEL29DB','1','1','','15','50','1','70');


--Dealership sells car to a new customer (total cost includes 8.25% tax and $2300 in fees)
INSERT INTO Customer(c_name, c_phone) 
    VALUES ('Ron White', '4085551291');

INSERT INTO Sales(s_date,s_VIN,s_spID,s_cID,s_MSRP,s_totalCost)
    VALUES ('2022-07-15','5FNYF18617RT8GPDT','6',(SELECT c_ID FROM Customer WHERE c_name = 'Ron White'),
                                                 (SELECT v_MSRP FROM Vehicle WHERE v_VIN = '5FNYF18617RT8GPDT'),
                                                 (SELECT v_MSRP FROM Vehicle WHERE v_VIN = '5FNYF18617RT8GPDT')+((SELECT v_MSRP FROM Vehicle WHERE v_VIN = '5FNYF18617RT8GPDT')*.0825)+2300);

UPDATE Vehicle
SET v_status = 'SOLD'
WHERE v_VIN = '5FNYF18617RT8GPDT';

--Dealership wants to know what car(s) have used the Tire Mount and Balance machine in July (run previous queries first)
SELECT * 
FROM Vehicle
WHERE v_VIN IN (SELECT sv_VIN
                FROM Service
                WHERE sv_equipmentKey IN (SELECT e_equipmentKey
                                            FROM Equipment
                                            WHERE e_name = 'Tire Mount and Balance')
                AND strftime('%m', sv_date) = '07');

--Mechanic fills out repair work order
UPDATE Vehicle
SET v_status = 'FOR REPAIR'
WHERE v_VIN = 'KL1TC5EE4B536UYLJ';

INSERT INTO Service(sv_serviceType,sv_date,sv_VIN,sv_partKey,sv_equipmentKey,sv_cID,sv_mID,sv_partCost,sv_partQty,sv_totalCost)
    VALUES ('Battery Replacement','2022-11-02','KL1TC5EE4B536UYLJ','4','','','7','50','1','130');

--Mechanic services car and sends it back to the dealership
UPDATE Vehicle
SET v_status = 'FOR SALE'
WHERE v_VIN = 'KL1TC1247WFBK2ZHN';

--Customer brings car in and requests service
INSERT INTO Customer(c_name, c_phone) 
    VALUES ('Jacob Lewsey', '4154985249');

INSERT INTO Service(sv_serviceType,sv_date,sv_VIN,sv_partKey,sv_equipmentKey,sv_cID,sv_mID,sv_partCost,sv_partQty,sv_totalCost)
    VALUES ('Brake Change','2021-12-15','WAUKF38E48DZ4WUTZ','3','2',(SELECT c_ID FROM Customer WHERE c_name = 'Jacob Lewsey'),'11','20','1','40');

--Customer wants to check if car is pre-owned (returns the number of times this car has been sold in the database)
SELECT count(*)
FROM Vehicle
inner join Sales on v_VIN = s_VIN;

--Customer wants to see cars for sale sorted by make and year
Select *
FROM Vehicle
where v_status = "FOR SALE"
order by v_year asc, v_make;

--Mechanic takes a car in for servicing from the dealership and doesn't need equipment or parts
UPDATE Vehicle
SET v_status = 'FOR REPAIR'
WHERE v_VIN = 'JT3BU14R93J6NZLHE';

INSERT INTO Service(sv_serviceType,sv_date,sv_VIN,sv_partKey,sv_equipmentKey,sv_cID,sv_mID,sv_partCost,sv_partQty,sv_totalCost)
    VALUES ('Alignment','2022-01-29','JT3BU14R93J6NZLHE','','','','7','','','');

UPDATE Vehicle
SET v_status = 'FOR SALE'
WHERE v_VIN = 'JT3BU14R93J6NZLHE';

--Show salespersons' info of those who have at least 1 sale.
SELECT sp_ID, sp_name, sp_position
from Sales
inner join Salesperson on s_spID = sp_ID
group by sp_ID
having count(sp_ID) > 0;

--Show mechanics that have serviced one car
SELECT m_ID, m_name, m_position
from Service
inner join Mechanic on sv_mID = m_ID
group by m_ID
having count(m_ID) = 1;

--Show car sales before/within/after a certain time
SELECT *
from Sales
where substr(s_date, 1, 10) > "2022-05-01";

--Show car services before/within/after a certain time
SELECT *
from Service
where "2022-04-15" > substr(sv_date, 1, 10) > "2022-05-02";

--Show serviced grouped by their service type
SELECT *
from Service
group by sv_serviceType;

--Show a saleperson who holds the position of "Supervisor" and has made more than 1 sale
SELECT *
from Sales
inner join Salesperson on s_spID = sp_ID
WHERE sp_position = 'Supervisor'
group by sp_ID
having count(sp_ID) > 0;

--Show customers who have bought more than 0 cars from the database
SELECT *
from Sales
inner join Customer on c_ID = s_cID
group by c_ID
having count(c_ID) > 0;

--Check if a car has been serviced and has been sold once in the database
SELECT *
from Vehicle
inner join Service on sv_VIN = v_VIN
inner join Sales on v_VIN = s_VIN;

--Show cars that require multiple services and sort by car number and service type alphabetically
select *
from Service
inner join Vehicle on v_VIN = sv_VIN
group by v_VIN, sv_serviceType
having count(v_VIN) > 1;

--Select sales from vehicles that were sold for more than their MSRP and the saleperson is a supervisor
SELECT *
from Sales
inner join Salesperson on s_spID = sp_ID
inner join Vehicle on s_VIN = v_VIN
where v_MSRP < s_totalCost and sp_ID in (SELECT sp_ID
                                        from Sales
                                        inner join Salesperson on s_spID = sp_ID
                                        WHERE sp_position = 'Supervisor');