import sys


def fetch( filename ):
    # Save a reference to the original standard output
    original_stdout = sys.stdout
    with open( filename, 'w' ) as a_file:
        # Change the standard output to the file we created.
        sys.stdout = a_file
        print("key,content")
        print("01,\"Three generations with six decades of life experience.\"")
        print("02,\"He looked behind the door and didn't like what he saw.\"")
        print("03,\"The pigs were insulted that they were named hamburgers.\"")
        print("04,\"Not all people who wander are lost.\"")
        print("05,\"It is grossly unfair to suggest that the school was responsible for the accident.\"")
        print("06,\"Two generations with six days of life experience.\"")
        print("07,\"She looked in front the door and knew shat she saw.\"")
        print("08,\"The cat were insulted that they were named burritos.\"")
        print("09,\"all people who wander are lost.\"")
        print("10,\"It is grossly unfair to tell, that the school was responsible for the kids lunch.\"")
        print("11,\"3 generations with 6 decades of life experience.\"")
        print("12,\"He looked behind the car and didn't like what he wanted.\"")
        print("13,\"The horses were insulted that they were named Maple.\"")
        print("14,\"Not all humans who wander are lost.\"")
        print("15,\"It is grossly fair to suggest that the school was responsible for kids success.\"")
        print("16,\"10000 generations with 15 decades of life experience.\"")
        print("17,\"They looked behind the door and didn't like what they saw.\"")
        print("18,\"The man was insulted that he was named hamburgers.\"")
        print("19,\"Not all animals who wander are found.\"")
        print("20,\"It is cool to suggest that the hospital was responsible for the accident.\"")
        # Reset the standard output to its original value
        sys.stdout = original_stdout
