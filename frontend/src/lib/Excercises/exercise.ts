import type { GetMeta } from "../Common/types";
import type { ExerciseGet, ExercisePost, GetExerciseArgs } from "./types"

export interface FillInBlanksExerciseType extends ExerciseType {
  exercise_content: {
    text: String;
    blankPos: Int32Array; // welcher integer?
  };
  exercise_solution: {
    userEntries: Array<string>;
  };
}

export const getExercise = async (
  exerciseID: number
): Promise<ExerciseGet | null> => {
  try {
    const response = await fetch(
      `/exercise?exercise_id=${exerciseID}&exercise_limit=1&exercise_details=true`,
      {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      }
    );
    if (!response.ok) {
      throw `HTTP Error ${response.status}`
    }
    return await response.json().then((data) => data.data[0]);
  } catch (err) {
    throw err
  }
};

export const getExercisesWithArgs = async (
  args?:GetExerciseArgs): Promise<{data: Array<ExerciseGet>, meta: GetMeta} | null> => {
    try {
      let argString = "";
      if (args){
        argString = "?";
        for (const key in args){
          argString += `${key}=${args[key]}&`
        }
        argString = argString.slice(0, -1);
      }
      const response = await fetch("/exercise"+argString, { method: "GET" });
      if (!response.ok) {
        throw `HTTP Error ${response.status}`;
      }
      //if (args){
        return await response.json();
      //} else {
      //  return {data: [await response.json()], meta:{}};
      //}
      
    } catch (error) {
     throw error;
    }
}

export const postExercise = async (exercise: ExercisePost) => {
  try {
    const response = await fetch("/exercise",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(exercise)//exercise as unknown as BodyInit
      }
    );
    if (!response.ok) {
      throw `HTTP Error ${response.status}`
    }
    console.log("Created!")
  } catch (err) {
    throw err
  }
};