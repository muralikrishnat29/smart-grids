BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `WindModules` (
	`Id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`Status`	INTEGER,
	`SupplySide`	NUMERIC,
	`Ra`	INTEGER,
	`Location`	INTEGER,
	`CurrentEnergy`	INTEGER,
	`ForecastEnergy`	TEXT,
	FOREIGN KEY(`SupplySide`) REFERENCES `SupplySide`(`Id`)
);
CREATE TABLE IF NOT EXISTS `SupplySide` (
	`Id`	INTEGER NOT NULL,
	`Description`	TEXT,
	PRIMARY KEY(`Id`)
);
CREATE TABLE IF NOT EXISTS `PVModules` (
	`Id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`Status`	INTEGER,
	`SupplySide`	NUMERIC,
	`Area`	INTEGER,
	`EMax`	INTEGER,
	`AngleOfModule`	TEXT,
	`Location`	INTEGER,
	`CurrentEnergy`	INTEGER,
	`ForecastEnergy`	TEXT,
	FOREIGN KEY(`SupplySide`) REFERENCES `SupplySide`(`Id`)
);
CREATE TABLE IF NOT EXISTS `LastUpdate` (
	`Id`	INTEGER,
	`LastUpdate`	TEXT,
	PRIMARY KEY(`Id`)
);
CREATE TABLE IF NOT EXISTS `Battery` (
	`Id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`Status`	INTEGER,
	`SupplySide`	NUMERIC,
	`State`	TEXT,
	`Efficiency`	INTEGER,
	`TimeInterval`	INTEGER,
	`InitialEnergy`	INTEGER,
	`SelfDischargeRate`	INTEGER,
	`Charge`	INTEGER,
	`ChargeSpecs`	INTEGER,
	`DischargeSpecs`	INTEGER,
	`EnergySpecs`	INTEGER,
	FOREIGN KEY(`SupplySide`) REFERENCES `SupplySide`(`Id`)
);
CREATE TABLE IF NOT EXISTS `History` (
	`Hour`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`WindEnergy`	INTEGER,
	`SolarEnergy`	INTEGER,
	`TotalEnergy`	INTEGER
);
COMMIT;
