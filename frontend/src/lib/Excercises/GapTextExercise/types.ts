import { SolutionPost } from "../types";

export interface SolutionPostFillInBlanks extends SolutionPost {
  solution_content: {
    list: Array<string>;
  };
}
