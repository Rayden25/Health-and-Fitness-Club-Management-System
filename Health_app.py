import psycopg2
from psycopg2.extras import DictCursor
import datetime

# Establish a connection to the database
conn = psycopg2.connect("dbname=postgres user=postgres password=Udubra124")

# Create a cursor with the connection and set it as a dictionary cursor
cur = conn.cursor(cursor_factory=DictCursor)


# Member Functions
def register_member(member_name):
    # Collect additional information for registration
    password = input("Create a password: ")
    email = input("Enter your email: ")
    fitness_goal = input("Enter your fitness goal: ")
    health_metrics = input("Enter your health metrics: ")

    # Insert new member into Members table
    cur.execute("INSERT INTO Members (Name, Password, Email, FitnessGoal, HealthMetrics) VALUES (%s, %s, %s, %s, %s) RETURNING MemberID",
                (member_name, password, email, fitness_goal, health_metrics))
    member_id = cur.fetchone()[0]  # Get the ID of the newly inserted member

    # Collect initial exercise routines
    exercise_routines = []
    while True:
        add_routine = input("Do you want to add an exercise routine? (yes/no): ")
        if add_routine.lower() != 'yes':
            break
        name = input("Enter exercise name: ")
        repetitions = int(input("Enter number of repetitions: "))
        sets = int(input("Enter number of sets: "))
        date = input("Enter date performed (YYYY-MM-DD): ")
        exercise_routines.append({'name': name, 'repetitions': repetitions, 'sets': sets, 'date': date})

    # Insert initial exercise routines in ExerciseRoutines table
    for routine in exercise_routines:
        sql = f"INSERT INTO ExerciseRoutines (MemberID, ExerciseName, Repetitions, Sets, DatePerformed) VALUES ({member_id}, '{routine['name']}', {routine['repetitions']}, {routine['sets']}, '{routine['date']}')"
        cur.execute(sql)

    # Collect initial fitness achievements
    fitness_achievements = []
    while True:
        add_achievement = input("Do you want to add a fitness achievement? (yes/no): ")
        if add_achievement.lower() != 'yes':
            break
        name = input("Enter achievement name: ")
        date = input("Enter achievement date (YYYY-MM-DD): ")
        fitness_achievements.append({'name': name, 'date': date})

    # Insert initial fitness achievements in FitnessAchievements table
    for achievement in fitness_achievements:
        sql = f"INSERT INTO FitnessAchievements (MemberID, AchievementName, AchievementDate) VALUES ({member_id}, '{achievement['name']}', '{achievement['date']}')"
        cur.execute(sql)

    # Collect initial health statistics
    health_statistics = []
    while True:
        add_statistic = input("Do you want to add a health statistic? (yes/no): ")
        if add_statistic.lower() != 'yes':
            break
        weight = float(input("Enter weight: "))
        body_fat_percentage = float(input("Enter body fat percentage: "))
        date = input("Enter date recorded (YYYY-MM-DD): ")
        health_statistics.append({'weight': weight, 'body_fat_percentage': body_fat_percentage, 'date': date})

    # Insert initial health statistics in HealthStatistics table
    for statistic in health_statistics:
        sql = f"INSERT INTO HealthStatistics (MemberID, Weight, BodyFatPercentage, DateRecorded) VALUES ({member_id}, {statistic['weight']}, {statistic['body_fat_percentage']}, '{statistic['date']}')"
        cur.execute(sql)

    conn.commit()
    print("Registration successful! Welcome to the Health and Fitness Club.")

def update_member_profile(member_id):
    print("What would you like to update?")
    print("1. Personal Information")
    print("2. Fitness Goals")
    print("3. Health Metrics")
    print("4. Exercise Routines")
    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        name = input("Enter new name: ")
        email = input("Enter new email: ")
        password = input("Enter new password: ")
        sql = f"UPDATE Members SET Name='{name}', Email='{email}', Password='{password}' WHERE MemberID={member_id}"
        cur.execute(sql)

    elif choice == '2':
        fitness_goal = input("Enter new fitness goal: ")
        sql = f"UPDATE Members SET FitnessGoal='{fitness_goal}' WHERE MemberID={member_id}"
        cur.execute(sql)

    elif choice == '3':
        health_metrics = input("Enter new health metrics: ")
        sql = f"UPDATE Members SET HealthMetrics='{health_metrics}' WHERE MemberID={member_id}"
        cur.execute(sql)

    elif choice == '4':
        exercise_routines = input("Enter new exercise routines: ")
        # Assuming exercise_routines is a list of dictionaries
        for routine in exercise_routines:
            sql = f"UPDATE ExerciseRoutines SET ExerciseName='{routine['name']}', Repetitions={routine['repetitions']}, Sets={routine['sets']}, DatePerformed='{routine['date']}' WHERE RoutineID={routine['id']} AND MemberID={member_id}"
            cur.execute(sql)

    else:
        print("Invalid choice. Please enter a number between 1 and 4.")

    conn.commit()

