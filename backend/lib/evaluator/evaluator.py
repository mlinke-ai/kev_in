#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from json import loads, JSONDecodeError

from backend.lib.core.config import ExerciseType
from backend.lib.interfaces.database import ExerciseModel

from .sandboxes.pyenv.pysandbox import ExecutePython

# from .sandboxes.javaenv.javasandbox import ExecuteJava

def eval_solution(
        solution_content: dict,
        exercise_id: int
        ) -> tuple[bool, bool]:
    """
    Evaluates if a provided solution attempt is correct.

    Args:
        solution_content :class:`dict`:
            The user input form the solution attempt. This should be a JSON
            object.
        exercise_id :class:`int`
            The id form the exercise, the solution attempt is about.
            
    """
    
    exercise: ExerciseModel = (
        ExerciseModel
        .query
        .filter_by(exercise_id=exercise_id)
        .one()
    )
    try:
        sample_sol = loads(exercise.exercise_solution)
    except (JSONDecodeError, TypeError):
        return False, False
    
    if exercise.exercise_type == ExerciseType.GapTextExercise:
        return True, False
    
    elif exercise.exercise_type == ExerciseType.SyntaxExercise:
        return True, False
    
    elif exercise.exercise_type == ExerciseType.ParsonsPuzzleExercise:
        return (
            Evaluator.evaluate_ppe(solution_content, sample_sol),
            False
        )
    
    elif exercise.exercise_type == ExerciseType.FindTheBugExercise:
        return True, False
    
    elif exercise.exercise_type == ExerciseType.DocumentationExercise:
        return True, False
    
    elif exercise.exercise_type == ExerciseType.OutputExercise:
        return True, False
    
    elif exercise.exercise_type == ExerciseType.ProgrammingExercise:
        return True, False


class Evaluator:

    @staticmethod
    def evaluate(**kwargs):
        # Define input arguments for evaluate
        # Get user func from head e.g. "def func(someArg, ...,)->None:" -> "func"
        pass

    # TODO function name required "user_func"
    @staticmethod
    def evaluate_user_code(user_code: str, user_func: str, language: str, **args_result_dict: dict) -> dict:
        """
        Description: Execute and evaluate untrusted user code.

        Args:
            user_code: String containing user code.
            user_func: Function inside user_code to execute. E.g. "def fibonacci(n):"
            language: "python" or "java"
            **args_result_dict: Dictionary {'1': ([Arg1, Arg2,.., Argn], [Result]), \
                                            '2': ([Args], [Result]), ..}
                                            e.g. {'1': ([2, 2, 2], [8])}
                                            Dictionary with input args and expected result.
        Return:
            Dictionary as a result log:
            {'Correct': ""} or if false
            {'Incorrect': "E.g. some errors, exceptions, or wrong result information"}
        """
        if language == "python":
            pySandbox = ExecutePython()
            arg_list = [args[0] for args in args_result_dict.values()]
            result_log = pySandbox.exec_untrusted_code(user_code, user_func, *arg_list)

            if result_log["RESULTLOG"]:
                # successful execution of user code
                if result_log["RESULTLOG"] == args_result_dict:
                    # user code correct
                    return {"Correct": ""}
                else:
                    # user code not correct
                    return {"Incorrect": "Expected results do not equal results."}

            # Errors, Exceptions when executing user code
            else:
                if len(result_log["COMPILERLOG"]["ERROR"]) != 0:
                    # interpreter error
                    return {"False": result_log["COMPILERLOG"]["ERROR"]}
                else:
                    # execution error
                    return {"False": result_log["EXECUTELOG"]["ERROR"]}

        elif language == "java":
            return {"Incorrect": "Not implemented yet"}
        else:
            return dict()

    @staticmethod
    def evaluate_ppe(user_input: dict, sample_solution: dict) -> bool:
        """
        Evaluates, if solution for a parsons puzzle exercise is right. Expected
        solurion format is:
        {
            "list": ["item1", "item2", ...]
        }
        """

        try:
            t1 = user_input["list"]
            t2 = sample_solution["list"]
        except KeyError:
            return False #wrong format somewhere

        return t1 == t2