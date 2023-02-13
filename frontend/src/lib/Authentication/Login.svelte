<!-- Login component that requests email and password from user -->

<script>
  import Button from "@smui/button";
  import Textfield from "@smui/textfield";
  import PasswordInput from "./PasswordInput.svelte";
  import { login } from "./user";

  let email = "";
  let password = "";

  let wrongCredentials = false;

  $: if (wrongCredentials) {
    document.getElementById("email-input").focus();
  }
</script>

<form
  class="login-form"
  on:submit|preventDefault={async () => {
    wrongCredentials = !(await login(email, password));
  }}
  hidden
>
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
  <input type="submit" hidden />
</form>
<Button
  on:click={async () => {
    wrongCredentials = !(await login(email, password));
  }}
  variant="unelevated">Login</Button
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