def display_dashboard(member_id):
    # Fetch exercise routines from ExerciseRoutines table
    sql = f"SELECT * FROM ExerciseRoutines WHERE MemberID={member_id}"
    cur.execute(sql)
    exercise_routines = cur.fetchall()

    print("Exercise Routines:")
    for routine in exercise_routines:
        print(f"Exercise Name: {routine['exercisename']}, Repetitions: {routine['repetitions']}, Sets: {routine['sets']}, Date Performed: {routine['dateperformed']}")

    # Fetch fitness achievements from FitnessAchievements table
    sql = f"SELECT * FROM FitnessAchievements WHERE MemberID={member_id}"
    cur.execute(sql)
    fitness_achievements = cur.fetchall()

    print("\nFitness Achievements:")
    for achievement in fitness_achievements:
        print(f"Achievement Name: {achievement['achievementname']}, Achievement Date: {achievement['achievementdate']}")

    # Fetch health statistics from HealthStatistics table
    sql = f"SELECT * FROM HealthStatistics WHERE MemberID={member_id}"
    cur.execute(sql)
    health_statistics = cur.fetchall()

    print("\nHealth Statistics:")
    for statistic in health_statistics:
        print(f"Weight: {statistic['weight']}, Body Fat Percentage: {statistic['bodyfatpercentage']}, Date Recorded: {statistic['daterecorded']}")

def schedule_session():
    # Collect session details
    member_id = int(input("Enter your member ID: "))
    trainer_id = int(input("Enter the trainer ID: "))
    session_type = input("Enter session type (Personal Training/Group Fitness): ")
    # Validate date
    while True:
        session_date = input("Enter session date (YYYY-MM-DD): ")
        try:
            session_date = datetime.datetime.strptime(session_date, '%Y-%m-%d').date()
            if session_date < datetime.date.today():
                print("The session date cannot be in the past. Please enter a future date.")
            else:
                break
        except ValueError:
            print("Invalid date format. Please enter the date in 'YYYY-MM-DD' format.")

    # Validate time
    while True:
        session_time = input("Enter session time (HH:MM:SS): ")
        try:
            session_time = datetime.datetime.strptime(session_time, '%H:%M:%S').time()
            break
        except ValueError:
            print("Invalid time format. Please enter the time in 'HH:MM:SS' format.")

    # Ask the user if they want to use equipment
    use_equipment = input("Do you want to use equipment? (yes/no): ")

    # Determine membership fee
    if use_equipment.lower() == 'yes':
        membership_fee = 75
        equipment_name = input("Enter the name of the equipment you want to use: ")
    else:
        membership_fee = 50
        equipment_name = None

    # Show the membership fee to the user
    print(f"The membership fee is: ${membership_fee}")

    # Ask the user if they want to pay the membership fee
    pay_fee = input("Would you like to pay the membership fee now? (yes/no): ")
    if pay_fee.lower() == 'yes':
        while True:
            try:
                payment_amount = float(input("Please enter the amount you want to pay: "))
                if payment_amount < membership_fee:
                    print("The amount entered is less than the membership fee. Please enter an amount equal to or greater than the membership fee.")
                else:
                    break
            except ValueError:
                print("Invalid amount. Please enter a valid number.")
        # Process membership fee payment
        payment_status = process_membership_fee(member_id, payment_amount)
        if not payment_status:
            print("Payment was not successful. Please try again.")
            return
    else:
        print("Please pay the membership fee as soon as possible.")
        return

    # Check if the trainer is available
    sql = f"SELECT * FROM TrainerAvailability WHERE TrainerID={trainer_id} AND AvailableDate='{session_date}' AND AvailableTimeStart <= '{session_time}' AND AvailableTimeEnd >= '{session_time}'"
    cur.execute(sql)
    if cur.fetchone() is None:
        print("The trainer is not available at the specified date and time.")
        return

    # Check if the equipment is available
    if equipment_name:
        sql = f"SELECT * FROM Equipment WHERE EquipmentName='{equipment_name}' AND MaintenanceStatus=FALSE"
        cur.execute(sql)
        if cur.fetchone() is None:
            print("The equipment is not available.")
            return

    # Schedule the session
    sql = f"INSERT INTO Schedule (MemberID, TrainerID, SessionType, SessionDate, SessionTime) VALUES ({member_id}, {trainer_id}, '{session_type}', '{session_date}', '{session_time}')"
    cur.execute(sql)
    conn.commit()
    print("The session has been scheduled successfully.")


