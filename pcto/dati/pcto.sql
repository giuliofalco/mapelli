BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS aziende (
        id              int PRIMARY KEY,
	partita_iva	text UNIQUE,
	ragione_sociale	text NOT NULL,
	tutor_referente_azienda	text ,
	sede_comune	text,
	sede_provincia	text,
	telefono	text,
	email	        text NOT NULL,
	settore	        text	
);
CREATE TABLE IF NOT EXISTS abbinamento (
        id int PRIMARY KEY,     
	partita_iva     text,
	email_studente  text,
	anno_scolastico	text,
	recensione	text NOT NULL,
	UNIQUE(partita_iva,email_studente,anno_scolastico)
);
CREATE TABLE IF NOT EXISTS studenti (
        id   int PRIMARY KEY,
	email_studente text,
	nome	text NOT NULL,
	cognome	text NOT NULL,
	UNIQUE(email_studente)
);
CREATE TABLE IF NOT EXISTS tutor_studente (
	email_tutor text,
	email_studente text	,
	anno_scolastico	text,
	PRIMARY KEY(email_tutor,email_studente,anno_scolastico)
);
CREATE TABLE IF NOT EXISTS contatti (
        id int PRIMARY KEY,
	partita_iva text,
	email_tutor text,
	anno_scolastico text DEFAULT 2021,
	note text,
	disponibilita text,
	periodo_inizio date,
	periodo_fine date,
	UNIQUE(partita_iva,email_tutor,anno_scolastico)
);
CREATE TABLE IF NOT EXISTS convenzioni (
	azienda	,
	data_stipula date NOT NULL,
	PRIMARY KEY(azienda)
);
CREATE TABLE IF NOT EXISTS tutor (
        id int PRIMARY KEY,
	email	TEXT NOT NULL UNIQUE,
	nome	TEXT NOT NULL,
	cognome	TEXT NOT NULL,
	password TEXT,
	UNIQUE(email)
);
COMMIT;
