CREATE TABLE CSVImport
(
    url VARCHAR(255) NOT NULL,
    topic VARCHAR(255) NOT NULL
);
LOAD DATA INFILE 'D:\Study\Python\CrawlData\_8_German_Retete\germany\data_url.csv' 
