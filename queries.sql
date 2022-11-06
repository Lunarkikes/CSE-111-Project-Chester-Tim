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
    VALUES ('Tire Change','2022-07-13','JT3MU52N953RRH1PA','1','1','','13','50','1','70'),
           ('Tire Change','2022-07-13','WBADM6343XHEL29DB','1','1','','15','50','1','70');


--Dealership sells car to a new customer
INSERT INTO Customer(c_name, c_phone) 
    VALUES ('Ron White', '4085551291');

INSERT INTO Sales(s_date,s_VIN,s_spID,s_cID,s_MSRP,s_totalCost)
    VALUES ('2022-07-15','5FNYF18617RT8GPDT','6',(SELECT c_ID FROM Customer WHERE c_name = 'Ron White'),
                                                 (SELECT v_MSRP FROM Vehicle WHERE v_VIN = '5FNYF18617RT8GPDT'),'28413.83');

UPDATE Vehicle
SET v_status = 'SOLD'
WHERE v_VIN = '5FNYF18617RT8GPDT';