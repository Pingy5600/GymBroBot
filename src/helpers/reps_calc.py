def calculate_1rm_table(one_rep_max):
    """
    Calculates weight and reps based on 1RM percentages.

    Args:
        one_rep_max (float): The user's one-rep max weight.

    Returns:
        list of dict: A list of rows containing percentage, weight, and reps.
    """
    percentages = [
        (100, 1),
        (95, 2),
        (90, 4),
        (85, 6),
        (80, 8),
        (75, 10),
        (70, 12),
        (65, 16),
        (60, 20),
        (55, 24),
        (50, 30),
    ]
    
    table = []
    for percentage, reps in percentages:
        weight = round(one_rep_max * (percentage / 100), 1)  # Round to 1 decimal place
        table.append({
            "percentage": f"{percentage}%",
            "weight": f"{weight} kg",
            "reps": reps,
        })
    return table