# Trainer Functions
def set_trainer_availability():
    # Collect trainer's availability details
    trainer_id = int(input("Enter your trainer ID: "))
    available_date = input("Enter the date you are available (YYYY-MM-DD): ")
    available_time_start = input("Enter the start time of your availability (HH:MM:SS): ")
    available_time_end = input("Enter the end time of your availability (HH:MM:SS): ")

    # Check if the trainer exists in the trainers table
    cur.execute(f"SELECT * FROM trainers WHERE TrainerID = {trainer_id}")
    trainer_exists = cur.fetchone()

    if trainer_exists is None:
        print("The trainer ID you entered does not exist. Please enter a valid trainer ID.")
    else:
        # Insert the trainer's availability into the TrainerAvailability table
        sql = f"INSERT INTO TrainerAvailability (TrainerID, AvailableDate, AvailableTimeStart, AvailableTimeEnd) VALUES ({trainer_id}, '{available_date}', '{available_time_start}', '{available_time_end}')"
        cur.execute(sql)
        conn.commit()
        print("Your availability has been set successfully.")


def view_member_profile(member_name):
    # Search for the member in Members table
    sql = f"SELECT * FROM Members WHERE Name='{member_name}'"
    cur.execute(sql)
    member = cur.fetchone()

    if member:
        print("Member Profile:")
        print(f"Name: {member['name']}")
        print(f"Email: {member['email']}")
        print(f"Fitness Goal: {member['fitnessgoal']}")
        print(f"Health Metrics: {member['healthmetrics']}")
    else:
        print("No member found with that name.")


# Administrative Staff Functions
def book_room(room_id, trainer_id, booking_date, booking_time_start, booking_time_end):
    # Check if the trainer is available
    sql = f"SELECT * FROM TrainerAvailability WHERE TrainerID={trainer_id} AND AvailableDate='{booking_date}' AND AvailableTimeStart <= '{booking_time_start}' AND AvailableTimeEnd >= '{booking_time_end}'"
    cur.execute(sql)
    if cur.fetchone() is None:
        print("The trainer is not available at the specified date and time.")
        return

    # Check if the room is available
    sql = f"SELECT * FROM RoomBookings WHERE RoomID={room_id} AND BookingDate='{booking_date}' AND ((BookingTimeStart <= '{booking_time_start}' AND BookingTimeEnd > '{booking_time_start}') OR (BookingTimeStart < '{booking_time_end}' AND BookingTimeEnd >= '{booking_time_end}'))"
    cur.execute(sql)
    if cur.fetchone() is not None:
        print("The room is not available at the specified date and time.")
        return

    # Book the room
    sql = f"INSERT INTO RoomBookings (RoomID, TrainerID, BookingDate, BookingTimeStart, BookingTimeEnd) VALUES ({room_id}, {trainer_id}, '{booking_date}', '{booking_time_start}', '{booking_time_end}')"
    cur.execute(sql)
    conn.commit()
    print("The room has been booked successfully.")

def user_book_room():
    # Collect room booking details
    room_id = int(input("Enter room ID: "))
    trainer_id = int(input("Enter trainer ID: "))
    booking_date = input("Enter booking date (YYYY-MM-DD): ")
    booking_time_start = input("Enter booking start time (HH:MM:SS): ")
    booking_time_end = input("Enter booking end time (HH:MM:SS): ")

    # Call the book_room function
    book_room(room_id, trainer_id, booking_date, booking_time_start, booking_time_end)


def monitor_equipment():
    # Ask the admin for the name of the equipment
    equipment_name = input("Enter the name of the equipment: ")

    # Query the database for the equipment's maintenance status
    sql = f"SELECT MaintenanceStatus FROM Equipment WHERE EquipmentName='{equipment_name}'"
    cur.execute(sql)
    result = cur.fetchone()

    if result is None:
        print("The equipment does not exist.")
    else:
        maintenance_status = result[0]
        if maintenance_status:
            print(f"The {equipment_name} is currently under maintenance.")
        else:
            print(f"The {equipment_name} is available for use.")


