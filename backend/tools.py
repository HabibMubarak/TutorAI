import random

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def generate_math_problem(topic: str, difficulty: str = "medium") -> dict:
    """Generates a math problem based on the specified topic and difficulty level.

    Args:
        topic (str): The type of math problem. Options: "addition", "subtraction", 
                     "multiplication", "division", "fraction", "equation"
        difficulty (str): Difficulty level - "easy", "medium", or "hard". Default is "medium".

    Returns:
        dict: Contains the problem, solution, and step-by-step explanation.
    """
    topic = topic.lower()
    difficulty = difficulty.lower()
    
    if topic == "addition":
        if difficulty == "easy":
            a, b = random.randint(1, 20), random.randint(1, 20)
        elif difficulty == "hard":
            a, b = random.randint(100, 500), random.randint(100, 500)
        else:  # medium
            a, b = random.randint(20, 100), random.randint(20, 100)
        
        problem = f"{a} + {b} = ?"
        solution = a + b
        steps = f"Schritt 1: Addiere {a} und {b}\nSchritt 2: {a} + {b} = {solution}"
        
    elif topic == "subtraction":
        if difficulty == "easy":
            a, b = random.randint(10, 30), random.randint(1, 10)
        elif difficulty == "hard":
            a, b = random.randint(200, 600), random.randint(50, 200)
        else:  # medium
            a, b = random.randint(30, 150), random.randint(10, 50)
        
        problem = f"{a} - {b} = ?"
        solution = a - b
        steps = f"Schritt 1: Subtrahiere {b} von {a}\nSchritt 2: {a} - {b} = {solution}"
        
    elif topic == "multiplication":
        if difficulty == "easy":
            a, b = random.randint(2, 10), random.randint(2, 10)
        elif difficulty == "hard":
            a, b = random.randint(15, 50), random.randint(15, 50)
        else:  # medium
            a, b = random.randint(10, 25), random.randint(10, 25)
        
        problem = f"{a} × {b} = ?"
        solution = a * b
        steps = f"Schritt 1: Multipliziere {a} mit {b}\nSchritt 2: {a} × {b} = {solution}"
        
    elif topic == "division":
        if difficulty == "easy":
            b = random.randint(2, 10)
            solution = random.randint(2, 10)
        elif difficulty == "hard":
            b = random.randint(10, 30)
            solution = random.randint(10, 30)
        else:  # medium
            b = random.randint(5, 15)
            solution = random.randint(5, 20)
        
        a = b * solution
        problem = f"{a} ÷ {b} = ?"
        steps = f"Schritt 1: Dividiere {a} durch {b}\nSchritt 2: {a} ÷ {b} = {solution}"
        
    elif topic == "fraction":
        if difficulty == "easy":
            num1, den1 = random.randint(1, 5), random.randint(2, 8)
            num2, den2 = random.randint(1, 5), random.randint(2, 8)
        elif difficulty == "hard":
            num1, den1 = random.randint(5, 20), random.randint(6, 30)
            num2, den2 = random.randint(5, 20), random.randint(6, 30)
        else:  # medium
            num1, den1 = random.randint(1, 10), random.randint(2, 12)
            num2, den2 = random.randint(1, 10), random.randint(2, 12)
        
        # Common denominator
        common_den = den1 * den2
        new_num1 = num1 * den2
        new_num2 = num2 * den1
        result_num = new_num1 + new_num2
        
        from math import gcd
        divisor = gcd(result_num, common_den)
        final_num = result_num // divisor
        final_den = common_den // divisor
        
        # LaTeX formatting for proper fraction display
        problem_latex = f"$$\\frac{{{num1}}}{{{den1}}} + \\frac{{{num2}}}{{{den2}}} = ?$$"
        problem = f"{num1}/{den1} + {num2}/{den2} = ?"
        solution_latex = f"$$\\frac{{{final_num}}}{{{final_den}}}$$" if final_den != 1 else f"$${final_num}$$"
        solution = f"{final_num}/{final_den}" if final_den != 1 else str(final_num)
        
        steps = (f"Schritt 1: Hauptnenner finden: {den1} × {den2} = {common_den}\n"
                f"Schritt 2: Erweitern:\n"
                f"  $$\\frac{{{num1}}}{{{den1}}} = \\frac{{{new_num1}}}{{{common_den}}}$$\n"
                f"  $$\\frac{{{num2}}}{{{den2}}} = \\frac{{{new_num2}}}{{{common_den}}}$$\n"
                f"Schritt 3: Addieren:\n"
                f"  $$\\frac{{{new_num1}}}{{{common_den}}} + \\frac{{{new_num2}}}{{{common_den}}} = \\frac{{{result_num}}}{{{common_den}}}$$\n"
                f"Schritt 4: Kürzen: $$\\frac{{{result_num}}}{{{common_den}}} = {solution_latex}$$")
        
    elif topic == "equation":
        if difficulty == "easy":
            x = random.randint(1, 10)
            b = random.randint(1, 20)
        elif difficulty == "hard":
            x = random.randint(10, 50)
            b = random.randint(20, 100)
        else:  # medium
            x = random.randint(5, 25)
            b = random.randint(10, 50)
        
        a = random.randint(2, 10)
        c = a * x + b
        
        problem = f"{a}x + {b} = {c}, löse nach x auf"
        solution = x
        steps = (f"Schritt 1: Subtrahiere {b} von beiden Seiten: {a}x = {c - b}\n"
                f"Schritt 2: Dividiere durch {a}: x = {(c - b) / a}\n"
                f"Schritt 3: x = {solution}")
    else:
        return {
            "status": "error",
            "error_message": f"Unbekanntes Thema '{topic}'. Verfügbare Themen: addition, subtraction, multiplication, division, fraction, equation"
        }
    
    return {
        "status": "success",
        "problem": problem,
        "problem_latex": problem_latex if topic == "fraction" else None,
        "solution": str(solution),
        "solution_latex": solution_latex if topic == "fraction" else None,
        "steps": steps,
        "topic": topic,
        "difficulty": difficulty
    }
