class Puissance4:
    def __init__(self):
        self.jeu = [[0 for j in range(12)] for i in range(6)]
        self.joueur = 1

    def afficher(self):
        print("\n   " + "  ".join(f"{i:2}" for i in range(12)))
        print("  +" + "---+" * 12)

        for i in self.jeu:
            ligne = " | ".join(self.symbole(j) for j in i)
            print("  | " + ligne + " |")
            print("  +" + "---+" * 12)
        print()



    def symbole(self, j):
        if j == 1:
            return "X"
        elif j == -1:
            return "O"
        else:
            return " "

    def actions(self):
        return [j for j in range(12) if self.jeu[0][j] == 0]

    def placer(self, colonne, joueur):
        temp = [j[:] for j in self.jeu]
        for i in range(5, -1, -1):
            if temp[i][colonne] == 0:
                temp[i][colonne] = joueur
                break
        return temp

    def resultatsurjeu(self, jeu):
        for i in range(6):
            for j in range(12):
                joueur = jeu[i][j]
                if joueur == 0:
                    continue
                if j <= 8 and all(jeu[i][j + u] == joueur for u in range(4)):
                    return joueur
                if i <= 2 and all(jeu[i + u][j] == joueur for u in range(4)):
                    return joueur
                if i <= 2 and j <= 8 and all(jeu[i + u][j + u] == joueur for u in range(4)):
                    return joueur
                if i >= 3 and j <= 8 and all(jeu[i - u][j + u] == joueur for u in range(4)):
                    return joueur
        return None

    def resultat(self):
        return self.resultatsurjeu(self.jeu)

    def testfinjeu(self, jeu):
        return self.resultatsurjeu(jeu) is not None or all(jeu[0][j] != 0 for j in range(12))

    def testfin(self):
        return self.testfinjeu(self.jeu)

    def heuristiquesurjeu(self, jeu, joueur):
        score = 0
        adversaire = -joueur
        gagnant = self.resultatsurjeu(jeu)
        if gagnant == joueur:
            return 100000
        elif gagnant == adversaire:
            return -100000

        def eval_ligne(ligne):
            s = 0
            if ligne.count(joueur) == 4:
                s += 100000
            elif ligne.count(joueur) == 3 and ligne.count(0) == 1:
                s += 50
            elif ligne.count(joueur) == 2 and ligne.count(0) == 2:
                s += 10
            elif ligne.count(joueur) == 1 and ligne.count(0) == 3:
                s += 1
            if ligne.count(adversaire) == 4:
                s -= 100000
            elif ligne.count(adversaire) == 3 and ligne.count(0) == 1:
                s -= 80
            elif ligne.count(adversaire) == 2 and ligne.count(0) == 2:
                s -= 15
            elif ligne.count(adversaire) == 1 and ligne.count(0) == 3:
                s -= 2
            return s

        for i in range(6):
            for j in range(12 - 3):
                ligne = [jeu[i][j + k] for k in range(4)]
                score += eval_ligne(ligne)

        for j in range(12):
            for i in range(6 - 3):
                col = [jeu[i + k][j] for k in range(4)]
                score += eval_ligne(col)

        for i in range(6 - 3):
            for j in range(12 - 3):
                diag1 = [jeu[i + k][j + k] for k in range(4)]
                diag2 = [jeu[i + 3 - k][j + k] for k in range(4)]
                score += eval_ligne(diag1)
                score += eval_ligne(diag2)

        for j in range(4, 8):
            for i in range(6):
                if jeu[i][j] == joueur:
                    score += 3
                elif jeu[i][j] == adversaire:
                    score -= 3

        return score

    def heuristique(self, joueur):
        return self.heuristiquesurjeu(self.jeu, joueur)

    def minmax(self, jeu, joueur, profondeur, alpha=-float("inf"), beta=float("inf"), joueurmax=True):
        gagnant = self.resultatsurjeu(jeu)
        if gagnant == 1:
            return 100000 - (6 - profondeur), None
        elif gagnant == -1:
            return -100000 + (6 - profondeur), None
        elif self.testfinjeu(jeu):
            return 0, None
        elif profondeur == 0:
            return self.heuristiquesurjeu(jeu, 1), None

        actions_possibles = [j for j in range(12) if jeu[0][j] == 0]

        if joueurmax:
            meilleur_score = -float("inf")
            meilleur_coup = actions_possibles[0] if actions_possibles else None
            for action in actions_possibles:
                nouveau_jeu = self.placersurjeu(jeu, action, 1)
                score, _ = self.minmax(nouveau_jeu, -1, profondeur - 1, alpha, beta, False)
                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_coup = action
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return meilleur_score, meilleur_coup
        else:
            meilleur_score = float("inf")
            meilleur_coup = actions_possibles[0] if actions_possibles else None
            for action in actions_possibles:
                nouveau_jeu = self.placersurjeu(jeu, action, -1)
                score, _ = self.minmax(nouveau_jeu, 1, profondeur - 1, alpha, beta, True)
                if score < meilleur_score:
                    meilleur_score = score
                    meilleur_coup = action
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return meilleur_score, meilleur_coup

    def placersurjeu(self, jeu, colonne, joueur):
        temp = [ligne[:] for ligne in jeu]
        for i in range(5, -1, -1):
            if temp[i][colonne] == 0:
                temp[i][colonne] = joueur
                break
        return temp

    def decisionIA(self, board):
        _, coup = self.minmax(board, 1, profondeur=5, joueurmax=True)
        return coup

    def jouer(self):
        self.jeu = [[0 for j in range(12)] for i in range(6)]
        print("Choisissez votre joueur:")
        print("1 = X (vous commencez)")
        print("-1 = O (IA commence)")

        while True:
            try:
                jh = int(input("Votre choix (1 ou -1): "))
                if jh in [1, -1]:
                    break
                else:
                    print("Veuillez entrer 1 ou -1")
            except ValueError:
                print("Entrée invalide")

        j2 = -jh
        jc = 1

        print(f"\nVous êtes {'X' if jh == 1 else 'O'}")
        print(f"L'IA est {'X' if jh == -1 else 'O'}")

        while not self.testfin():
            self.afficher()
            print(f"Au tour de {'X' if jc == 1 else 'O'}")

            if jc == jh:
                while True:
                    try:
                        col = int(input("Colonne (0 à 11): "))
                        if 0 <= col <= 11 and col in self.actions():
                            self.jeu = self.placer(col, jc)
                            break
                        else:
                            print("Colonne pleine ou invalide")
                    except ValueError:
                        print("Entrée invalide")
            else:
                print("L'IA réfléchit...")
                if jc == 1:
                    _, coup = self.minmax(self.jeu, 1, profondeur=5, joueurmax=True)
                else:
                    _, coup = self.minmax(self.jeu, -1, profondeur=5, joueurmax=False)
                if coup is not None:
                    self.jeu = self.placer(coup, jc)
                    print(f"L'IA ({'X' if jc == 1 else 'O'}) joue en colonne {coup}")
                else:
                    print("Erreur: L'IA n'a pas pu choisir un coup")

            jc = -jc

        self.afficher()
        g = self.resultat()
        if g:
            if g == jh:
                print("Vous avez gagné")
            else:
                print("L'IA a gagné")
        else:
            print("Match nul")


if __name__ == "__main__":
    jeu = Puissance4()
    jeu.jouer()