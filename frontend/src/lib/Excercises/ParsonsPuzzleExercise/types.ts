import type { ExerciseGet, SolutionPost } from "../types";

export interface ExerciseGetPPE extends ExerciseGet {
  exercise_content: {
    list: Array<string>;
  };
  exercise_solution: {
    list: Array<string>;
  };
}

export interface SolutionPostPPE extends SolutionPost {
  solution_content: {
    list: Array<string>;
  };
}
