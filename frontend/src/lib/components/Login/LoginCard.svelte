<script>
  import Button from "@smui/button";
  import Card from "@smui/card/";
  import Textfield from "@smui/textfield";
  import HelperText from "@smui/textfield/helper-text";
  import PasswordInput from "./PasswordInput.svelte";
  import Tab, { Label as TLabel } from "@smui/tab";
  import TabBar from "@smui/tab-bar";
  import Select, { Option } from "@smui/select";
  import { navigate } from "svelte-routing";
  import { userName, userIsAdmin, userLevel } from "../../../stores"

  let username = "";
  let password = "";

  let userNotFound = false;
  let wrongPassword = false;

  let active = "Kev.In Account";
  let idProviders = ["TU Chemnitz", "WH Zwickau"];
  let value = "TU Chemnitz";

  const login = async () => {
    await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_name: "sadmin",
        user_pass: "sadmin"//"9f5ba68f21489544d985797d58847b65e9a22c4981aeccafc96b351e84df254c",
      }),
    })
    .then((response) => {
      if (response.status == 200) {
        response.json().then((data) => {
          if (data.token) {
            console.log(data.token)
            
            // TODO: Save Cookie with jwt token

            // Save user info in local storage
            $userName = username
            $userIsAdmin = true
            $userLevel = 9000
            navigate("/dashboard", { replace: true })
          } else {
            console.log(data.message)
            wrongPassword = true
            userNotFound = true
          }
        })
      } else if (response.status == 401){
        // TODO: Shift wrong creds code here
      } else {
        // TODO: Handle exceptions
      }
      })
  }
</script>

<div class="login-card-container">
  <Card variant="outlined">
    <TabBar tabs={["Kev.In Account", "University Login"]} let:tab bind:active>
      <Tab {tab}>
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
      <form class="login-form" on:submit|preventDefault={login}>
        <div class="input-username">
          <Textfield
            invalid={userNotFound}
            id="username-input"
            style="width: 20rem"
            bind:value={username}
            label="Username"
            variant="outlined"
          >
            <HelperText slot="helper"
              >{#if userNotFound}User not found. <a href="/register"
                  >Create Account?</a
                >{/if}</HelperText
            >
          </Textfield>
        </div>
        <div class="input-password">
          <PasswordInput bind:password {wrongPassword} />
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
  .input-username {
    padding: 0.2rem;
  }
  .input-password {
    padding: 0.2rem;
  }

  .login-card-container {
    width: 25rem;
    margin: 0;
    position: absolute;
    top: 50%;
    left: 50%;
    -ms-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
  }

  .idp-select-menu {
    position: relative;
    margin: 1rem 1rem 7.7rem 1rem;
    width: 100%;
  }
</style>
