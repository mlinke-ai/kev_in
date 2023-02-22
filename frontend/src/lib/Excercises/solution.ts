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

// export interface FillInBlanksExerciseType extends SolutionPost {
//   solution_content: {
//     list: Array<string>;
//   };
// }

export const submitSolution = async (solution: SolutionPostProgramming | SolutionPostParsonsPuzzle) => {
  try {
    const response = await fetch("/solution", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        solution_exercise: solution.solution_exercise,
        solution_date: solution.solution_date,
        solution_duration: solution.solution_duration,
        solution_content: solution.solution_content
      }),
    });
    if (!response.ok) {
      
    }
    await response.json().then((data) => console.log(data));
  } catch (error) {
    console.error(error);
  }
};

export function getCurrentTimestamp(): number {
  return Date.now() / 1000;
}
