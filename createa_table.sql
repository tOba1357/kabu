CREATE TABLE tblcompanies (
  id     INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  name   VARCHAR(100)           NOT NULL,
  code   VARCHAR(64)            NOT NULL,
  market VARCHAR(24)
);

CREATE TABLE tblvalues (
  id            INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  company_id    INTEGER                NOT NULL,
  start_value   DOUBLE,
  end_value     DOUBLE,
  high_value    DOUBLE,
  low_value     DOUBLE,
  volume        DOUBLE,
  trading_value DOUBLE,
  date          DATE
);

CREATE TABLE tbllearning_log (
  id         INTEGER AUTO_INCREMENT NOT NULL  PRIMARY KEY,
  company_id INTEGER                NOT NULL
);
