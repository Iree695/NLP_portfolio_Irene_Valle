
def demo_local_stt():
    ...

def demo_local_tts():
    ...

def demo_external_stt():
    ...

def demo_external_tts():
    ...

def demo_extra_speech_task():
    ...

def main():
    while True:
        print("1. Local STT")
        print("2. Local TTS")
        print("3. External STT")
        print("4. External TTS")
        print("5. Extra Speech Task")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            demo_local_stt()
        elif choice == '2':
            demo_local_tts()
        elif choice == '3':
            demo_external_stt()
        elif choice == '4':
            demo_external_tts()
        elif choice == '5':
            demo_extra_speech_task()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

