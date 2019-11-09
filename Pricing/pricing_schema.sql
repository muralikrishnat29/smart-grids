CREATE TABLE IF NOT EXISTS `tomorrow`(
    `hour` INTEGER PRIMARY KEY, 
    `price` FLOAT
);
CREATE TABLE IF NOT EXISTS `today`(
    `hour` INTEGER PRIMARY KEY, 
    `price` FLOAT
);
CREATE TABLE IF NOT EXISTS `LastUpdate` (
	`Id`	INTEGER,
	`LastUpdateTodayPrice`	TEXT,
    `LastUpdateTomorrowPrice`	TEXT,
	PRIMARY KEY(`Id`)
);