def update_class_schedule():
    # Ask the admin for the class details
    class_id = int(input("Enter the class ID: "))
    trainer_id = int(input("Enter the trainer ID: "))
    new_date = input("Enter the new class date (YYYY-MM-DD): ")
    new_time = input("Enter the new class time (HH:MM:SS): ")
    new_timestamp = f"{new_date} {new_time}"

    # Check if the class exists in the database
    sql = f"SELECT * FROM Classes WHERE ClassID={class_id}"
    cur.execute(sql)
    result = cur.fetchone()

    if result is None:
        # If the class doesn't exist, create a new class
        sql = f"INSERT INTO Classes (ClassID, TrainerID, ClassTime) VALUES ({class_id}, {trainer_id}, '{new_timestamp}')"
        print("The class has been created successfully.")
    else:
        # If the class exists, update the class schedule
        sql = f"UPDATE Classes SET TrainerID={trainer_id}, ClassTime='{new_timestamp}' WHERE ClassID={class_id}"
        print("The class schedule has been updated successfully.")

    cur.execute(sql)
    conn.commit()

def process_membership_fee(member_id, amount):
    # Insert payment record into Payments table
    cur.execute("INSERT INTO Payments (MemberID, Amount, PaymentStatus) VALUES (%s, %s, %s)",
                (member_id, amount, 'Paid'))
    print("Membership fee payment processed successfully.")
    return True


# Main Interface Function
def main_interface():
    while True:
        print("Welcome to the Health and Fitness Club Management System!")
        print("Please select your role:")
        print("1. Member")
        print("2. Trainer")
        print("3. Admin")
        print("4. Quit")
        role = input("Enter your role (1/2/3/4): ")

        if role == '1':
            authenticate_member()
        elif role == '2':
            trainer_name = input("Enter your trainer name: ")
            authenticate_trainer(trainer_name)
        elif role == '3':
            admin_id = int(input("Enter your admin ID: "))
            authenticate_admin(admin_id)
        elif role == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid role selected. Please try again.")

# Authentication Functions
def authenticate_member():
    # Check if the member exists in the database
    member_name = input("Enter your member name: ")
    cur.execute("SELECT * FROM Members WHERE Name = %s", (member_name,))
    member = cur.fetchone()
    if member:
        password_attempt = input("Enter your password: ")
        if password_attempt == member['password']:
            print(f"Welcome, {member_name}!")
            member_interface(member_name)  # Pass member ID to member interface
        else:
            print("Incorrect password.")
    else:
        print("Member not found.")
        register_option = input("Would you like to register as a new member? (yes/no): ")
        if register_option.lower() == 'yes':
            register_member(member_name)
        else:
            print("Thank you for visiting.")

def authenticate_trainer(trainer_name):
    # Check if the trainer exists in the database
    cur.execute(f"SELECT * FROM Trainers WHERE Name = %s", (trainer_name,))
    trainer = cur.fetchone()
    if trainer:
        trainer_interface(trainer_name)  # Pass trainer name to trainer interface
    else:
        print("Trainer not found. Please try again.")

def authenticate_admin(admin_id):
    # Check if the admin exists in the database
    cur.execute(f"SELECT * FROM Admins WHERE AdminID = %s", (admin_id,))
    admin = cur.fetchone()
    if admin:
        admin_interface(admin_id)  # No need to pass admin ID to admin interface
    else:
        print("Admin not found. Please try again.")

# Member Interface Function
def member_interface(member_name):
    while True:
        print(f"\nWelcome, {member_name}!")
        print("\nMember Interface:")
        print("1. Update member profile")
        print("2. Display member dashboard")
        print("3. Schedule Session")
        print("4. Quit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            member_id = int(input("Enter your member ID: "))
            update_member_profile(member_id)
        elif choice == '2':
            member_id = int(input("Enter your member ID: "))
            display_dashboard(member_id)
        elif choice == '3':
            schedule_session()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Trainer Interface Function
def trainer_interface(trainer_name):
    print(f"Welcome, {trainer_name}!")
    while True:
        print("\nTrainer Interface:")
        print("1. Set availability")
        print("2. View member profile")
        print("3. Quit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            set_trainer_availability()
        elif choice == '2':
            member_name = input("Enter the name of the member: ")
            view_member_profile(member_name)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Admin Interface Function
def admin_interface(admin_id):
    while True:
        print(f"\nWelcome, Admin {admin_id}!")
        print("\nAdmin Interface:")
        print("1. Book room")
        print("2. Monitor equipment")
        print("3. Update class schedule")
        print("4. Quit")
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            user_book_room()
        elif choice == '2':
            monitor_equipment()
        elif choice == '3':
            update_class_schedule()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Call the main interface function
main_interface()


# Call the function
# Close the cursor and the connection
cur.close()
conn.close()
