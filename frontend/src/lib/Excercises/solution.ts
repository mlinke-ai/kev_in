import { SolutionGet, SolutionPost } from "./types";

export const submitSolution = async (
  solution: SolutionPost
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
