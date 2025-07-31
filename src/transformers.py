from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
import time

# Initialize LangChain with Local Mistral
llm = ChatOllama(model="mistral", temperature=0)


# Initialize LangChain LLM
#llm = ChatOpenAI(model="gpt-4", temperature=0)

class LLMArgumentationAgent:
    """An agent that uses an LLM (GPT) to generate arguments and counterarguments."""

    def __init__(self, name, role):
        self.name = name
        self.role = role  # Defines stance (e.g., "Pro AI", "Against AI")
        self.arguments = []  # Stores generated arguments
        self.counterarguments = []  # Stores generated counterarguments

    def generate_argument(self, topic):
        """Generates an argument in favor of the agent's role and stores it."""
        messages = [
            SystemMessage(content=f"You are {self.name}, an expert debater advocating for '{self.role}'."),
            HumanMessage(content=f"Generate a strong argument supporting '{self.role}' on the topic: '{topic}'. You only give the argument and nothing else except if you agree with the counter argument")
        ]
        argument = llm(messages).content.strip()
        self.arguments.append(argument)
        return argument

    def generate_counterargument(self, opponent_argument):
        """Generates a counterargument and stores it."""
        messages = [
            SystemMessage(content=f"You are {self.name}, an expert debater advocating for '{self.role}'."),
            HumanMessage(content=f"Your opponent said: '{opponent_argument}'. Provide a logical and persuasive counterargument. \
                        If you cannot refute it, respond only with 'I concede this point and nothing else..")
        ]
        counterargument = llm(messages).content.strip()
        self.counterarguments.append(counterargument)
        return counterargument


class ArgumentationProtocol:
    """Handles structured argumentation between two LLM-driven agents."""

    def __init__(self, agent1, agent2, topic):
        self.agent1 = agent1
        self.agent2 = agent2
        self.topic = topic
        self.argument_pairs = []  # Stores pairs of (argument, counterargument)

    def debate(self):
        """Conducts a structured turn-based argumentation session, storing all arguments."""
        print(f"\n🔥 Debate on: {self.topic}\n")

        # Start debate
        current_agent, opponent = self.agent1, self.agent2

        # Generate initial argument
        argument = current_agent.generate_argument(self.topic)
        print(f"{current_agent.name}: {argument}")

        while True:
            # time.sleep(1)  # Simulate thinking time

            # Opponent generates a counterargument
            counterargument = opponent.generate_counterargument(argument)

            # Store the argument-counterargument pair
            self.argument_pairs.append((argument, counterargument))

            if "I concede" in counterargument:
                print(f"{opponent.name}: I concede this point.")
                print(f"\n🏆 {current_agent.name} wins the debate!")
                break

                       # Check for repetition to avoid endless loops
            if self.detect_repetition(counterargument):
                print(f"\n⏹️ Debate Stopped: Arguments are repeating. Declaring a draw!")
                break


            print(f"{opponent.name}: {counterargument}")

            # Swap turns
            argument = counterargument
            current_agent, opponent = opponent, current_agent

    def get_all_arguments(self):
        """Returns a list of all arguments and counterarguments."""
        return self.argument_pairs

    def detect_repetition(self, new_argument):
        """Detects if the same argument has been used before."""
        return any(new_argument == arg for arg, _ in self.argument_pairs)


agent1 = LLMArgumentationAgent("Alice", "I am pro the universe is expanding")
agent2 = LLMArgumentationAgent("Bob", "The universe is shrinking")

print("Debate Starts!\n")

# Start the debate
protocol = ArgumentationProtocol(agent1, agent2, "Is the universe expanding?")
protocol.debate()

# Retrieve and print all arguments and counterarguments
all_arguments = protocol.get_all_arguments()
print("\n📜 Debate Summary:")
for i, (arg, counter) in enumerate(all_arguments):
    print(f"Round {i+1}:")
    print(f"  Argument: {arg}")
    print(f"  Counterargument: {counter}\n")
