<script lang="ts">
  import Page from "../../lib/Common/Page.svelte";
  import Card from "@smui/card/src/Card.svelte";
  import UserSvg from "../../lib/AnimatedSVG/UserSVG.svelte";
  import { userID as uID, userName as uname, userMail as umail } from "../../stores";
  import { getUser } from "../../lib/Authentication/user";
  import type { GetUser } from "../../lib/Authentication/types";

  export let userID: number = undefined;
  let userName: string;
  let userMail: string;

  async function setUserData() {
    let userData: GetUser;
    userData = (await getUser({user_id: userID})).data[0];
    userName = userData.user_name;
    userMail = userData.user_mail;
  }

  if (userID){
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
  let r = document.querySelector(":root");

  function displayStats() {
    setUserProgress();
    setSolvedExercises();
    setTotalExercises();
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

  displayStats();
</script>

<Page>
  <div class="grid-container">
    <div class="profile-pic">
      <Card>
        <UserSvg />
      </Card>
    </div>

    <div class="user-data">
      Name: {userName}<br />
      E-Mail: {userMail}
    </div>

    <div class="user-stats">
      <div class="box">
        <h4>Solved Exercises:</h4>
        {#if statsLoaded}
          <p>{solvedExercises} out of {totalExercises}</p>

          <p>Total</p>
          <div class="container">
            <div class="progress total">{userProgress}%</div>
          </div>
        {/if}
      </div>
    </div>
  </div>
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
    background-color: rgba(0, 20, 17, 1);
    //rgba(0,20,17,1)
  }

  .progress {
    text-align: right;
    padding-top: 10px;
    padding-bottom: 10px;
    color: white;
  }

  .total {
    width: var(--userProgress);
    background-color: #005f50;
  }

  //muster for further progress bars
  // .name {width: percentage; background-color: rgba(0,20,17,1);}

  //grid
  .grid-container {
    display: grid;
    display: flex;
    grid-template-areas:
      "left right right"
      "main main main";
    background-color: rgb(0, 57, 49);
    gap: 10px;
  }

  .profile-pic {
    grid-area: left;
  }

  .user-data {
    font-size: 24pt;
    font-family: monospace;
    grid-area: right;
  }

  .user-stats {
    grid-area: main;
  }
</style>
