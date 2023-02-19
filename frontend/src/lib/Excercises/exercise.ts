import type { ProgrammingExerciseType, ParsonsPuzzleExerciseType } from "./types"

export const getExercise = async (
  exerciseID: number
): Promise<ProgrammingExerciseType | ParsonsPuzzleExerciseType | undefined> => {
  try {
    const response = await fetch(
      `/exercise?exercise_id=${exerciseID}&exercise_limit=1&exercise_details=true`,
      {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      }
    );
    if (!response.ok) {
      throw new Error(`HTTP Error ${response.status}`)
    }
    return await response.json().then((data) => data.data[0]);
  } catch (error) {
    throw new Error(error)
  }
};
