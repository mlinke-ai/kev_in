<script>
  import Button from "@smui/button";
  import Card from "@smui/card/";
  import Textfield from "@smui/textfield";
  import PasswordInput from "./PasswordInput.svelte";
  import Tab, { Label as TLabel } from "@smui/tab";
  import TabBar from "@smui/tab-bar";
  import Select, { Option } from "@smui/select";
  import { accessLevel, userName, startPage } from "../../../stores";
  import { accessLevels } from "../../types";
  import { setupUserSettings } from "../../functions/user";
  import { replace as replaceRoute } from "svelte-spa-router";

  let username = "";
  let password = "";

  let wrongCredentials = false;

  let active = "Login";
  let value = "Login";

  const login = async () => {
    await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_name: username,
        user_pass: password,
      }),
    }).then((response) => {
      if (response.status == 200) {
        response.json().then((data) => {
          // TODO: Save Cookie with jwt token

          // Save user info in local storage
          $accessLevel = accessLevels.admin;
          setupUserSettings($accessLevel);
          $userName = username;
          $accessLevel = accessLevels.admin;
          replaceRoute($startPage);
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

<div class="login-card-container">
  <Card variant="outlined">
    <TabBar tabs={["Login", "Sign Up"]} let:tab bind:active>
      <Tab style={"cursor: default"} disabled {tab}>
        <TLabel>{tab}</TLabel>
      </Tab>
    </TabBar>

    {#if active == "Sign Up"}
      <div class="sign-up-form"></div>
    {:else}
      <form class="login-form" on:submit|preventDefault={login} hidden>
        <div class="input">
          <Textfield
            invalid={wrongCredentials}
            id="username-input"
            style="width: 20rem"
            bind:value={username}
            label="Username"
            variant="outlined"
          />
        </div>
        <div class="input" style="margin-top: 1rem;">
          <PasswordInput bind:password wrongPassword={wrongCredentials} style="width: 20rem"/>
        </div>
      </form>
    {/if}
    <Button
      class="login-button"
      on:click={login}
      type="submit"
      variant="unelevated">Login</Button
    >
  </Card>
</div>

<style lang="css">
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

  .login-card-container {
    width: 25rem;
    margin: auto;
  }
</style>
