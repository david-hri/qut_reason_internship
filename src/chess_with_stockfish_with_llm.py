import os
import chess
import chess.engine
import re
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage


from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage



def get_response_from_llm(prompt,model="llama3.2"):
    # Initialiser le modèle Mistral
    llm = ChatOllama(model=model, temperature=0.7)

    # Créer un message avec le prompt
    messages = [HumanMessage(content=prompt)]

    # Obtenir la réponse du modèle
    response = llm.invoke(messages)
    response=response.content.strip()

    if model.startswith("deepseek"):
        response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

    # Retourner la réponse
    return response

def llm_vs_stockfish(level=0):
    liste_des_coups=""
    # Chemin vers l'exécutable Stockfish
    stockfish_path = r"C:\Users\dadah\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

    # Vérifiez si le fichier existe et est accessible
    if not os.path.isfile(stockfish_path):
        print(f"Le fichier Stockfish n'existe pas à l'emplacement spécifié : {stockfish_path}")
        return

    # Initialiser le moteur Stockfish
    try:
        engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        engine.configure({"Skill Level": level})
    except PermissionError:
        print("Permission refusée. Essayez d'exécuter le script en tant qu'administrateur.")
        return
    

    #Début de la partie:
    # Initialiser le plateau
    board = chess.Board()

    

    #Premier Mouvement:
    move = get_response_from_llm("Let's play chess. You are a chess Grandmaster playing against me at your best level. What is the best move to play if you are playing as white? Respond only with the move to play and nothing else (e.g., e4, d4, etc.).")

    liste_des_coups+=str(move)+", "
    uci_move = board.push_san(move)

    print("First move:", move, uci_move, "(UCI notations)")


    result = engine.play(board, chess.engine.Limit(time=0.1))
    # Convertir le coup en notation standard (SAN) AVANT de l'appliquer
    move_san_stockfish = board.san(result.move)
    # Appliquer le coup sur l’échiquier
    board.push(result.move)

    print("Stockfish move (SAN) :", move_san_stockfish)
    liste_des_coups+=str(move_san_stockfish)+", "

    while not board.is_game_over():
    # Afficher le plateau
        print(board)
        print(liste_des_coups)
        info = engine.analyse(board, chess.engine.Limit(time=1))  # Le temps peut être ajusté

        # Afficher l'évaluation
        evaluation = info["score"].relative.score(mate_score=10000)  # Convertit l'évaluation en centi-points
        if evaluation is not None:
            print(f"Score of the position : {evaluation / 100.0} pions")
        else:
            print("Évaluation : Échec et mat ou égalité")



        if board.turn == chess.WHITE:
            legal_moves_san = [board.san(move) for move in board.legal_moves]
            prompt = f"Here is the list of the last moves played (You are playing as white): {liste_des_coups}. What is the best move to play now if you are playing as white, using the list of legal moves: {legal_moves_san}? Respond only with the move to play and nothing else (e.g., Nf3, e4...) and do not make any comments of any kind, I just want the move."
            move=get_response_from_llm(prompt)
            try:
                uci_move = board.push_san(move)
                print("LLM move:", move, uci_move, "(UCI notations)")
                liste_des_coups+=str(move)+", "
            except ValueError:
                
                print("Invalide move by the LLM:", move, ". Try again")
                continue
        
        else:
            result = engine.play(board, chess.engine.Limit(time=2))
            # Convertir le coup en notation standard (SAN) AVANT de l'appliquer
            move_san_stockfish = board.san(result.move)
            liste_des_coups+=str(move_san_stockfish)+", "
            print("Move of Stockfish (SAN) :", move_san_stockfish)
            # Appliquer le coup sur l’échiquier
            board.push(result.move)

    engine.quit()
    result=board.result()
    print(result)

            
            

            








