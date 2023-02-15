<script>
  import Page from "../lib/common/Page.svelte";
  import Card, {
    Content,
    PrimaryAction,
    Media,
    MediaContent,
    Actions,
    ActionButtons,
    ActionIcons,
  } from "@smui/card";
  import Button, { Label, Icon } from "@smui/button";
  import GroupSvg from "../lib/AnimatedSVG/GroupSVG.svelte";
  import ExerciseSvg from "../lib/AnimatedSVG/ExerciseSVG.svelte";
  import { accessLevels } from "../lib/constants";
  import { userName } from "../stores";
  import { userID } from "../stores";

  //display exercise progress
  let totalExercises = 100;
  let solvedExercises = 50;
  console.log(solvedExercises);
  let userProgress;
  //let userProgress = (solvedExercises / totalExercises);
  let r = document.querySelector(":root");
  let statsLoaded = false;

  // function myFunction_get() {
  //   let rs = getComputedStyle(r);
  //   alert("The value of --blue is: " + rs.getPropertyValue("--userProgress"));
  // }

  const getTotalExercises = async () => {
    fetch(`/exercise`, {
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          statsLoaded = false;
          console.log(data);
          totalExercises = Object.values(data).length;
          console.log(solvedExercises);
          console.log(totalExercises);
          getSolvedExercises(); 
          //following function calls might be removed if this is activated
          // setTotalExercises();
          // setSolvedExercises();
          // setUserProgress();
          //statsLoaded = true;
        });
      } else {
        alert("Oops an Error occured. " + response.status);
      }
    });
  };

  const getSolvedExercises = async () => {
    fetch(`/solution?solution_user=${$userID}&solution_correct=true`, {
      //?solution_user=${$userID}&solution_correct=true
      //to get the number of all correct solutions of the user with id ${me}
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          statsLoaded = false;
          console.log(data);
          solvedExercises = Object.values(data).length;
          setTotalExercises();
          setSolvedExercises();
          setUserProgress();
          statsLoaded = true;
        });
      } else {
        alert("Oops an Error occured. " + response.status);
      }
    });
  };
  //responses error 500??

  function setUserProgress() {
    userProgress = Math.floor((solvedExercises / totalExercises) * 100);
    console.log(solvedExercises);
    r.style.setProperty("--userProgress", userProgress + "%");
  }

  function setTotalExercises() {
    r.style.setProperty("--totalExercises", totalExercises + "px");
  }

  function setSolvedExercises() {
    //solvedExercises = Math.floor(totalExercises / 3);
    //just for testcases, remove if getSolvedExercises() works properly
    r.style.setProperty("--solvedExercises", solvedExercises + "px");
  }

  getTotalExercises();
  //getSolvedExercises();
</script>

<Page requiredAccessLevel={accessLevels.admin}>
  <div class="grid-container-outside">
    <!--  Header -->
    <div class="header-outside">
      <h2 style="padding: 20px; font-family: monospace;">
        Welcome to your dashboard, {$userName}!
      </h2>
    </div>

    <!--  Menu -->
    <div class="menu-outside" />

    <!--  Main -->
    <div class="main-outside">
      <div class="grid-container-inside">
        <div class="left-inside">
          <a href="/#/users">
            <Card>
              <GroupSvg />
            </Card>
            <div class="label">List all users</div>
          </a>
        </div>

        <div class="right-inside">
          <a href="/#/exercises">
            <Card>
              <ExerciseSvg />
            </Card>
            <div class="label">List all exercises</div>
          </a>
        </div>
      </div>
    </div>

    <!--  Right -->
    <div class="right-outside">
      <div class="box">
        <h4>Solved Exercieses:</h4>
        {#if statsLoaded}
          <p>{solvedExercises} out of {totalExercises}</p>

          <p>Total</p>
          <div class="container">
            <div class="progress total">{userProgress}% </div>
          </div>
        {/if}
      </div>
    </div>

    <!--  Footer -->
    <div class="footer-outside">
      <a href="/#/solutions">
        <Icon>
          inventory_outlined
        </Icon>
      Show my own solutions
      </a>
    </div>
  </div>
</Page>

<style lang="scss">
  /* progress-bar */

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
    background-color: rgba(0,20,17,1);
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

  // grid

  .header-outside {
    grid-area: header;
    width: auto;
    height: fit-content;
  }

  .menu-outside {
    grid-area: menu;
  }
  .main-outside {
    display: flex;
    width: fit-content;
    align-content: center;
    grid-area: main;
  }
  .right-outside {
    width: auto;
    align-content: center;
    grid-area: right;
    padding: 15px;
    display: flex;
  }

  .footer-outside {
    align-content: center;
    height: fit-content;
    padding: 20px;
    grid-area: footer;
  }

  .grid-container-outside {
    display: grid;
    grid-template-areas:
      "header header header"
      "main right right"
      "footer footer footer";
    gap: 10px;
    background-color: transparent;
    padding: 10px;
  }

  .grid-container-outside > div {
    background-color: rgb(0, 57, 49);
    font-size: 30px;
    width: 100%;
    display: flex;
  }

  .left-inside {
    width: 300px;
    height: auto;
    align-content: center;
    grid-area: left;
  }

  .right-inside {
    width: 300px;
    height: auto;
    align-content: center;
    grid-area: right;
  }

  .grid-container-inside {
    display: grid;
    grid-template-areas: "left right";
    gap: 10px;
    background-color: transparent;
    padding: 10px;
  }

  .grid-container-inside > div {
    background-color: rgb(0, 57, 49);
    font-size: 30px;
  }

  .label {
    align-content: center;
    padding: 5px;
  }

  /* // .box{
  //   width: 3fr;
  // } */
</style>
