create or replace TABLE SWIB_RND.ERIN_ESCOBAR.STUDENT (
	STUDENT_ID NUMBER(38,0) NOT NULL autoincrement start 1 increment 1 noorder,
	NAME VARCHAR(20) NOT NULL,
	MAJOR VARCHAR(20) DEFAULT 'undecided',
	primary key (STUDENT_ID)
);