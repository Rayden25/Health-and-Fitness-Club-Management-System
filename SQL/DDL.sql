-- Member table
CREATE TABLE Members (
    MemberID SERIAL PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(100),
    FitnessGoal VARCHAR(100),
    HealthMetrics VARCHAR(100)
);

-- Trainer table
CREATE TABLE Trainers (
    TrainerID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Specialization VARCHAR(255)
);

CREATE TABLE TrainerAvailability (
    AvailabilityID SERIAL PRIMARY KEY,
    TrainerID INTEGER REFERENCES Trainers(TrainerID),
    AvailableDate DATE,
    AvailableTimeStart TIME,
    AvailableTimeEnd TIME
);

-- Admin table
CREATE TABLE Admins (
    AdminID SERIAL PRIMARY KEY,
	Name VARCHAR(100)
    
);

-- Room table
CREATE TABLE RoomBookings (
    BookingID SERIAL PRIMARY KEY,
	TrainerID INTEGER REFERENCES Trainers(TrainerID),
	AdminID INTEGER REFERENCES Admins(AdminID),
    RoomID INTEGER,
    BookingDate DATE,
    BookingTimeStart TIME,
    BookingTimeEnd TIME
);


-- Equipment table
CREATE TABLE Equipment (
    EquipmentID SERIAL PRIMARY KEY,
	AdminID INTEGER REFERENCES Admins(AdminID),
	EquipmentName VARCHAR(100),
    MaintenanceStatus BOOLEAN
);

CREATE TABLE Schedule (
    SessionID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    TrainerID INT REFERENCES Trainers(TrainerID),
    SessionType VARCHAR(255),
    SessionDate DATE,
    SessionTime TIME
);

-- Class table
CREATE TABLE Classes (
    ClassID SERIAL PRIMARY KEY,
	ClassName VARCHAR(100),
    TrainerID INT REFERENCES Trainers(TrainerID),
    ClassTime TIMESTAMPTZ
);

-- Payment table
CREATE TABLE Payments (
    PaymentID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    Amount DECIMAL(10, 2),
    PaymentStatus VARCHAR(50)
);

-- Exercise Routines table
CREATE TABLE ExerciseRoutines (
    RoutineID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    ExerciseName VARCHAR(100),
    Repetitions INT,
    Sets INT,
    DatePerformed DATE
);

-- Fitness Achievements table
CREATE TABLE FitnessAchievements (
    AchievementID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    AchievementName VARCHAR(100),
    AchievementDate DATE
);

-- Health Statistics table
CREATE TABLE HealthStatistics (
    StatisticID SERIAL PRIMARY KEY,
    MemberID INT REFERENCES Members(MemberID),
    Weight DECIMAL(5, 2),
    BodyFatPercentage DECIMAL(4, 2),
    DateRecorded DATE
);

