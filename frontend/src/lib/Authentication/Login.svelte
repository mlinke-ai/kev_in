<!-- Login component that requests email and password from user -->
<script>
  import Button from "@smui/button";
  import Textfield from "@smui/textfield";
  import Message from "../common/Message/Message.svelte";
  import { messages } from "../common/types";
  import PasswordInput from "./PasswordInput.svelte";
  import { login } from "./user";

  let email = "";
  let password = "";

  let errorMessage;
  let warningMessage;

  const attemptLogin = async () => {
    if (!email || !password) {
      warningMessage.open();
      return;
    }
    if (await login(email, password)) {
    } else {
      document.getElementById("email-input").focus();
      errorMessage.open();
    }
  };
</script>

<form class="login-form" on:submit|preventDefault={attemptLogin} hidden>
  <div class="input">
    <Textfield
      id="email-input"
      style="width: 20rem"
      bind:value={email}
      label="Email"
      variant="outlined"
    />
  </div>
  <div class="input" style="margin-top: 1rem;">
    <PasswordInput bind:password style="width: 20rem" />
  </div>
  <input type="submit" hidden />
</form>
<Button on:click={attemptLogin} variant="unelevated">Login</Button>

<Message
  bind:message={errorMessage}
  content={"Wrong username or password"}
  type={messages.error}
/>
<Message
  bind:message={warningMessage}
  content={"Please enter your credentials"}
  type={messages.warning}
/>

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
