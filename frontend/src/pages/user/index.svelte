<script>
  import Page from "../../lib/Common/Page.svelte";
  import Card from "@smui/card";
  //import LanguageCard from "../../lib/Common/LanguageCard.svelte";
  import ExerciseSvg from "../../lib/AnimatedSVG/ExerciseSVG.svelte";
  import { userName } from "../../stores";
  import { userID } from "../../stores";
  import SolutionsSvg from "../../lib/AnimatedSVG/SolutionsSVG.svelte";

  //display exercise progress
  let totalExercises;
  let solvedExercises;
  let reqMeta;
  let userProgress;
  let r = document.querySelector(":root");
  let noCorrectExercise;
  let statsLoaded = false;

  const getTotalExercises = async () => {
    fetch(`/exercise`, {
      method: "GET",
    }).then((response) => {
      if (response.status === 200) {
        response.json().then((data) => {
          statsLoaded = false;
          reqMeta = Object.values(data);
          totalExercises = reqMeta[1].total;
          getSolvedExercises(); 
        });
      }else if(response.status === 204){
        console.log("No exercises in database yet. Error: " + response.status);
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
          reqMeta= Object.values(data);
          solvedExercises = reqMeta[1].total
          setTotalExercises();
          setSolvedExercises();
          setUserProgress();
          statsLoaded = true;
        });
      } else if (response.status === 204){
        //case: no correct solved exercises by user
        statsLoaded = false;
        noCorrectExercise = true;
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

  getTotalExercises();
</script>

<Page slideTransition={true}>
  <div class="grid-container-outside">
    <!--  Header -->
    <div class="header-outside">
      <h2 style="padding: 20px; font-family: monospace;">
        Welcome to your dashboard, {$userName}!
      </h2>
      <p style="padding: 0px 20px; font-family: monospace;">Get started with solving some exercises!</p>
    </div>

    <!--  Menu -->
    <div class="menu-outside" />

    <!--  Main -->
    <div class="main-outside">
      <div class="grid-container-inside">
        <div class="left-inside">
          <a href="/#/admin/view_exercises">
            <!-- <LanguageCard
            title="list all exercises">
              <ExerciseSvg />
            </LanguageCard> -->
            <!-- replace Card with languageCard, if it's modified to display diffrent width -->
            <Card>
              <ExerciseSvg />
            </Card>
            <div class="label">list all exercises</div>
          </a>
        </div>

        <div class="right-inside">
          <a href="/#/user/my_solutions">
            <!-- <LanguageCard
            title="list my solutions">
              <SolutionsSvg/>
            </LanguageCard> -->
            <!-- replace Card with languageCard, if it's modified to display diffrent width -->
            <Card>
              <SolutionsSvg/>
            </Card>
            <div class="label">list my solutions</div>
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
            <div class="progress total">{userProgress}% </div>
          </div>
        {/if}
        {#if noCorrectExercise}
        <p>Haven't solved any exercises correctly (yet). :(</p>
        {/if}
      </div>
    </div>

    <!--  Footer -->
    <div class="footer-outside" />
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
  // .name {width: percentage; background-color:var(--mdc-theme-primary);}

  // grid

  .header-outside {
    grid-area: header;
    height: fit-content;
  }

  .menu-outside {
    grid-area: menu;
  }
  .main-outside {
    width: fit-content;
    align-content: center;
    grid-area: main;
  }
  .right-outside {
    width: auto;
    align-content: center;
    grid-area: right;
    padding: 15px;
  }

  .footer-outside {
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
  }

  .grid-container-outside > div {
    background-color:rgba(190, 190, 170, 0.1);
    font-size: 30px;
    width: 100%;
    font-family: monospace;
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
    grid-template-areas: "left right";
    gap: 10px;
    background-color: transparent;
    padding: 10px;
  }

  .grid-container-inside > div {
    background-color: transparent;
  }

  .label {
    font-size: 16pt;
    padding: 5px;
  }

</style>
