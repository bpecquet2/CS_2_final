def vote_menu():
    print('v: Vote')
    print('x: Exit')
    user_input = input('Option: ').strip()  # make input var
    # create loop for option
    while True:  # loops until a return statement
        if user_input == 'v' or user_input == 'V':
            return 'v'
        elif user_input == 'x' or user_input == 'X':
            return 'x'
        else:
            user_input = input('Invalid (v/x): ').strip()


def candidate_menu():
    # create loop for option
    print('1: Jane')
    print('2: John')
    user_input = input('Candidate: ').strip()  # make input var
    while True:  # loops until a return statement
        if user_input == '1':
            print('Voted Jane')
            return 1
        elif user_input == '2':
            print('Voted John')
            return 2
        else:
            user_input = input('Invalid (1/2): ').strip()



def main():
    # set variables for vote count
    john_votes = 0
    jane_votes = 0

    while True:
        choice = vote_menu()
        if choice == 'x':  # break the loop with x for exit
            total_votes = f'John-{john_votes}, Jane-{jane_votes}, Total-{john_votes + jane_votes}'
            print(total_votes)
            break
        elif choice == 'v':  # add to vote vars if v is choice
            candidate_choice = candidate_menu()
            if candidate_choice == 1:
                jane_votes += 1
            elif candidate_choice == 2:
                john_votes += 1


main()
