import type { languages } from "../common/types";

export enum exercises {
  gapText = 1,
  syntax = 2,
  parsonsPuzzle = "ParsonsPuzzleExercise",
  findTheBug = 4,
  documentation = 5,
  output = 6,
  programming = "ProgrammingExercise",
}

interface ExerciseType {
  exercise_id: number;
  exercise_title: string;
  exercise_description: string;
  exercise_type_name: string;
  exercise_type_value: exercises;
  exercise_language_type: languages;
  exercise_language_name: string;
  exercise_content: object;
  exercise_solution: object;
}

export enum exerciseIcons {
  gapText = "",
  syntax = "",
  parsonsPuzzle = "extension",
  findTheBug = "",
  documentation = "",
  output = "",
  programming = "code",
}

export interface ProgrammingExerciseType extends ExerciseType {
  exercise_content: {
    code: string;
    func: string;
  };
  exercise_solution: {
    key: [params: Array<number>, result: Array<number>];
  };
}

export interface ParsonsPuzzleExerciseType extends ExerciseType {
  exercise_content: {
    list: Array<string>;
  };
  exercise_solution: {
    list: Array<string>;
  };
}
