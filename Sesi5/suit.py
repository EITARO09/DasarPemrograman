import random

def play_game():
    player_score = 0
    computer_score = 0
    choices = ["batu", "gunting", "kertas"]

    while True:
        player_choice = input("Pilih batu, gunting, atau kertas (atau ketik 'keluar' untuk mengakhiri): ").lower()

        if player_choice == 'keluar':
            print("Terima kasih sudah bermain!")
            break

        if player_choice not in choices:
            print("Input tidak valid. Silakan pilih antara batu, gunting, atau kertas.")
            continue

        computer_choice = random.choice(choices)
        print(f"Komputer memilih: {computer_choice}")

        if player_choice == computer_choice:
            print("Hasil: Seri")
        elif player_choice == "batu":
            if computer_choice == "gunting":
                print("Pemain Menang")
                player_score += 1
            else:
                print("Komputer Menang")
                computer_score += 1
        elif player_choice == "gunting":
            if computer_choice == "kertas":
                print("Pemain Menang")
                player_score += 1
            else:
                print("Komputer Menang")
                computer_score += 1
        elif player_choice == "kertas":
            if computer_choice == "batu":
                print("Pemain Menang")
                player_score += 1
            else:
                print("Komputer Menang")
                computer_score += 1

        print(f"Skor - Pemain: {player_score} | Komputer: {computer_score}")

        play_again = input("Apakah Anda ingin melanjutkan permainan? (ya/tidak): ").lower()
        if play_again != 'ya':
            print("Terima kasih sudah bermain!")
            break

play_game()
