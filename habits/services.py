def create_message(habit):
    """Creates reminder message for habit creator"""
    message = f'Не забудь выполнить привычку "{habit.action}" в {habit.time}'
    if habit.linked_habit or habit.reward:
        message += f', а в качестве награды: {habit.linked_habit.action or habit.reward}'
    return message
