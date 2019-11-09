CREATE TABLE "LastUpdate" (
  `Id` NUMERIC NOT NULL,
  `LastUpdate` TEXT NOT NULL,
  PRIMARY KEY(`Id`)
); CREATE TABLE "PVParameters" (
  `Hour` INTEGER NOT NULL,
  `Temperature` INTEGER,
  `SolarIrradiance` INTEGER,
  `LastMeasure` TEXT,
  `Latitude` INTEGER,
  PRIMARY KEY(`Hour`)
); CREATE TABLE "WindParameters" (
  `Hour` INTEGER NOT NULL,
  `Temperature` INTEGER,
  `Humidity` INTEGER,
  `WindSpeed` INTEGER,
  `Pressure` INTEGER,
  PRIMARY KEY(`Hour`)
);