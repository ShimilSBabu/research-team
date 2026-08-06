from src.prompt_factory.prompt_manager import get_prompt

def main():
    print("Hello from research-team!")
    prompt=get_prompt()
    print(f"prompt: {prompt}")


if __name__ == "__main__":
    main()
