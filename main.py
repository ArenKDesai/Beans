import beans

def main():

    # Main Beans processing loop
    while True:

        # Command Prompt input
        try:
            user_input = input("beans> ")
            if not user_input:
                continue
        except EOFError:
            beans.exit_the_stage()

        # Tell Beans to think about it
        beans.process_user_input(user_input=user_input)

if __name__ == '__main__':
    main()