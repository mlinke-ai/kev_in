#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Kev.in - a coding learning platform
# Copyright (C) 2022 to 2023  Max Linke and others
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from json import JSONDecodeError, loads

from sqlalchemy.exc import NoResultFound

from backend.lib.core.config import ExerciseType
from backend.lib.interfaces.database import ExerciseModel

from .sandboxes.pyenv.pysandbox import ExecutePython

# from .sandboxes.javaenv.javasandbox import ExecuteJava


def eval_solution(solution_content: dict, exercise_id: int) -> tuple[bool | None, bool, str]:
    """
    Evaluates if a provided solution attempt is correct.

    Args:
        solution_content :class:`dict`:
            The user input form the solution attempt. This should be a JSON
            object.
        exercise_id :class:`int`
            The id form the exercise, the solution attempt is about.

    Returns:
        A Tuple of class :class:`tuple[bool | None, bool, str]`
        (solution_correct, solution_pending, eval_message). solution_correct
        stores, whether a solution is correct (if `None` the corresponding
        exercise does not exist), solution_pending_stores whether a solution has
        to be evaluated by an admin, eval_message contains a message from the
        evaluator.
    """

    try:
        exercise: ExerciseModel = ExerciseModel.query.filter_by(exercise_id=exercise_id).one()
    except NoResultFound:
        return None, False, "Unknown exercise"

    try:
        sample_sol = loads(exercise.exercise_solution)
        sample_exc = loads(exercise.exercise_content)
    except (JSONDecodeError, TypeError):
        return False, False, "Evaluation error due to missformed Content"

    eval_log: tuple[bool, str]

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


class Evaluator:
    @staticmethod
    def evaluate(**kwargs):
        # Define input arguments for evaluate
        # Get user func from head e.g. "def func(someArg, ...,)->None:" -> "func"
        pass

    @staticmethod
    def evaluate_user_code(user_input: dict, language: str, sample_sol: dict, func_head: str) -> tuple[bool, str]:
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
            result_log = pySandbox.exec_untrusted_code(user_input["code"], func_head, *arg_list)

            if result_log["RESULTLOG"]:
                # successful execution of user code
                if result_log["RESULTLOG"] == sample_sol:
                    # user code correct
                    # return {"Correct": ""}
                    return True, "Successfully passed all Tests"
                else:
                    # user code not correct
                    # return {"Incorrect": "Expected results do not equal results."}
                    return False, "Some Test cases failed"

            # Errors, Exceptions when executing user code
            else:
                if len(result_log["COMPILERLOG"]["ERROR"]) != 0:
                    # interpreter error
                    # return {"False": result_log["COMPILERLOG"]["ERROR"]}
                    return False, str(result_log["COMPILERLOG"]["ERROR"][0])
                else:
                    # execution error
                    # return {"False": result_log["EXECUTELOG"]["ERROR"]}
                    return False, str(result_log["EXECUTELOG"]["ERROR"][0])

        elif language == "Java":
            # return {"Incorrect": "Not implemented yet"}
            return False, "Java Sandbox is not supported yet"
        else:
            return False, "Usupported Language value"

    @staticmethod
    def evaluate_ppe(user_input: dict, sample_solution: dict) -> tuple[bool, str]:
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
            return False, "Wrong JSON-data-format for ParsonsPuzzle in exercise or solution"

        if t1 == t2:
            return True, "Correctly ordered all pieces"
        else:
            return False, "Wrong order of pieces"

    @staticmethod
    def evaluate_gap_text(user_input: dict, sample_solution: dict) -> tuple[bool, str]:
        """
        Evaluates, if solution for a parsons puzzle exercise is right. Expected
        solution format is:
        {
            "gap_entries": ["item1", "item2", ...]
        }
        """

        try:
            t1 = user_input["gap_entries"]
            t2 = sample_solution["gap_entries"]
        except KeyError:
            return False, "Wrong JSON-data-format for GapText in exercise or solution"

        if t1 == t2:
            return True, "Correctly filled all gaps"
        else:
            return False, "Some gaps were not correctly filled"
