import type {
  ExerciseGet,
  ExercisePost,
  SolutionGet,
  SolutionPost,
} from "../types";

export interface ExerciseGetProgramming extends ExerciseGet {
  exercise_content: {
    code: string;
    func: string;
  };
  exercise_solution: {
    key: [params: Array<number>, result: Array<number>];
  };
}

export interface ExercisePostProgramming extends ExercisePost {
  exercise_content: {
    code: string;
    func: string;
  };
  exercise_solution: {
    [key: string]: [Array<number>, Array<number>];
  };
}

export interface SolutionGetProgramming extends SolutionGet {
  solution_content: {
    code: string;
    func: string;
  };
}

export interface SolutionPostProgramming extends SolutionPost {
  solution_content: {
    code: string;
  };
}
