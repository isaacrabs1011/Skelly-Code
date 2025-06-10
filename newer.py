# Skeleton Program code for the AQA A Level Paper 1 Summer 2025 examination
# Updated with brackets, exponentiation, score fix, and input validation
# Written in Python 3.9

import re
import random
import math


def Main():
    NumbersAllowed = []
    Targets = []
    MaxNumberOfTargets = 20
    MaxTarget = 0
    MaxNumber = 0
    TrainingGame = False
    Choice = input("Enter y to play the training game, anything else to play a random game: ").lower()
    print()
    if Choice == "y":
        MaxNumber = 1000
        MaxTarget = 1000
        TrainingGame = True
        Targets = [-1, -1, -1, -1, -1, 23, 9, 140, 82, 121, 34, 45, 68, 75, 34, 23, 119, 43, 23, 119]
    else:
        MaxNumber = 10
        MaxTarget = 50
        Targets = CreateTargets(MaxNumberOfTargets, MaxTarget)
    NumbersAllowed = FillNumbers(NumbersAllowed, TrainingGame, MaxNumber)
    PlayGame(Targets, NumbersAllowed, TrainingGame, MaxTarget, MaxNumber)
    input()


def PlayGame(Targets, NumbersAllowed, TrainingGame, MaxTarget, MaxNumber):
    Score = 0
    GameOver = False
    while not GameOver:
        DisplayState(Targets, NumbersAllowed, Score)
        UserInput = input("Enter an expression: ").replace(" ", "")
        print()
        if CheckIfUserInputValid(UserInput):
            UserInputInRPN = ConvertToRPN(UserInput)
            if CheckNumbersUsedAreAllInNumbersAllowed(NumbersAllowed, UserInputInRPN, MaxNumber):
                IsTarget, Score = CheckIfUserInputEvaluationIsATarget(Targets, UserInputInRPN, Score)
                if IsTarget:
                    NumbersAllowed = RemoveNumbersUsed(UserInput, MaxNumber, NumbersAllowed)
                    NumbersAllowed = FillNumbers(NumbersAllowed, TrainingGame, MaxNumber)
        Score -= 1
        if Targets[0] != -1:
            GameOver = True
        else:
            Targets = UpdateTargets(Targets, TrainingGame, MaxTarget)
    print("Game over!")
    DisplayScore(Score)


def CheckIfUserInputEvaluationIsATarget(Targets, UserInputInRPN, Score):
    UserInputEvaluation = EvaluateRPN(UserInputInRPN.copy())
    UserInputEvaluationIsATarget = False
    if UserInputEvaluation != -1:
        for Count in range(0, len(Targets)):
            if Targets[Count] == UserInputEvaluation:
                Score += 2
                Targets[Count] = -1
                UserInputEvaluationIsATarget = True
                break  # Avoid duplicate scoring for same match
    return UserInputEvaluationIsATarget, Score


def RemoveNumbersUsed(UserInput, MaxNumber, NumbersAllowed):
    UserInputInRPN = ConvertToRPN(UserInput)
    for Item in UserInputInRPN:
        if CheckValidNumber(Item, MaxNumber):
            if int(Item) in NumbersAllowed:
                NumbersAllowed.remove(int(Item))
    return NumbersAllowed


def UpdateTargets(Targets, TrainingGame, MaxTarget):
    for Count in range(0, len(Targets) - 1):
        Targets[Count] = Targets[Count + 1]
    Targets.pop()
    if TrainingGame:
        Targets.append(Targets[-1])
    else:
        Targets.append(GetTarget(MaxTarget))
    return Targets


def CheckNumbersUsedAreAllInNumbersAllowed(NumbersAllowed, UserInputInRPN, MaxNumber):
    Temp = NumbersAllowed.copy()
    for Item in UserInputInRPN:
        if CheckValidNumber(Item, MaxNumber):
            if int(Item) in Temp:
                Temp.remove(int(Item))
            else:
                return False
    return True


def CheckValidNumber(Item, MaxNumber):
    if re.fullmatch(r"[0-9]+", Item):
        ItemAsInteger = int(Item)
        if 1 <= ItemAsInteger <= MaxNumber:
            return True
    return False


def DisplayState(Targets, NumbersAllowed, Score):
    DisplayTargets(Targets)
    DisplayNumbersAllowed(NumbersAllowed)
    DisplayScore(Score)


def DisplayScore(Score):
    print("Current score: " + str(Score))
    print("\n")


def DisplayNumbersAllowed(NumbersAllowed):
    print("Numbers available: ", end='')
    for N in NumbersAllowed:
        print(str(N) + "  ", end='')
    print("\n")


def DisplayTargets(Targets):
    print("|", end='')
    for T in Targets:
        print(" " if T == -1 else T, end='|')
    print()


def ConvertToRPN(UserInput):
    Precedence = {"+": 2, "-": 2, "*": 4, "/": 4, "^": 6}
    Operators = []
    Output = []
    i = 0
    while i < len(UserInput):
        char = UserInput[i]
        if char.isdigit():
            number = char
            i += 1
            while i < len(UserInput) and UserInput[i].isdigit():
                number += UserInput[i]
                i += 1
            Output.append(number)
            continue
        elif char == "(":
            Operators.append(char)
        elif char == ")":
            while Operators and Operators[-1] != "(":
                Output.append(Operators.pop())
            if Operators and Operators[-1] == "(":
                Operators.pop()
        elif char in Precedence:
            while (Operators and Operators[-1] in Precedence and
                   Precedence[Operators[-1]] >= Precedence[char]):
                Output.append(Operators.pop())
            Operators.append(char)
        i += 1
    while Operators:
        Output.append(Operators.pop())
    return Output


def EvaluateRPN(UserInputInRPN):
    S = []
    try:
        while UserInputInRPN:
            while UserInputInRPN[0] not in ["+", "-", "*", "/", "^"]:
                S.append(UserInputInRPN.pop(0))
            Num2 = float(S.pop())
            Num1 = float(S.pop())
            Op = UserInputInRPN.pop(0)
            if Op == "+":
                S.append(str(Num1 + Num2))
            elif Op == "-":
                S.append(str(Num1 - Num2))
            elif Op == "*":
                S.append(str(Num1 * Num2))
            elif Op == "/":
                if Num2 == 0:
                    return -1
                S.append(str(Num1 / Num2))
            elif Op == "^":
                S.append(str(Num1 ** Num2))
        result = float(S[0])
        return int(result) if result.is_integer() else -1
    except:
        return -1


def GetNumberFromUserInput(UserInput, Position):
    Number = ""
    while Position < len(UserInput) and UserInput[Position].isdigit():
        Number += UserInput[Position]
        Position += 1
    return (int(Number), Position) if Number else (-1, Position)


def CheckIfUserInputValid(UserInput):
    # Updated regex to allow brackets, multi-digit numbers, and operators
    return re.fullmatch(r"[0-9+\-*/^() ]+", UserInput) is not None


def GetTarget(MaxTarget):
    return random.randint(1, MaxTarget)


def GetNumber(MaxNumber):
    return random.randint(1, MaxNumber)


def CreateTargets(SizeOfTargets, MaxTarget):
    return [-1] * 5 + [GetTarget(MaxTarget) for _ in range(SizeOfTargets - 5)]


def FillNumbers(NumbersAllowed, TrainingGame, MaxNumber):
    if TrainingGame:
        return [2, 3, 2, 8, 512]
    else:
        while len(NumbersAllowed) < 5:
            NumbersAllowed.append(GetNumber(MaxNumber))
        return NumbersAllowed


if __name__ == "__main__":
    Main()
