import re
from collections import deque, defaultdict
from constraint import Problem, AllDifferentConstraint


def create_schedule():
    days_per_group = 5
    slots_per_day = 5
    num_groups = 3
    # Courses with '_Cour' for lecture and '_TD' for TD
    courses = ['AI,Dr Lekehali', 'DA/CI,Dr Djennadi', 'Reseaux,Dr Zenadji', 'Security,Dr Djebari',
               'Méthodes formelles,Dr Zedek', 'Recherche operationel,Dr Isaadi', 'Analyse numérique,Dr Alkama']
    lecture_courses = [course + '_Cour' for course in courses]
    td_courses = [course + '_TD' for course in courses]
    tp_courses = ['AI_TP,Pr Abbas,', 'Reseaux_TP,Pr Zaidi']
    free_values = ['FREE1', 'FREE2', 'FREE3', 'FREE4', 'FREE5', 'FREE6', 'FREE7', 'FREE8']
    all_courses =  td_courses + free_values + tp_courses + lecture_courses + ['Entreprenariat,Pr Kaci_Cour']

    # Create a problem instance
    problem = Problem()

    # Define variables
    for group in range(num_groups):
        for day in range(days_per_group):
            for slot in range(slots_per_day):
                var = (group, day, slot)
                problem.addVariable(var, all_courses)

    # Constraint: The last two slots of the third day should be FREE
    problem.addConstraint(lambda c: c == 'FREE1', ((0, 2, 3),))
    problem.addConstraint(lambda c: c == 'FREE2', ((0, 2, 4),))
    problem.addConstraint(lambda c: c == 'FREE3', ((1, 2, 3),))
    problem.addConstraint(lambda c: c == 'FREE4', ((1, 2, 4),))
    problem.addConstraint(lambda c: c == 'FREE5', ((2, 2, 3),))
    problem.addConstraint(lambda c: c == 'FREE6', ((2, 2, 4),))

    # Custom constraint function to ensure all TD courses are different in the same slot
    def td_all_different_constraint(*args):
        td_courses_in_slot = [val for val in args if '_TD' in val]
        return len(td_courses_in_slot) == len(set(td_courses_in_slot))

    # Custom constraint function to ensure all groups have the same Lecture in the same slot
    def lecture_same_constraint(*args):
        lectures_in_slot = [val for val in args if '_L' in val]
        return len(set(lectures_in_slot)) <= 1

    # Applying constraints for each day and slot
    for day in range(days_per_group):
        for slot in range(slots_per_day):
            vars_in_slot = [(group, day, slot) for group in range(num_groups)]
            # Apply the lecture same constraint
            problem.addConstraint(lecture_same_constraint, vars_in_slot)
            # Apply the TD all different constraint
            problem.addConstraint(td_all_different_constraint, vars_in_slot)

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
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
    if not schedule:
        print("No solution found.")
        return

    column_width = max(len(course) for course in schedule.values()) + 2
    group_count = len(set(group for group, _, _ in schedule.keys()))

    print("Schedule:")
    for group in range(group_count):
        print(f"\nGroup {group + 1}:")
        for day_index, day in enumerate(days):
            print(f"  {day}:")
            for slot in range(5):
                course = schedule.get((group, day_index, slot), 'FREE')
                print(f"    {slot + 1:<5}{'FREE' if course.startswith('FREE') else course:^{column_width}}")

    # Extract and count the number of days each teacher works
    teacher_days = defaultdict(set)
    teacher_pattern = re.compile(r'(Pr|Dr)\s+([A-Za-z]+)_')

    for (group, day, slot), course in schedule.items():
        match = teacher_pattern.search(course)
        if match:
            teacher = match.group(2)
            teacher_days[teacher].add(day)

    # Count the number of teachers who work less than 3 days
    teachers_less_than_3_days = [teacher for teacher, days in teacher_days.items() if len(days) <=2]

    print(f"\nNumber of teachers who work less than 3 days per week: {len(teachers_less_than_3_days)}")
    print("Teachers:", ", ".join(teachers_less_than_3_days))


# Create and print the schedule
schedule = create_schedule()
print_schedule(schedule)
