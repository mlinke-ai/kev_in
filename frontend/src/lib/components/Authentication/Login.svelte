<script>
  import Button from "@smui/button";
  import Textfield from "@smui/textfield";
  import PasswordInput from "./PasswordInput.svelte";
  import { accessLevel, userName, startPage } from "../../../stores";
  import { accessLevels } from "../../types";
  import { getUserData, setupUserSettings } from "../../functions/user";

  let email = "";
  let password = "";

  let wrongCredentials = false;

  const login = async () => {
    await fetch("/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_name: email,
        user_pass: password,
      }),
    }).then((response) => {
      if (response.status == 200) {
        response.json().then((data) => {
          getUserData();
          setupUserSettings();
        });
      } else if (response.status == 401) {
        wrongCredentials = true;
        console.log("Login failed");
        document.getElementById("email-input").focus();
      } else {
        // TODO: Handle exceptions
      }
    });
  };
</script>

<form class="login-form" on:submit|preventDefault={login} hidden>
  <div class="input">
    <Textfield
      invalid={wrongCredentials}
      id="email-input"
      style="width: 20rem"
      bind:value={email}
      label="Email"
      variant="outlined"
    />
  </div>
  <div class="input" style="margin-top: 1rem;">
    <PasswordInput
      bind:password
      wrongPassword={wrongCredentials}
      style="width: 20rem"
    />
  </div>
</form>
<Button class="login-button" on:click={login} type="submit" variant="unelevated"
  >Login</Button
>

<style>
  .login-form {
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
