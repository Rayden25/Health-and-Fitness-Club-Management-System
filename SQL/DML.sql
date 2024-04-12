-- Inserting data into the Members table
INSERT INTO Members (Name, Email, Password, FitnessGoal, HealthMetrics) VALUES ('John Doe', 'john.doe@example.com', 'password123', 'Weight Loss', 'Normal');

-- Inserting data into the Trainers table
INSERT INTO Trainers (Name, Specialization) VALUES ('Jane Smith', 'Yoga');

-- Inserting data into the TrainerAvailability table
INSERT INTO TrainerAvailability (TrainerID, AvailableDate, AvailableTimeStart, AvailableTimeEnd) VALUES (1, '2024-04-13', '09:00:00', '17:00:00');

-- Inserting data into the Admins table
INSERT INTO Admins (Name) VALUES ('Admin1');

-- Inserting data into the RoomBookings table
INSERT INTO RoomBookings (TrainerID, AdminID, RoomID, BookingDate, BookingTimeStart, BookingTimeEnd) VALUES (1, 1, 101, '2024-04-14', '10:00:00', '12:00:00');

-- Inserting data into the Equipment table
INSERT INTO Equipment (AdminID, EquipmentName, MaintenanceStatus) VALUES (1, 'Treadmill', true);

-- Inserting data into the Schedule table
INSERT INTO Schedule (MemberID, TrainerID, SessionType, SessionDate, SessionTime) VALUES (1, 1, 'Yoga', '2024-04-15', '10:00:00');

-- Inserting data into the Classes table
INSERT INTO Classes (ClassName, TrainerID, ClassTime) VALUES ('Morning Yoga', 1, '2024-04-16 09:00:00');

-- Inserting data into the Payments table
INSERT INTO Payments (MemberID, Amount, PaymentStatus) VALUES (1, 50.00, 'Paid');

-- Inserting data into the ExerciseRoutines table
INSERT INTO ExerciseRoutines (MemberID, ExerciseName, Repetitions, Sets, DatePerformed) VALUES (1, 'Push Ups', 10, 3, '2024-04-12');

-- Inserting data into the FitnessAchievements table
INSERT INTO FitnessAchievements (MemberID, AchievementName, AchievementDate) VALUES (1, '5k Run', '2024-04-10');

-- Inserting data into the HealthStatistics table
INSERT INTO HealthStatistics (MemberID, Weight, BodyFatPercentage, DateRecorded) VALUES (1, 70.0, 20.0, '2024-04-11');
