<script lang="ts">
  import Page from "../../lib/Common/Page.svelte";
  import Menu from "@smui/menu";
  import List, { Item, Separator, Text } from "@smui/list";
  import Card from "@smui/card";
  //import LanguageCard from "../../lib/Common/LanguageCard.svelte";
  import Button, { Label, Icon } from "@smui/button";
  import GroupSvg from "../../lib/AnimatedSVG/GroupSVG.svelte";
  import ExerciseSvg from "../../lib/AnimatedSVG/ExerciseSVG.svelte";
  import { userName } from "../../stores";
  import { userID } from "../../stores";
  import Tooltip, { Wrapper } from "@smui/tooltip";

  //display exercise progress
  let reqMeta;
  let totalExercises = 100;
  let solvedExercises = 50;
  let userProgress;
  let r = document.querySelector(":root");
  let statsLoaded = false;

  const getTotalExercises = async () => {
    fetch(`/exercise`, {
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          statsLoaded = false;
          console.log(data);
          reqMeta = Object.values(data);
          totalExercises = reqMeta[1].total;
          getSolvedExercises();
        });
      }else if(response.status === 204){
        console.log(
          "No exercises in database. Please create some. Error: " +
            response.status
        );
      } else {
        alert("Oops an Error occured. " + response.status);
      }
    });
  };

  const getSolvedExercises = async () => {
    fetch(`/solution?solution_user=${$userID}&solution_correct=true`, {
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          statsLoaded = false;
          console.log(data);
          reqMeta = Object.values(data);
          solvedExercises = reqMeta[1].total;
          setTotalExercises();
          setSolvedExercises();
          setUserProgress();
          statsLoaded = true;
        });
      } else if (response.status === 204){
        //no correct solved exercises by user
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

  function setUserProgress() {
    userProgress = Math.floor((solvedExercises / totalExercises) * 100);
    console.log(solvedExercises);
    // @ts-ignore
    r.style.setProperty("--userProgress", userProgress + "%");
  }

  function setTotalExercises() {
    // @ts-ignore
    r.style.setProperty("--totalExercises", totalExercises + "px");
  }

  function setSolvedExercises() {
    // @ts-ignore
    r.style.setProperty("--solvedExercises", solvedExercises + "px");
  }

  getTotalExercises();

  let menu: Menu;
</script>

<Page title="Admin - Dashboard" slideTransition={true}>
  <div class="grid-container-outside">
    <!--  Header -->
    <div class="header-outside">
      <h2 style="padding: 20px 20px 0px 20px; font-family: monospace;">
        Welcome to your dashboard, {$userName}!
      </h2>
      <p style="padding: 0px 20px; font-family: monospace;">What do you want to do?</p>
    </div>

    <!--  Menu -->
    <div class="menu-outside" />

    <!--  Main -->
    <div class="main-outside">
      <div class="grid-container-inside">
        <div class="left-inside">
          <a href="/#/admin/view_users">
            <!-- <LanguageCard
            title=".list all users">
              <GroupSvg />
            </LanguageCard> -->
            <!-- replace Card with languageCard, if it's modified to display diffrent width -->
            <Card>
              <GroupSvg />
            </Card>
            <div class="label">list all users</div>
          </a>
        </div>

        <div class="right-inside">
          <a href="/#/admin/view_exercises">
            <!-- <LanguageCard
            title=".list all exercises">
              <ExerciseSvg />
            </LanguageCard> -->
            <!-- replace Card with languageCard, if it's modified to display diffrent width -->
            <Card>
              <ExerciseSvg />
            </Card>
            <div class="label">list all exercises</div>
          </a>
        </div>
      </div>
    </div>

    <!--  Right -->
    <div class="right-outside">
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

    <!--  Footer -->
    <div class="footer-outside">
      <div class="add-exercise">
        <Card>
          <div class="pointer" on:mousedown={() => menu.setOpen(true)}>
            <div class="display-button-menu">
              <div class="display-icon">
                <Icon class="material-icons">library_add</Icon>
              </div>
              <div class="label-icon">add exercise</div>
            </div>
          </div>

          <Menu bind:this={menu}>
            <List style="width: fit-content">
              <a href="/exercises/create/parsonspuzzle">
                <Item class="add-exercise-item">
                  <Icon class="material-icons add-exercise-item-icon"
                    >extension</Icon
                  >
                  <p style="width: 175px; padding-left: 10px;">Parsons Puzzle</p>
                </Item>
              </a>
              <Wrapper>
                <Item class="add-exercise-item" disabled>
                  <Icon class="material-icons add-exercise-item-icon"
                    >border_color</Icon
                  >
                  <p style="width: 175px;  padding-left: 10px;">
                    Fill in the Blanks
                  </p>
                </Item>
                <Tooltip style="z-index: 999;">Coming Soon!</Tooltip>
              </Wrapper>
              <a href="/exercises/create/programming">
                <Item class="add-exercise-item">
                  <Icon class="material-icons add-exercise-item-icon">code</Icon
                  >
                  <p style="width: 175px;  padding-left: 10px;">
                    Free Coding Exercise
                  </p>
                </Item>
              </a>
            </List>
          </Menu>
        </Card>
      </div>

      <div class="add-user">
        <Card>
          <a href="#/admin/add_user">
             <!-- please insert link to create a new user here -->
            <div class="display-button">
              <div class="display-icon">
                <Icon class="material-icons">library_add</Icon>
              </div>
              <div class="label-icon">add user</div>
            </div>
          </a>
        </Card>
      </div>

      <div class="own-solutions">
        <Card>
          <a href="/#/admin/view_solutions">
            <div class="display-button">
              <div class="display-icon">
                <Icon class="material-icons">fact_check</Icon>
              </div>
              <div class="label-icon">Show all solutions</div>
            </div>
          </a>
        </Card>
      </div>
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
    background-color: var(--mdc-theme-surface);
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
    background-color: var(--mdc-theme-primary);
  }
  //muster for further progress bars
  // .name {width: percentage; background-color: rgba(0,20,17,1);}

  // grid

  .header-outside {
    grid-area: header;
    font-family: monospace;
  }

  .menu-outside {
    grid-area: menu;
  }

  .main-outside {
   
    align-content: center;
    grid-area: main;
  }

  .right-outside {
    
    align-content: center;
    grid-area: right;
    padding: 15px;
    display: flex;
  }

  .footer-outside {
    display: flex;
    gap: 10px;
    align-content: center;
    padding: 20px;
    grid-area: footer;
  }

  .grid-container-outside {
    display: flex;
    display: grid;
    grid-template-areas:
      "header header header header"
      "main main right right"
      "footer footer footer footer";
    gap: 10px;
    background-color: transparent;
    padding: 10px;
  }

  .grid-container-outside > div {
    background-color: rgba(190, 190, 170, 0.1);
    font-family: monospace;
    font-size: 30px;
  }

  .left-inside {
    width: 350px;
    //rm if languagecard has been modified
    padding: 10px;
    align-content: center;
    grid-area: left;
  }

  .right-inside {
    width: 350px;
    //rm if languagecard has been modified
    padding: 10px;
    align-content: center;
    grid-area: right;
  }

  .grid-container-inside {
    display: grid;
    display: flex;
    grid-template-areas: "left right";
    background-color: transparent;
  }

  .grid-container-inside > div {
    background-color: transparent;
    font-size: 30px;
  }

  .label {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
      Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue",
      sans-serif;
    align-self: center;
    padding: 5px;
  }

  .label-icon {
    float: left;
    color: #5382a1;
    font-size: 18pt;
    font-family: monospace;
    text-transform: uppercase;
    text-align: center;
    padding: 5px 15px 0px 0px;
  }

  .display-icon {
    color: #5382a1;
    float: left;
    width: 50px;
    height: 50px;
    margin-left: 10px;
  }

  .display-button {
    width: fit-content;
    margin: 10px;
  }

  .display-button-menu {
    width: fit-content;
    margin: 10px;
  }

  .pointer {
    cursor: pointer;
  }

  .add-exercise {
    width: fit-content;
    float: right;
    align-items: center;
  }

  .add-user {
    width: fit-content;
    float: right;
    align-items: center;
  }

  .own-solutions {
    width: fit-content;
    float: right;
    align-items: center;
  }

</style>