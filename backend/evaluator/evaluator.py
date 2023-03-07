#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask_sqlalchemy.query import sqlalchemy

from backend.database.models import ExerciseLanguage, ExerciseModel, ExerciseType
from backend.evaluator.sandboxes.pyenv.pysandbox import ExecutePython

# from backend.evaluator.sandboxes.javaenv.javasandboxes import ExecuteJava


def eval_solution(solution_content: dict, exercise_id: int) -> tuple[bool | None, bool, str]:
    """
    Evaluates whether a solution attempt is correct.

    Args:
        solution_content (dict): The user input from the solution attempt. This should be a JSON object.
        exercise_id (int): The ID from the exercise, the solution attempt is about.

    Returns:
        tuple[bool | None, bool, str]: A tuple describing whether the solution attempt is correct, needs manual evaluation and a message from the evaluator.
    """
    try:
        exercise = ExerciseModel.query.filter_by(exercise_id=exercise_id).one()
    except sqlalchemy.exc.NoResultFound as e:
        return None, False, "Unknown exercise"

    try:
        sample_sol = json.loads(exercise.exercise_solution)
        sample_exc = json.loads(exercise.exercise_content)
    except json.JSONDecodeError as e:
        return False, False, "Decoding failed failed due to an encoding error"
    except TypeError as e:
        return False, False, "decoding failed due to a type error"

    if exercise.exercise_type == ExerciseType.GapTextExercise:
        eval_log = Evaluator.evaluate_gap_text(solution_content, sample_sol)
        return eval_log[0], False, eval_log[1]
    elif exercise.exercise_type == ExerciseType.SyntaxExercise:
        return True, False, "Evaluation not implemented yet"
    elif exercise.exercise_type == ExerciseType.ParsonsPuzzleExercise:
        eval_log = Evaluator.evaluate_ppe(solution_content, sample_sol)
        return eval_log[0], False, eval_log[1]
    elif exercise.exercise_type == ExerciseType.FindTheBugExercise:
        return True, False, "Evaluation not implemented yet"
    elif exercise.exercise_type == ExerciseType.DocumentationExercise:
        return False, True, "An Andmin has to review this Solution"
    elif exercise.exercise_type == ExerciseType.OutputExercise:
        return True, False, "Evaluation not implemented yet"
    elif exercise.exercise_type == ExerciseType.ProgrammingExercise:
        eval_log = Evaluator.evaluate_user_code(
            solution_content, exercise.exercise_language.name, sample_sol, sample_exc["func"]
        )
        return eval_log[0], False, eval_log[1]
    else:
        return False, False, "Unknown exercise type"


class Evaluator:
    @staticmethod
    def evaluate(**kwargs: dict) -> None:
        pass

    @staticmethod
    def evaluate_user_code(
        user_input: dict, language: ExerciseLanguage, sample_sol: dict, func_head: str
    ) -> tuple[bool, str]:
        """
        Execute and evaluate untrusted user code.

        Args:
            user_input (dict): The user code as a string in dict.
            language (ExerciseLanguage): The language of the exercise. Either 'Python' or 'Java'.
            sample_sol (dict): The test cases.
            func_head (str): The function which should be tested.

        Returns:
            tuple[bool, str]: A tuple with the evaluation result and a message.
        """
        if language == ExerciseLanguage.Python:
            py_sandbox = ExecutePython()
            arg_list = [args[0] for args in sample_sol.values()]
            result_log = py_sandbox.exec_untrusted_code(user_input["code"], func_head, *arg_list)
            if result_log["RESULTLOG"]:
                # successful execution of user code
                if result_log["RESULTLOG"] == sample_sol:
                    # user code correct
                    return True, "Successfully passed all tests"
                else:
                    # user code not correct
                    return False, "Some test cases failed"
            else:
                # errors, exceptions while executing, compiling user code
                if len(result_log["COMPILERLOG"]) != 0:
                    # interpreter error
                    return False, str(result_log["COMPILERLOG"]["ERROR"[0]])
                else:
                    # execution error
                    return False, str(result_log["EXECUTELOG"]["ERROR"][0])
        elif language == ExerciseLanguage.Java:
            return False, "Java is not yet supported"
        else:
            return False, "Unknown language"

    @staticmethod
    def evaluate_ppe(user_input: dict, sample_solution: dict) -> tuple[bool, str]:
        """
        Evaluate whether the solution attempt for a parsons puzzle exercise is correct.

        Args:
            user_input (dict): The user input.
            sample_solution (dict): The expected solution.

        Returns:
            tuple[bool,str]: A tuple whether the solution is correct and a message.
        """
        try:
            t1 = user_input["list"]
            t2 = sample_solution["list"]
        except KeyError as e:
            return False, "Wrong JSON-data-format"

        if t1 == t2:
            return True, "Correctly ordered all pieces"
        else:
            return False, "Wrong order of pieces"

    @staticmethod
    def evaluate_gap_text(user_input: dict, sample_solution: dict) -> tuple[bool, str]:
        """
        Evaluate whether the solution attempt for a gap text exercise is correct.

        Args:
            user_input (dict): The user input.
            sample_solution (dict): The expected solution.

        Returns:
            tuple[bool,str]: A tuple whether the solution is correct and a message.
        """
        try:
            t1 = user_input["gap_entries"]
            t2 = sample_solution["gap_entries"]
        except KeyError as e:
            return False, "Wrong JSON-data-format"

        if t1 == t2:
            return True, "Correctly filled all gaps"
        else:
            return False, "Some gaps were not correctly filled"
