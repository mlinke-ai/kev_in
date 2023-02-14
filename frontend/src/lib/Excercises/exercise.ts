function getCurrentTimestamp() {
  return (Date.now() / 1000)
}

export const getExercise = async (exerciseID) => {
  fetch(
    `/exercise?exercise_id=${exerciseID}&exercise_details=true`,
    {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    }
  ).then(response => {
    if (response.status === 401) {
      // redirect to login
      window.location.replace("/");
    } else if (response.status === 403) {
      alert("No admin rights")
    } else if (response.status === 400) {
      alert("user_limit out of range")
    } else if (response.status === 200) {
      response.json().then(data => {
        return data.json();
      })
    }
  })
}

export const submitSolution = async (exerciseID, elapsedTime, solutionContent) => {
  fetch(
    "/solution",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        solution_exercise: exerciseID,
        solution_date: getCurrentTimestamp(),
        solution_duration: elapsedTime,
        solution_content: solutionContent
      })
    }
  ).then(response => {
    if (response.status === 400) {
      alert("A required argument was not sent");
    }
    else if (response.status === 401) {
      // redirect to login
      window.location.replace("/#/login");
    } else if (response.status === 403) {
      alert("you naughty naughty")
    } else if (response.status === 200) {
      alert("Successfully submitted solution")
      response.json().then(data => {
        console.log(data);
      })
    }
  })
}
