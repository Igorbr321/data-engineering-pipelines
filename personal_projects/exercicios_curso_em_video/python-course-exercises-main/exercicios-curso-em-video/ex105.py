def grades(*n, sit=False):
    """
    Calculates statistics of grades and optionally provides a situation message.

    Args:
        *n: Variable number of grade values.
        sit (bool, optional): If True, includes a situation message based on the average grade. Defaults to False.

    Returns:
        dict: A dictionary containing the total number of grades, the highest grade, the lowest grade,
              the average grade, and optionally, the situation message.

    Example:
        resp = grades(5, 9, sit=True)
        print(resp)
    """
    from statistics import mean

    # Initialize dictionary to store information
    info = dict()

    # Calculate statistics
    info['total'] = len(n)  # Total number of grades
    info['highest'] = max(n)  # Highest grade
    info['lowest'] = min(n)  # Lowest grade
    info['average'] = mean(n)  # Average grade

    # Determine situation message if 'sit' parameter is True
    if sit:
        average_grade = info['average']
        if average_grade >= 9:
            info['situation'] = 'Excellent!'
        elif average_grade >= 7:
            info['situation'] = 'Good!'
        elif average_grade >= 5:
            info['situation'] = 'Fair.'
        else:
            info['situation'] = 'Fail.'

    return info

# Example of usage
result = grades(5, 9, sit=True)
print(result)
