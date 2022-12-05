import sqlite3
import os

# list of queries to be executed by the database class constructor (creates tables)
init_queries = [
	'''CREATE TABLE Staff (
			staffNo INTEGER PRIMARY KEY, 
			fName VARCHAR(255) NOT NULL, 
			lName VARCHAR(255) NOT NULL, 
			street VARCHAR(255), 
			city VARCHAR(255), 
			telephoneNo VARCHAR(15),
			DOB VARCHAR(10) NOT NULL, 
			position VARCHAR(255), 
			salary INT, 
			clinicNo INT, 
			FOREIGN KEY (clinicNo) REFERENCES Clinic(clinicNo) ON UPDATE CASCADE ON DELETE SET NULL,
			FOREIGN KEY (city) REFERENCES Zip(city) ON UPDATE CASCADE ON DELETE SET NULL,
			UNIQUE (fName, lName)				
		);''',
	
		'''CREATE TABLE Examination (
			examNo INTEGER PRIMARY KEY, 
			complaint LONGTEXT,
			description LONGTEXT,
			dateExamined VARCHAR(10),
			actions LONGTEXT,
			staffNo INT,
			petNo INT,
			FOREIGN KEY (staffNo) REFERENCES Staff(staffNo) ON UPDATE CASCADE ON DELETE SET NULL,
			FOREIGN KEY (petNo) REFERENCES Pet(petNo) ON UPDATE CASCADE ON DELETE SET NULL
		);''',

		'''CREATE TABLE Clinic (
			clinicNo INTEGER PRIMARY KEY, 
			name VARCHAR(255),
			FOREIGN KEY (name) REFERENCES ClinicLocation(name) ON UPDATE CASCADE ON DELETE CASCADE
		);''',

		'''CREATE TABLE ClinicLocation (
			name VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
			street VARCHAR(255), 
			city VARCHAR(255), 
			telephoneNo VARCHAR(15),
			FOREIGN KEY (city) REFERENCES Zip(city) ON UPDATE CASCADE ON DELETE SET NULL
		);''',

		'''CREATE TABLE Pet (
			petNo INTEGER PRIMARY KEY, 
			fName VARCHAR(255) NOT NULL, 
			lName VARCHAR(255) NOT NULL, 
			DOB VARCHAR(10) NOT NULL, 
			species VARCHAR(255),
			breed VARCHAR(255),
			color VARCHAR(255),
			clinicNo INT,
			ownerNo INT,
			FOREIGN KEY (clinicNo) REFERENCES Clinic(clinicNo) ON UPDATE CASCADE ON DELETE SET NULL,
			FOREIGN KEY (ownerNo) REFERENCES Owner(ownerNo) ON UPDATE CASCADE ON DELETE CASCADE,
			UNIQUE (fName, lName)				
		);''',

		'''CREATE TABLE Owner (
			ownerNo INTEGER PRIMARY KEY, 
			fName VARCHAR(255) NOT NULL, 
			lName VARCHAR(255) NOT NULL, 
			street VARCHAR(255), 
			city VARCHAR(255), 
			telephoneNo VARCHAR(15),
			FOREIGN KEY (city) REFERENCES Zip(city) ON UPDATE CASCADE ON DELETE SET NULL,
			UNIQUE (fName, lName)				
		);''',

		'''CREATE TABLE Zip (
			city VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY, 
			zip VARCHAR(10)
		);'''
]

class database:
	#constructor: create sqlite3 database and exec the init_queries
	def __init__(this, name):
		if os.path.exists(name): os.remove(name)
		this.connect = sqlite3.connect(name)
		this.cursor = this.connect.cursor()
		this.exec(init_queries)

	#execute a list of queries and call print_results
	def exec(this, list):
		for i in enumerate(list): 
			this.cursor.execute(i[1])
			this.print_results()

	#print query results if there are any
	def print_results(this):
		res = this.cursor.fetchall()
		if res: print(res, '\n')

	#destructor: commit changes and close connection
	def __del__(this):
		this.connect.commit()
		this.connect.close()

