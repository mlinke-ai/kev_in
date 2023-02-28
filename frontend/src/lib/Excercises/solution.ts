interface SolutionPost {
  solution_exercise: number;
  solution_date: number;
  solution_duration: number;
}

export interface SolutionPostProgramming extends SolutionPost {
  solution_content: {
    code: string;
  };
}

export interface SolutionPostParsonsPuzzle extends SolutionPost {
  solution_content: {
    list: Array<string>;
  };
}

export interface SolutionPostFillInBlanks extends SolutionPost {
  solution_content: {
    list: Array<string>;
  };
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
  solution_content?: unknown;
}

export interface SolutionGetProgramming extends SolutionGet {
  solution_content: {
    code: string;
    func: string;
  };
}

export const submitSolution = async (
  solution: SolutionPostProgramming | SolutionPostParsonsPuzzle
):Promise<SolutionGet | null> => {
  try {
    const response = await fetch("/solution", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        solution_exercise: solution.solution_exercise,
        solution_date: solution.solution_date,
        solution_duration: solution.solution_duration,
        solution_content: solution.solution_content,
      }),
    });
    if (!response.ok) {
      throw `HTTP Error ${response.status}`
    }
    return await response.json().then((data) => data);
  } catch (err) {
    throw err
  }
};

export function getCurrentTimestamp(): number {
  return Date.now() / 1000;
}
