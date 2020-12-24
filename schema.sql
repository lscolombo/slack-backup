CREATE TABLE user (
	name TEXT, 
	real_name TEXT, 
	display_name TEXT, 
	slack_id TEXT, 
	PRIMARY KEY (slack_id)
);


CREATE TABLE channel (
	slack_id TEXT, 
	name TEXT, 
	PRIMARY KEY (slack_id)
);

CREATE TABLE message_direct (
	slack_id TEXT, 
	text TEXT, 
	user_id TEXT, 
	ts TEXT, 
	PRIMARY KEY (slack_id)
);
