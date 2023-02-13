<!-- Sign Up component that provides email format and password length checking -->

<script>
  import Button from "@smui/button";
  import Textfield from "@smui/textfield";
  import HelperText from "@smui/textfield/helper-text";
  import PasswordInput from "./PasswordInput.svelte";
  import { passwordLength } from "../constants";
  import { login } from "./user";

  let email = "";
  let emailRegEx =
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  let username = "";
  let password = "";
  let passwordRepetition = "";

  let userExists = false;

  function checkData() {
    if (password.length < passwordLength) {
      return false;
    } else if (password != passwordRepetition) {
      return false;
    } else if (!checkMail()) {
      return false;
    }
    return true;
  }

  const signup = async () => {
    if (!checkData()) {
      alert("incorrect data");
      return;
    }
    await fetch("/user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_name: username,
        user_pass: password,
        user_mail: email,
      }),
    }).then((response) => {
      if (response.status == 201) {
        login(email, password);
      } else if (response.status == 401) {
        document.getElementById("email-input").focus();
        alert("Sign Up failed");
      } else if (response.status == 409) {
        userExists = true;
        document.getElementById("email-input").focus();
        alert("Username is already taken.");
      } else if (response.status == 500) {
        alert("Oops an Error occured. Please try again.");
      } else {
        alert("Oops an Error occured. " + response.status);
      }
    });
  };

  let wrongMailFlag = false;
  function checkMail() {
    if (emailRegEx.test(String(email).toLowerCase())) {
      wrongMailFlag = false;
      return true;
    } else {
      wrongMailFlag = true;
      return false;
    }
  }

  let incorrectRepetition = false;
  function checkRepetition() {
    if (password == passwordRepetition) {
      incorrectRepetition = false;
    } else {
      incorrectRepetition = true;
    }
  }

  let passwordTooShort = false;
  function checkPWlength() {
    if (password.length < 8) {
      passwordTooShort = true;
    } else {
      passwordTooShort = false;
    }
  }
</script>

<form class="signup-form">
  <div class="input">
    <Textfield
      on:blur={checkMail}
      invalid={wrongMailFlag || userExists}
      id="email-input"
      style="width: 20rem"
      bind:value={email}
      label="E-Mail"
      variant="outlined"
    >
      <HelperText slot="helper" persistent>
        {#if wrongMailFlag}
          Please enter a valid E Mail address.
        {/if}
        {#if userExists}
          An account with this E Mail has already been created. <a
            href="/forgot-password">Forgot Password?</a
          >
        {/if}
      </HelperText>
    </Textfield>
  </div>

  <div class="input">
    <Textfield
      id="username-input"
      style="width: 20rem"
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
  </div>
  <div class="input">
    <PasswordInput
      bind:password
      label="Enter your Password"
      inputHandler={checkPWlength}
      wrongPassword={passwordTooShort}
      helperText="Password needs at least 8 characters."
      style="width: 20rem"
    />
  </div>
  <div class="input">
    <PasswordInput
      bind:password={passwordRepetition}
      label="Repeat your Password"
      inputHandler={checkRepetition}
      wrongPassword={incorrectRepetition}
      helperText="The Repetition does not match."
      style="width: 20rem"
    />
  </div>
</form>

<Button type="submit" variant="unelevated" on:click={signup}>
  Sign Up now
</Button>

<style>
  .signup-form {
    margin: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
  }
  .input {
    padding: 0.2rem;
  }
</style>