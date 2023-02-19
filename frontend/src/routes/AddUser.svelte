<script>
  import Button from "@smui/button";
  import Card from "@smui/card/";
  import Textfield from "@smui/textfield";
  import HelperText from "@smui/textfield/helper-text";
  import PasswordInput from "../lib/Authentication/PasswordInput.svelte";
  import { userName, userMail, accessLevel } from "../stores"
  import Page from "../lib/common/Page.svelte";
  import { push } from "svelte-spa-router";
  import { accessLevels, passwordLength } from "../lib/common/types"
  
  let email = "";
  let emailRegEx = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;  
  let username = "";
  let password = "";
  let passwordRepetition = "";

  let userExists = false;
   
  function checkData(){
    if (password.length < passwordLength){
      return false
    }
    else if(password != passwordRepetition){
      return false
    }
    else if (!checkMail()){
      return false
    }
    return true
  }
  
  const signup = async () => {
    if (!checkData()){
      alert("incorrect data");
      return
    }
    await fetch("http://127.0.0.1:5000/user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_name: username,
        user_pass: password,
        user_mail: email,
        user_admin: false
      }),
    }).then((response) => {
      if (response.status == 201) {
        window.location.replace("..#/users");
      } else if (response.status == 401) {
        document.getElementById("email-input").focus()
        alert("Sign Up failed")
      } else if (response.status == 409) {
        userExists = true
        document.getElementById("email-input").focus()
        alert("Username is already taken.")
      } else if (response.status == 500){
        alert("Oops an Error occured. Please try again.")
      } else {
        alert("Oops an Error occured. " + response.status)
      }
    });
  };

  let wrongMailFlag = false;
  function checkMail(){
    if (emailRegEx.test(String(email).toLowerCase())){
      wrongMailFlag = false;
      return true;
    }
    else{
      wrongMailFlag = true;
      return false;
    }
  }
  
  let incorrectRepetition = false;
  function checkRepetition(){
    if (password == passwordRepetition){
      incorrectRepetition = false
    }
    else{
      incorrectRepetition = true
    }
  }
  
  let passwordTooShort = false;
  function checkPWlength(){
    if (password.length < 8){
      passwordTooShort = true
    } else {
      passwordTooShort = false
    }
  }


</script>

<div class="login-card-container">
    <Page>
      <Card variant="outlined">

        <form class="login-form">
            <Textfield
                on:blur= {checkMail}
                invalid={wrongMailFlag||userExists}
                id="email-input"
                style="width: 100%"
                bind:value={email}
                label="E-Mail"
                variant="outlined"
                
            >
                <HelperText slot="helper" persistent>
                  {#if wrongMailFlag}
                    Please enter a valid E Mail address.
                  {/if}
                  {#if userExists}
                    An account with this E Mail has already been created. <a href="/forgot-password">Forgot Password?</a>
                  {/if}
                </HelperText>
            </Textfield>

            <Textfield
                id="username-input"
                style="width: 100%"
                bind:value={username}
                label="Username"
                variant="outlined"
            >
                <HelperText slot="helper">
                    {#if userExists}
                        User already exists.
                    {/if}
                </HelperText>
            </Textfield>

            <PasswordInput
                bind:password 
                label="Enter your Password" 
                inputHandler={checkPWlength} 
                wrongPassword={passwordTooShort} 
                helperText="Password needs at least 8 characters."/>
            <PasswordInput 
                bind:password={passwordRepetition} 
                label="Repeat your Password" 
                inputHandler={checkRepetition} 
                wrongPassword={incorrectRepetition} 
                helperText="The Repetition does not match." 
                style="width: 100%"/>
        </form>

        <Button
          class="login-button"
          type="submit"
          variant="unelevated"
          on:click= {signup}>
            Add This User
        </Button>
      </Card>
    </Page>
    
</div>

  
<style lang="css">
    .login-form {
      display: flex;
      flex-direction: column;
      gap: 1rem;
      margin-left: 1%;
      margin-right: 1%;
      padding: 5%;

    }
  
    .login-card-container {
      width: 40%;
      margin-left: auto;
      margin-right: auto;
    }
  
  </style>
  