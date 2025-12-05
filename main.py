from backend.agent import Agent

def main():
    agent = Agent()
    response = agent.ask("What is the capital of France?")
    print(response)

if __name__ == "__main__":
    main()
