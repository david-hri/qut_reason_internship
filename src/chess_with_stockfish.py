import os
import chess
import chess.engine

def play_against_stockfish():
    # Chemin vers l'exécutable Stockfish
    stockfish_path = r"C:\Users\dadah\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

    # Vérifiez si le fichier existe et est accessible
    if not os.path.isfile(stockfish_path):
        print(f"Le fichier Stockfish n'existe pas à l'emplacement spécifié : {stockfish_path}")
        return

    # Initialiser le moteur Stockfish
    try:
        engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    except PermissionError:
        print("Permission refusée. Essayez d'exécuter le script en tant qu'administrateur.")
        return

    # Initialiser le plateau
    board = chess.Board()

    while not board.is_game_over():
        # Afficher le plateau
        print(board)

        # Votre tour (Blancs)
        if board.turn == chess.WHITE:
            move = input("Entrez votre coup (ex: e2e4): ")
            try:
                board.push_uci(move)
            except ValueError:
                print("Coup invalide. Réessayez.")
                continue

        # Tour de Stockfish (Noirs)
        else:
            print("Stockfish réfléchit...")
            result = engine.play(board, chess.engine.Limit(time=2.0))
            board.push(result.move)
            print(f"Stockfish joue: {result.move}")

    # Afficher le résultat final
    print("Partie terminée")
    print("Résultat: ", board.result())

    # Fermer le moteur Stockfish
    engine.quit()

# Lancer le jeu
play_against_stockfish()