def llm_vs_llm():
    
    liste_des_coups=""
    # Chemin vers l'exécutable Stockfish
    stockfish_path = r"C:\Users\dadah\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

    # Vérifiez si le fichier existe et est accessible
    if not os.path.isfile(stockfish_path):
        print(f"Le fichier Stockfish n'existe pas à l'emplacement spécifié : {stockfish_path}")
        return

    # Initialiser le moteur Stockfish
    try:
        engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
        engine.configure({"Skill Level": 1})
    except PermissionError:
        print("Permission refusée. Essayez d'exécuter le script en tant qu'administrateur.")
        return
    

    #Début de la partie:
    # Initialiser le plateau
    board = chess.Board()

    

    #Premier Mouvement:
    move = get_response_from_llm("Let's play chess. You are a chess Grandmaster playing against me at your best level. What is the best move to play if you are playing as white? Respond only with the move to play and nothing else (e.g., e4, d4, etc.).")

    liste_des_coups+=str(move)+", "
    uci_move = board.push_san(move)

    print("First move:", move, uci_move, "(UCI notations)")


    result = engine.play(board, chess.engine.Limit(time=0.1))
    # Convertir le coup en notation standard (SAN) AVANT de l'appliquer
    move_san_stockfish = board.san(result.move)
    # Appliquer le coup sur l’échiquier
    board.push(result.move)

    print("Stockfish move (SAN) :", move_san_stockfish)
    liste_des_coups+=str(move_san_stockfish)+", "

    while not board.is_game_over():
    # Afficher le plateau
        print(board)
        print(liste_des_coups)
        info = engine.analyse(board, chess.engine.Limit(time=1))  # Le temps peut être ajusté

        # Afficher l'évaluation
        evaluation = info["score"].relative.score(mate_score=10000)  # Convertit l'évaluation en centi-points
        if evaluation is not None:
            print(f"Score of the position : {evaluation / 100.0} pions")
        else:
            print("Évaluation : Échec et mat ou égalité")



        if board.turn == chess.WHITE:
            legal_moves_san = [board.san(move) for move in board.legal_moves]
            prompt = f"Here is the list of the last moves played (You are playing as white): {liste_des_coups}. What is the best move to play now if you are playing as white, using the list of legal moves: {legal_moves_san}? Respond only with the move to play and nothing else (e.g., Nf3, e4...) and do not make any comments of any kind, I just want the move."
            move=get_response_from_llm(prompt)
            try:
                uci_move = board.push_san(move)
                print("LLM move:", move, uci_move, "(UCI notations)")
                liste_des_coups+=str(move)+", "
            except ValueError:
                
                print("Invalide move by the LLM:", move, ". Try again")
                continue
        
        else:
            legal_moves_san = [board.san(move) for move in board.legal_moves]
            prompt = f"Here is the list of the last moves played (You are playing as black): {liste_des_coups}. What is the best move to play now if you are playing as white, using the list of legal moves: {legal_moves_san}? Respond only with the move to play and nothing else (e.g., Nf3, e4...) and do not make any comments of any kind, I just want the move."
            move=get_response_from_llm(prompt,model="llama3")
            try:
                uci_move = board.push_san(move)
                print("LLM move:", move, uci_move, "(UCI notations)")
                liste_des_coups+=str(move)+", "
            except ValueError:
                
                print("Invalide move by the LLM:", move, ". Try again")
                continue

    engine.quit()
    result=board.result()
    print(result)


llm_vs_llm()

# def get_response_from_llm(prompt):
#     # Initialiser le modèle Mistral
#     model="deepseek-r1:14b"
#     llm = ChatOllama(model=model, temperature=0.3)

#     # Créer un message avec le prompt
#     messages = [HumanMessage(content=prompt)]

#     # Obtenir la réponse du modèle
#     response = llm.invoke(messages)
#     response=response.content.strip()

#     if model.startswith("deepseek"):
#         model2="llama3.2"
#         llm2=ChatOllama(model=model2, temperature=0.3)
#         messages2 = [HumanMessage(content="what is the move played by this player,Respond only with the move to play and nothing else (e.g., Nf3, e4...) and do not make any comments of any kind, I just want the move." + str(response) )]
#         response2=llm2.invoke(messages2)
#         return response2.strip()

#     # Retourner la réponse
#     return response
