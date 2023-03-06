import type { ExerciseGet, ExercisePost } from "./types"

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