def main():
	# instantiate database object (constructor will initalize it with init_queries)
	db = database('pawsome_pets.db')

	# get all tables to make sure init_queries succeeded
	db.exec(['''SELECT name FROM sqlite_master WHERE type = 'table';'''])

	# list of queries for inserting 5 rows of sample data into each table
	sample_data_queries = [
		'''INSERT INTO Staff (fName, lName, street, city, telephoneNo, DOB, position, salary, clinicNo) VALUES ('John', 'Smith', 'Chestnut Ave', 'Birmingham', '124-994-2293', '02-15-1985', 'Secretary', 55000, 1)''',
		'''INSERT INTO Staff (fName, lName, street, city, telephoneNo, DOB, position, salary, clinicNo) VALUES ('Ashley', 'Graham', 'Fawn St', 'Westport', '305-724-6923', '02-16-2001', 'Veterinarian', 85000, 2)''',
		'''INSERT INTO Staff (fName, lName, street, city, telephoneNo, DOB, position, salary, clinicNo) VALUES ('Leon', 'Kennedy', 'Rose Blv', 'Fall River', '101-444-8792', '10-01-1990', 'Janitor', 30000, 1)''',
		'''INSERT INTO Staff (fName, lName, street, city, telephoneNo, DOB, position, salary, clinicNo) VALUES ('Patricia', 'Hoxforn', 'Highland Ave', 'Dartmouth', '774-231-4012', '07-12-1998', 'Veterinary Technician', 68000, 4)''',
		'''INSERT INTO Staff (fName, lName, street, city, telephoneNo, DOB, position, salary, clinicNo) VALUES ('Alexander', 'Rutherford', 'Waning Crescant Dr', 'Cambridge', '808-156-6832', '05-19-1993', 'Marketing Specialist', 70000, 3)''',

		'''INSERT INTO Examination (complaint, description, dateExamined, actions, staffNo, petNo) VALUES ('Broken leg', 'Canine Max fractured leg while running', '08-15-2022', 'Fitted with doggie cast', 5, 1)''',
		'''INSERT INTO Examination (complaint, description, dateExamined, actions, staffNo, petNo) VALUES ('Scratched cornea', 'Feline Moonpie was scratched in the eye by his brother while playing', '10-27-2022', 'Prescribed eye drops', 4, 2)''',
		'''INSERT INTO Examination (complaint, description, dateExamined, actions, staffNo, petNo) VALUES ('Ear mites', 'Rabbit Lily has severe ear mite infestation', '12-01-2022', 'Prescribed antibiotics', 3, 3)''',
		'''INSERT INTO Examination (complaint, description, dateExamined, actions, staffNo, petNo) VALUES ('Kennel Cough', 'Canine Hershey contracted Kennel Cough after going to daycare without getting vaccinated first', '04-13-2022', 'Told to rest, get vaccinated, and stay away from daycare for now', 2, 4)''',
		'''INSERT INTO Examination (complaint, description, dateExamined, actions, staffNo, petNo) VALUES ('Broken wing', 'Bird Chip broke wing while flying indoors', '09-05-2022', 'Fitted with wing cast', 1, 5)''',

		'''INSERT INTO Clinic (name) VALUES ('Birmingham Pawsome Pets')''',
		'''INSERT INTO Clinic (name) VALUES ('Westport Pawsome Pets')''',
		'''INSERT INTO Clinic (name) VALUES ('Fall River Pawsome Pets')''',
		'''INSERT INTO Clinic (name) VALUES ('Dartmouth Pawsome Pets')''',
		'''INSERT INTO Clinic (name) VALUES ('Cambridge Pawsome Pets')''',

		'''INSERT INTO ClinicLocation (name, street, city, telephoneNo) VALUES ('Birmingham Pawsome Pets', 'Picnic St', 'Birmingham', '705-724-4552')''',
		'''INSERT INTO ClinicLocation (name, street, city, telephoneNo) VALUES ('Westport Pawsome Pets', 'Auburn Dr', 'Westport', '902-611-0951')''',
		'''INSERT INTO ClinicLocation (name, street, city, telephoneNo) VALUES ('Fall River Pawsome Pets', 'Jeffrey St', 'Fall River', '508-911-6933')''',
		'''INSERT INTO ClinicLocation (name, street, city, telephoneNo) VALUES ('Dartmouth Pawsome Pets', 'Palace Ave', 'Dartmouth', '774-811-1329')''',
		'''INSERT INTO ClinicLocation (name, street, city, telephoneNo) VALUES ('Cambridge Pawsome Pets', 'West Rodney St', 'Cambridge', '202-113-0009')''',

		'''INSERT INTO Pet (fName, lName, DOB, species, breed, color, clinicNo, ownerNo) VALUES ('Max', 'Rogers', '04-24-2019', 'canine', 'German Shepherd', 'brown', 3, 2)''',
		'''INSERT INTO Pet (fName, lName, DOB, species, breed, color, clinicNo, ownerNo) VALUES ('Moonpie', 'Pimentel', '05-31-2021', 'feline', 'Domestic Shorthair', 'black/white', 5, 1)''',
		'''INSERT INTO Pet (fName, lName, DOB, species, breed, color, clinicNo, ownerNo) VALUES ('Lily', 'Blanche', '02-13-2022', 'rabbit', 'New Zealand White', 'white', 4, 1)''',
		'''INSERT INTO Pet (fName, lName, DOB, species, breed, color, clinicNo, ownerNo) VALUES ('Hershey', 'Perry', '11-04-2018', 'canine', 'Labrador Retriever', 'brown', 1, 3)''',
		'''INSERT INTO Pet (fName, lName, DOB, species, breed, color, clinicNo, ownerNo) VALUES ('Chip', 'Ehrmantraut', '07-21-2017', 'bird', 'Parakeet', 'green/yellow', 3, 2)''',

		'''INSERT INTO Owner (fName, lName, street, city, telephoneNo) VALUES ('Jamie', 'Rogers', 'Rockland Ave', 'Birmingham', '643-102-5992')''',
		'''INSERT INTO Owner (fName, lName, street, city, telephoneNo) VALUES ('Jackson', 'Pimentel', 'Pickle Dr', 'Westport', '508-291-3312')''',
		'''INSERT INTO Owner (fName, lName, street, city, telephoneNo) VALUES ('Irene', 'Blanche', 'Peanut St', 'Fall River', '330-500-2235')''',
		'''INSERT INTO Owner (fName, lName, street, city, telephoneNo) VALUES ('Cherry', 'Perry', 'Mallory St', 'Dartmouth', '808-104-4492')''',
		'''INSERT INTO Owner (fName, lName, street, city, telephoneNo) VALUES ('Monica', 'Ehrmantraut', 'Leaf Rd', 'Cambridge', '774-001-0192')''',

		'''INSERT INTO Zip (city, zip) VALUES ('Birmingham', 61021)''',
		'''INSERT INTO Zip (city, zip) VALUES ('Westport', 02790)''',
		'''INSERT INTO Zip (city, zip) VALUES ('Fall River', 99526)''',
		'''INSERT INTO Zip (city, zip) VALUES ('Dartmouth', 83321)''',
		'''INSERT INTO Zip (city, zip) VALUES ('Cambridge', 10923)'''
	]

	print('\n')
	db.exec(sample_data_queries)

	# print out the contents of each table to verify the INSERT queries worked
	print_queries = [
		'''SELECT * FROM Staff''',
		'''SELECT * FROM Examination''',
		'''SELECT * FROM Clinic''',
		'''SELECT * FROM ClinicLocation''',
		'''SELECT * FROM Pet''',
		'''SELECT * FROM Owner''',
		'''SELECT * FROM Zip'''
	]

	db.exec(print_queries)

	example_queries = [

		'''SELECT * FROM Examination WHERE petNo = 
		       (SELECT petNo FROM Pet WHERE fName = 'Moonpie' AND lName = 'Pimentel')''',

		'''SELECT * FROM Examination WHERE petNo IN 
		       (SELECT petNo FROM Pet WHERE ownerNo = 
		           (SELECT ownerNo FROM Owner WHERE fname = 'Jamie' AND lName = 'Rogers'))''',

		'''SELECT AVG(salary) FROM Staff WHERE staffNo IN 
		       (SELECT staffNo FROM Staff WHERE clinicNo IN 
		           (SELECT clinicNo FROM Clinic WHERE name IN 
		               (SELECT name FROM ClinicLocation WHERE city = 'Birmingham')))''',

		'''SELECT COUNT(*) FROM Pet WHERE clinicNo IN
		       (SELECT clinicNo FROM Clinic WHERE name IN
		            (SELECT name FROM ClinicLocation WHERE city = 'Fall River'))''',

		'''SELECT complaint FROM Examination WHERE petNo IN
		       (SELECT petNo FROM Pet WHERE species = 'canine')''',

		'''SELECT complaint FROM Examination WHERE petNo IN
		       (SELECT petNo FROM Pet WHERE species = 'canine') AND (complaint LIKE '%Broke%' OR complaint LIKE '%broke%') '''

	]

	print('\n')
	db.exec(example_queries)

if __name__ == "__main__":
	main()