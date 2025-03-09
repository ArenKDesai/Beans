import beans

def main():

    # Main Beans processing loop
    while True:

        # Command Prompt input
        user_input = input("beans> ")
        if not user_input:
            continue

        # Tell Beans to think about it
        beans.process_user_input(user_input=user_input)

if __name__ == '__main__':
    main()