import type { GetMeta } from "../Common/types";
import { GetSolutionArgs, SolutionGet, SolutionPost } from "./types";

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

export const getSolutionsWithArgs = async (
  args?:GetSolutionArgs): Promise<{data: Array<SolutionGet>, meta: GetMeta} | null> => {
    try {
      let argString = "";
      if (args){
        argString = "?";
        for (const key in args){
          argString += `${key}=${args[key]}&`
        }
        argString = argString.slice(0, -1);
      }
      const response = await fetch("/solution"+argString, { method: "GET" });
      if (!response.ok) {
        if (response.status === 204){
          return null;
        }
        throw `HTTP Error ${response.status}`;
      }
      //if (args){
        return await response.json();
      //} else {
      //  return {data: [await response.json()], meta:{}};
      //}

      //TODO: proper error-handling
      
    } catch (error) {
     throw error;
    }
}

export function getCurrentTimestamp(): number {
  return Date.now() / 1000;
}
