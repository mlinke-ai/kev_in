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
) -> (bool, bool):
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
        sample_exc = loads(exercise.exercise_content)
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
        return Evaluator.evaluate_user_code(solution_content, exercise.exercise_language.name,
                                            sample_sol, sample_exc['func']), False


class Evaluator:

    @staticmethod
    def evaluate(**kwargs):
        # Define input arguments for evaluate
        # Get user func from head e.g. "def func(someArg, ...,)->None:" -> "func"
        pass

    @staticmethod
    def evaluate_user_code(user_input: dict, language: str, sample_sol: dict, func_head: str) -> bool:
        """
        Description: Execute and evaluate untrusted user code.

        :arg:
            user_input: { 'code': "user code in string format" }
            language: "Python" or "Java"
            sample_sol: {   "0": [[<params>],[<result>]],
                            "1": [[<params>],[<result>]],
                            ...
                            "n": [[<params>],[<result>]]
                        }
            func_head: "head of function which should be tested"

        :return:
            Dictionary as a result log possible:
            {'Correct': ""} or if false
            {'Incorrect': "E.g. some errors, exceptions, or wrong result information"}
            Currently implemented only boolean.
        """

        if language == "Python":
            pySandbox = ExecutePython()
            arg_list = [args[0] for args in sample_sol.values()]
            result_log = pySandbox.exec_untrusted_code(user_input['code'],
                                                       func_head, *arg_list)

            if result_log["RESULTLOG"]:
                # successful execution of user code
                if result_log["RESULTLOG"] == sample_sol:
                    # user code correct
                    # return {"Correct": ""}
                    return True
                else:
                    # user code not correct
                    # return {"Incorrect": "Expected results do not equal results."}
                    return False

            # Errors, Exceptions when executing user code
            else:
                if len(result_log["COMPILERLOG"]["ERROR"]) != 0:
                    # interpreter error
                    # return {"False": result_log["COMPILERLOG"]["ERROR"]}
                    return False
                else:
                    # execution error
                    # return {"False": result_log["EXECUTELOG"]["ERROR"]}
                    return False

        elif language == "Java":
            # return {"Incorrect": "Not implemented yet"}
            return False
        else:
            return False

    @staticmethod
    def evaluate_ppe(user_input: dict, sample_solution: dict) -> bool:
        """
        Evaluates, if solution for a parsons puzzle exercise is right. Expected
        solution format is:
        {
            "list": ["item1", "item2", ...]
        }
        """

        try:
            t1 = user_input["list"]
            t2 = sample_solution["list"]
        except KeyError:
            return False  # wrong format somewhere

        return t1 == t2
