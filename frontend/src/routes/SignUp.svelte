<script>
  import Button from "@smui/button";
  import Card from "@smui/card/";
  import Textfield from "@smui/textfield";
  import HelperText from "@smui/textfield/helper-text";
  import PasswordInput from "../lib/components/Login/PasswordInput.svelte"
  import { userName, userIsAdmin, userLevel, userLoggedIn } from "../stores"
  import Page from "../lib/components/Page.svelte";
  
  let email = "";
  let emailRegEx = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;  
  let username = "";
  let password = "";
  let passwordRepeat = "";

  let userExists = false;
  let incorrectRepetition = false;
  let incorrectEmail = false;
  let passwordTooShort = true;
  let noInput = true;

  // reactive statements
  $: if (password != passwordRepeat){
    incorrectRepetition = true
  }
  else{
    incorrectRepetition = false
  }

  $: if (emailRegEx.test(String(email).toLowerCase())){
    incorrectEmail = false
  }
  else{
    incorrectEmail = !(email=="")
  }

  $: if (password.length < 1 || username.length <1 || email.length < 1){
    noInput = true
  }
  else{
    noInput = false
  }

  $: if (password.length >= 8){
    passwordTooShort = false
  }
  else{
    passwordTooShort = true
  }

  let disableSignUp = true
  $: if (!incorrectEmail && !incorrectRepetition && !passwordTooShort && !noInput){
    disableSignUp = false
  }
  else{
    disableSignUp = true
  }

  const signup = async () => {
    await fetch("http://127.0.0.1:5000/api/user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_name: email,
        user_pass: password,
        user_mail: email,
        user_admin: false
      }),
    }).then((response) => {
      if (response.status == 200) {
        response.json().then((data) => {
          // TODO: Save Cookie with jwt token

          // Save user info in local storage
          $userLoggedIn = true;
          $userName = email;
          $userIsAdmin = true;
          $userLevel = 9000;
          window.location.replace("..#/profile");
        });
      } else if (response.status == 401) {
        console.log("Sign Up failed")
        document.getElementById("email-input").focus()
      } else {
        // TODO: Handle exceptions
      }
    });
  };


</script>

<div class="login-card-container">
    <Page>
      <Card variant="outlined">

        <form class="login-form">
            <Textfield
                invalid={userExists}
                id="username-input"
                style="width: 100%"
                bind:value={email}
                label="E-Mail"
                variant="outlined"
            >
                <HelperText slot="helper">
                    {#if incorrectEmail}
                        Make sure to enter a valid e-Mail address.
                    {/if}
                </HelperText>
            </Textfield>
            <Textfield
                invalid={userExists}
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
            <PasswordInput bind:password label="Enter your Password">
            </PasswordInput>
            <PasswordInput bind:password={passwordRepeat} wrongRepition={incorrectRepetition} wrongPassword={incorrectRepetition} label="Repeat your Password" style="width: 100%"/>
        </form>

        <Button
          class="login-button"
          type="submit"
          variant="unelevated"
          disabled={disableSignUp}>
            Sign Up now
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
  