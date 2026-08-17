def calculate_notes_withdrawal(cash):
    notes_50 = cash // 50
    cash -= notes_50 * 50  # Alternatively, you can use cash %= 50

    notes_20 = cash // 20
    cash -= notes_20 * 20  # Alternatively, you can use cash %= 20

    notes_10 = cash // 10
    cash -= notes_10 * 10  # Alternatively, you can use cash %= 10

    notes_1 = cash // 1

    return notes_50, notes_20, notes_10, notes_1


def print_notes(notes_50, notes_20, notes_10, notes_1):
    print(f"Notes of $50: {notes_50}")
    print(f"Notes of $20: {notes_20}")
    print(f"Notes of $10: {notes_10}")
    print(f"Notes of $1: {notes_1}")

