CREATE DATABASE kjrb;
USE kjrb
CREATE TABLE kjrb(url VARCHAR(100), 
	yinti VARCHAR(100), 
	biaoti VARCHAR(100),
	futi VARCHAR(100),
	author VARCHAR(20),
	picture VARCHAR(100),
	article text,
	pageNo VARCHAR(10),
	pageName VARCHAR(50),
	primary key(url)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;