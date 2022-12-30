<script>
  import Button from "@smui/button";
  import Card from "@smui/card/";
  import Textfield from "@smui/textfield";
  import PasswordInput from "./PasswordInput.svelte";
  import Tab, { Label as TLabel } from "@smui/tab";
  import TabBar from "@smui/tab-bar";
  import Select, { Option } from "@smui/select";
  import { accessLevel, userName, userLevel } from "../../../stores";
  import { accessLevels } from "../../types";

  let email = "";
  let password = "";

  let wrongCredentials = false;

  let active = "Kev.In Account";
  let idProviders = ["TU Chemnitz", "WH Zwickau"];
  let value = "TU Chemnitz";

  const login = async () => {
    await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_name: email,
        user_pass: password,
      }),
    }).then((response) => {
      if (response.status == 200) {
        response.json().then((data) => {
          // TODO: Save Cookie with jwt token

          // Save user info in local storage
          $accessLevel = accessLevels.admin;
          $userName = email;
          $userLevel = 9000;
          window.location.replace("..#/profile");
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
    <TabBar tabs={["Kev.In Account Login"]} let:tab bind:active>
      <!--"University Login"-->
      <Tab style={"cursor: default"} disabled {tab}>
        <TLabel>{tab}</TLabel>
      </Tab>
    </TabBar>

    {#if active == "University Login"}
      <div class="idp-select-menu">
        <Select style="width: 90%" bind:value label="Select ID Provider">
          {#each idProviders as idps}
            <Option value={idps}>{idps}</Option>
          {/each}
        </Select>
      </div>
    {:else}
      <form
        class="login-form"
        on:submit|preventDefault={login}
        hidden
      >
        <div class="input-email">
          <Textfield
            invalid={wrongCredentials}
            id="email-input"
            style="width: 20rem"
            bind:value={email}
            label="Email"
            variant="outlined"
          />
        </div>
        <div class="input-password">
          <PasswordInput bind:password wrongPassword={wrongCredentials} />
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
  .input-email {
    padding: 0.2rem;
  }
  .input-password {
    padding: 0.2rem;
  }

  .login-card-container {
    width: 25rem;
    margin: auto;
  }

  .idp-select-menu {
    position: relative;
    margin: 1rem 1rem 7.7rem 1rem;
    width: 100%;
  }
</style>
