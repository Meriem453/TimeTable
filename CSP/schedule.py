from constraint import *
from constraint import Problem, AllDifferentConstraint


def create_schedule():
    days_per_group = 5
    slots_per_day = 5
    num_groups = 6
    # Courses with '_L' for lecture and '_TD' for TD
    courses = ['AI', 'Archi', 'Reseaux', 'Sec', 'MF', 'RO', 'ANUM' , 'ENT']
    lecture_courses = [course + '_L' for course in courses]
    td_courses = [course + '_TD' for course in courses]
    free_values = ['FREE1', 'FREE2', 'FREE3', 'FREE4', 'FREE5', 'FREE6', 'FREE7', 'FREE8', 'FREE9']
    all_courses = free_values + lecture_courses  + td_courses

    # Create a problem instance
    problem = Problem()

    # Define variables
    for group in range(num_groups):
        for day in range(days_per_group):
            for slot in range(slots_per_day):
                problem.addVariable((group, day, slot), all_courses)

    # Constraint: The last two slots of the third day should be FREE
    problem.addConstraint(lambda c: c == 'FREE1', ((0, 2, 3),))
    problem.addConstraint(lambda c: c == 'FREE2', ((0, 2, 4),))
    problem.addConstraint(lambda c: c == 'FREE3', ((1, 2, 3),))
    problem.addConstraint(lambda c: c == 'FREE4', ((1, 2, 4),))
    problem.addConstraint(lambda c: c == 'FREE5', ((2, 2, 3),))
    problem.addConstraint(lambda c: c == 'FREE6', ((2, 2, 4),))
    
    # Constraint: No two groups have the same course in the same slot
    for day in range(days_per_group):
        for slot in range(slots_per_day):
           problem.addConstraint(AllDifferentConstraint(), [(group, day, slot) for group in range(num_groups)])

    # Constraint: No two slots have the same course in the same group
    for group in range(num_groups):
        group_constraints = [(group, day, slot) for slot in range(slots_per_day) for day in range(days_per_group)]
        problem.addConstraint(AllDifferentConstraint(), group_constraints)

    # Constraint: No more than three successive slots of work per day
    def max_three_successive_work_slots(*slots):
        count = 0
        for slot in slots:
            if not slot.startswith('FREE'):
                count += 1
                if count > 3:
                    return False
            else:
                count = 0
        return True

    for group in range(num_groups):
        for day in range(days_per_group):
            variables = [(group, day, slot) for slot in range(slots_per_day)]
            problem.addConstraint(max_three_successive_work_slots, variables)

    solution = problem.getSolution()
    return solution


def print_schedule(schedule):
    # print(schedule)
    if schedule:
        for group in range(6):
            print(f"Group {group}:")
            for day in range(5):
                print(f"  Day {day}:")
                for slot in range(5):
                    print(f"    Slot {slot}: {schedule[(group, day, slot)]}")
    else:
        print("No solution found.")


# Create and print the schedule
schedule = create_schedule()
print_schedule(schedule)
