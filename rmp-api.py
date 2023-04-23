import ratemyprofessor


def get_professor_rating(professor_name):
    # professor_name should be a string containing the full name of the professor
    school = ratemyprofessor.get_school_by_name("The University of Texas at Dallas")
    professor = ratemyprofessor.get_professor_by_school_and_name(school, professor_name)
    return professor

    """
    if professor is not None:
        print(
            "%s works in the %s Department of %s."
            % (professor.name, professor.department, professor.school.name)
        )
        print("Rating: %s / 5.0" % professor.rating)
        print("Difficulty: %s / 5.0" % professor.difficulty)
        print("Total Ratings: %s" % professor.num_ratings)
        if professor.would_take_again is not None:
            print(("Would Take Again: %s" % round(professor.would_take_again, 1)) + "%")
        else:
            print("Would Take Again: N/A")
    """


"""
prof = get_professor_rating("Nhut Nguyen")
print(prof.difficulty)
"""
