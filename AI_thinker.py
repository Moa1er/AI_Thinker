from chatgpt_api.chatgpt import * 

def main():
    question = input("Enter your question: ")
    max_levels = int(input("Enter the maximum number of reflection levels: "))

    # Decompose the question into specialized GPTs
    decomposition_prompt = f"Decompose the following question into specialized GPTs: {question}. Answer only with the roles of the specialized GPTs separated by newlines."
    gpt_roles = ask_for_division(decomposition_prompt).split("\n")

    # Initialize the discussion with the original question
    discussion = [f"Original Question: {question}"]

    # Perform the back-and-forth discussion
    for level in range(max_levels):
        for role in gpt_roles:
            response = ask_specialized_gpt(role, discussion)
            discussion.append(f"{role}: {response}")

    # Print the final discussion
    print("\nFinal Discussion:")
    for message in discussion:
        print(message)

    # Get the final response
    final_response = ask_final_response(question, discussion)
    print(f"\nFinal Response: {final_response}")

if __name__ == "__main__":
    main()