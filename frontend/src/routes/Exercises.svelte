<script>
  import Page from "../lib/components/common/Page.svelte";
  import Button from "@smui/button/src/Button.svelte";
  import Card, {
    Content,
    PrimaryAction,
    Media,
    MediaContent,
    Actions,
    ActionButtons,
    ActionIcons,
  } from '@smui/card';
  import EditSvg from "../lib/components/AnimatedSVG/EditSVG.svelte";

  const exercises = [];
  let numExercises = 0;
  let currExercise = 1;

  const getNumExercises = async () => {
    await fetch("http://127.0.0.1:5000/exercise", {
      method: "GET",
    }).then((response) => {
      if (response.status == 200) {
        numExercises = this
      } else if (response.status == 401) {
        alert(this.message)
      } else if (response.status == 403) {
        alert(this.message)
      } else if (response.status == 500){
        alert("Oops an Error occured. Please try again.")
      } else {
        alert("Oops an Error occured. " + response.status)
      }
    });
  };

  const getExercises = async () => {
    await fetch("http://127.0.0.1:5000/exercise?exercise_id=currExercise", {
      method: "GET",
    }).then((response) => {
      if (response.status == 200) {
        exercises.push(this)
        currExercise++
      } else if (response.status == 401) {
        alert(this.message)
      } else if (response.status == 403) {
        alert(this.message)
      } else if (response.status == 500){
        alert("Oops an Error occured. Please try again.")
      } else {
        alert("Oops an Error occured. " + response.status)
      }
    });
  };


  import { mdiFormatColorFill, mdiWrench, mdiCurrencyUsd } from '@mdi/js';
  import IconButton, { Icon } from '@smui/icon-button';
  import { Svg } from '@smui/common';
 
  let clicked = 0;

</script>

<Page>
  <h1>Exercises</h1>

  <p>
    This is a placeholder site for listing all exercises.
  </p>

  <p>
    
  </p>

  <div class="grid-container">
    <div class="grid-item">
        <Card>
        Exercise 01
        <div style="display: flex; align-items: center;">
            <a href="/#/error">
            <IconButton>
              <Icon component={Svg} viewBox="0 0 24 24">
                <path fill="outlined" 
                d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34a.9959.9959 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" />
              </Icon>
            </IconButton>
        </a>
          </div>
        </Card>
    </div>
    <div class="grid-item">Exercise 02</div>
    <div class="grid-item">Exercise 03</div>
    <div class="grid-item">Exercise 04</div>
    <div class="grid-item">Exercise 05</div>
    <div class="grid-item">Exercise 06</div>
    <div class="grid-item">Exercise 07</div>
    <div class="grid-item">Exercise 08</div>
    <div class="grid-item">Exercise 09</div>
    <div class="grid-item">Exercise 10</div>
    <div class="grid-item">Exercise 11</div>
    <div class="grid-item">Exercise 12</div>
    <div class="grid-item">Exercise 13</div>
    <div class="grid-item">Exercise 14</div>
    <div class="grid-item">Exercise 15</div>
  </div>

  <a href="/#/admin-dashboard">
  <Button>
     Back to dashboard
  </Button>
</a>
</Page>

<style>
  .grid-container {
    display: grid;
    grid-template-columns: auto auto auto;
    background-color: rgb(0, 57, 49);;
    padding: 10px;
  }
  .grid-item {
    background-color: #001a16;
    border: 1px solid rgba(0, 0, 0, 0.8);
    padding: 20px;
    font-size: 30px;
    text-align: center;
  }
</style>
