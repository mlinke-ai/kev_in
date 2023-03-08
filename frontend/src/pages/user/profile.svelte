<script lang="ts">
  import Page from "../../lib/Common/Page.svelte";
  import Card from "@smui/card/src/Card.svelte";
  import Button from "@smui/button/src/Button.svelte";
  import { startPage } from "../../stores";
  import UserSvg from "../../lib/AnimatedSVG/UserSVG.svelte";
  import {
    userID as uID,
    userName as uname,
    userMail as umail,
  } from "../../stores";
  import { getUser } from "../../lib/Authentication/user";
  import type { GetUser } from "../../lib/Authentication/types";
  import { getExercisesWithArgs } from "../../lib/Excercises/exercise";
  //import { getSolutionsWithArgs } from "../../lib/Excercises/solution";
  import { link } from "svelte-spa-router";

  export let userID: number = undefined;
  let userName: string;
  let userMail: string;

  async function setUserData() {
    let userData: GetUser;
    userData = (await getUser({ user_id: userID })).data[0];
    userName = userData.user_name;
    userMail = userData.user_mail;
  }

  if (userID) {
    setUserData();
  } else {
    userID = $uID;
    userName = $uname;
    userMail = $umail;
  }

  let statsLoaded = false;
  let solvedExercises = 30;
  let totalExercises = 74;
  let userProgress;
  let requiredData;
  let correct = true;
  let r = document.querySelector(":root");

  function getStats() {
    getTotalExercises();
    getSolvedExercises();
    displayStats();
  }

  async function getTotalExercises() {
    requiredData = (await getExercisesWithArgs({})).meta;
    console.log(requiredData);
    totalExercises = requiredData.total;
    console.log(totalExercises);
  }

  // async function getSolvedExercises() {
  //   requiredData = (await getSolutionsWithArgs({solution_user: userID, solution_correct: correct}));
  //   console.log(requiredData);
  //   solvedExercises = requiredData.meta.total;
  //   console.log(solvedExercises);
  // }
  //to use this function, getSolutionWithArgs needs proper errorhandling

  const getSolvedExercises = async () => {
    fetch(`/solution?solution_user=${userID}&solution_correct=true`, {
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          statsLoaded = false;
          console.log(data);
          requiredData = Object.values(data);
          solvedExercises = requiredData[1].total;
          setTotalExercises();
          setSolvedExercises();
          setUserProgress();
          statsLoaded = true;
        });
      } else if (response.status === 204) {
        //no correct solved exercises by new user
        statsLoaded = false;
        solvedExercises = 0;
        setTotalExercises();
        setSolvedExercises();
        setUserProgress();
        statsLoaded = true;
      } else {
        alert("Oops an Error occured. " + response.status);
      }
    });
  };

  function displayStats() {
    setUserProgress();
    setSolvedExercises();
    setTotalExercises();
    statsLoaded = true;
  }

  function setUserProgress() {
    userProgress = Math.floor((solvedExercises / totalExercises) * 100);
    console.log(solvedExercises);
    //@ts-ignore
    r.style.setProperty("--userProgress", userProgress + "%");
  }

  function setTotalExercises() {
    //@ts-ignore
    r.style.setProperty("--totalExercises", totalExercises + "px");
  }

  function setSolvedExercises() {
    //@ts-ignore
    r.style.setProperty("--solvedExercises", solvedExercises + "px");
  }

  getStats();
</script>

<Page>
  <div class="grid-container">
    <div class="profile-pic">
      <Card>
        <UserSvg />
      </Card>
    </div>

    <div class="user-data">
      <p>Name: {userName}</p>
      <p>E-Mail: {userMail}</p>
    </div>

    <div class="user-stats">
      <div class="box">
        {#if statsLoaded}
          <b>Solved Exercises:</b>
          {solvedExercises} out of {totalExercises}

          <p>Progress</p>
          <div class="container">
            <div class="progress total">{userProgress}%</div>
          </div>
        {/if}
      </div>
    </div>
  </div>

  <a use:link href={$startPage}>
    <Button>Back to dashboard</Button>
  </a>
</Page>

<style lang="scss">
  //stats-bar
  :root {
    --userProgress: 5%;
    --solvedExercises: 5px;
    --totalExercises: 100px;
  }

  * {
    box-sizing: border-box;
  }

  .container {
    width: 100%;
    background-color: var(--mdc-theme-surface);
  }

  .progress {
    text-align: right;
    padding-top: 10px;
    padding-bottom: 10px;
    color: white;
  }

  .total {
    width: var(--userProgress);
    background-color: var(--mdc-theme-primary);
  }

  //muster for further progress bars
  // .name {width: percentage; background-color: rgba(0,20,17,1);}

  //grid
  .grid-container {
    display: grid;
    grid-template-areas:
      "left right right right"
      "footer footer footer footer";
    background-color: transparent;
    gap: 10px;
  }

  .grid-container > div {
    background-color: transparent;
    padding: 10px;
  }

  .profile-pic {
    background-color: rgb(0, 57, 49);
    width: 350px;
    grid-area: left;
  }

  .user-data {
    font-size: 24pt;
    font-family: monospace;
    grid-area: right;
    width: 100%;
  }

  .user-stats {
    font-size: 24pt;
    font-family: monospace;
    width: 100%;
    grid-area: footer;
  }
</style>
