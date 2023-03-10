import type { languages } from "../Common/types";

export enum exercises {
  gapText = 1,
  syntax = 2,
  parsonsPuzzle = 3,
  findTheBug = 4,
  documentation = 5,
  output = 6,
  programming = 7,
}

export enum exerciseIcons {
  gapText = "border_color",
  syntax = "abc",
  parsonsPuzzle = "extension",
  findTheBug = "bug_report",
  documentation = "assignment",
  output = "terminal",
  programming = "code",
}

export interface ExerciseGet {
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

export interface ExercisePost {
  exercise_title: string;
  exercise_description: string;
  exercise_type: exercises;
  exercise_content: any;
  exercise_language: number; 
  exercise_solution: any;
}

export interface GetExerciseArgs {
  exercise_id?: number;
  exercise_title?: string;
  exercise_description?: string;
  exercise_type_name?: string;
  exercise_type_value?: exercises;
  exercise_language_type?: languages;
  exercise_language_name?: string;
  exercise_content?: object;
  exercise_solution?: object;
}

export interface SolutionGet {
  evaluator_message: string;
  message: string;
  solution_correct: boolean;
  solution_date: string;
  solution_duration: number;
  solution_exercise: number;
  solution_id: number;
  solution_pending: boolean;
  solution_user: number;
  solution_content: unknown;
}

export interface SolutionPost {
  solution_exercise: number;
  solution_date: number;
  solution_duration: number;
  solution_content: unknown;
}

export interface GetSolutionArgs {
  evaluator_message?: string;
  message?: string;
  solution_correct?: boolean;
  solution_date?: string;
  solution_duration?: number;
  solution_exercise?: number;
  solution_id?: number;
  solution_pending?: boolean;
  solution_user?: number;
  solution_content?: unknown;
}