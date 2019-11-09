BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `DeviceModules` (
	`Id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	'Building'	NUMERIC,
	`DemandSide`	NUMERIC,
	'DeviceName'	INTEGER,
	`EST(h)`	INTEGER,
	'LET(h)'	INTEGER,
	'LOT(h)'	INTEGER,
	'Power(kW)'	INTEGER,
	'StartTime(h)'	INTEGER,
	'EndTime(h)'	INTEGER,
	'DeviceStatus'	TEXT,
	'Power_total(kW)'	TEXT,
	'Power_sum(kW)'	TEXT,
	FOREIGN KEY(`DemandSide`) REFERENCES `DemandSide`(`Id`),
	FOREIGN KEY(`Building`) REFERENCES `Building`(`Id`)
);
CREATE TABLE IF NOT EXISTS `DemandSide` (
	`Id`	INTEGER NOT NULL,
	`Description`	TEXT,
	PRIMARY KEY(`Id`)
);

CREATE TABLE IF NOT EXISTS `LastUpdate` (
	`Id`	INTEGER,
	`LastUpdate`	TEXT,
	PRIMARY KEY(`Id`)
);
CREATE TABLE IF NOT EXISTS 'Building' (
	`Id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`DemandSide`	INTEGER,
	'BuildingName'	TEXT,
	'CED_Count'	INTEGER,
	'CED_List'	TEXT,
	'CEDConsumption'	TEXT,
	'UDConsumption'	TEXT,
	'TotalDemand'	TEXT,
	FOREIGN KEY(`DemandSide`) REFERENCES `DemandSide`(`Id`)
);
COMMIT;