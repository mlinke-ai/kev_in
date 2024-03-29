<script lang="ts">
  import Page from "../../lib/Common/Page.svelte";
  import Button from "@smui/button/src/Button.svelte";

  import IconButton, { Icon } from "@smui/icon-button";
  import { Label, Svg } from "@smui/common";
  import { each } from "svelte/internal";
  import type { GetUser } from "../../lib/Authentication/types";
  import { link } from "svelte-spa-router";

  const maxDisplayed = 18;
  let currentUserUrl = `/user?user_offset=1&user_limit=${maxDisplayed}`;
  let prevUsersUrl;
  let nextUsersUrl;
  let usersLoaded = false;
  let users = [];
  let usersData: Array<GetUser>;
  let usersMeta;

  const getUsers = async () => {
    await fetch(`${currentUserUrl}`, {
      method: "GET",
    }).then((response) => {
      if (response.status == 200) {
        response.json().then((data) => {
          users = Object.values(data);
          usersData = users[0];
          usersMeta = users[1];
          prevUsersUrl = usersMeta.prev_url;
          nextUsersUrl = usersMeta.next_url;
          console.log(prevUsersUrl);
          usersLoaded = true;
        });
      } else if (response.status == 204) {
        console.log("There are no users in database. Error: " + response.status);
      } else if (response.status == 500) {
        alert("Oops an Error occured. Please try again.");
      } else {
        alert("Oops an Error occured. " + response.status);
      }
    });
  };

  getUsers();

  function showNextUsers() {
    currentUserUrl = nextUsersUrl;
    usersLoaded = false;
    getUsers();
  }

  function showLastUsers() {
    currentUserUrl = prevUsersUrl;
    usersLoaded = false;
    getUsers();
  }
</script>

<Page>
  <h1>Users</h1>

  <div class="add-user-icon">
    <a href="/#/error">
      <!-- add link for adding a new user -->
      <Button>
        <Icon component={Svg} viewBox="0 0 24 24">
          <path
            fill="outlined"
            d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 9h-4v4h-2v-4H9V9h4V5h2v4h4v2z"
          />
        </Icon>
        <Label>add user</Label>
      </Button>
    </a>
  </div>

  <p>Click on the name of a user to display his profile</p>

  {#if usersLoaded}
    <div class="grid-container">
      {#each usersData as user}
        <div class="grid-item">
          <div class="card">
            <a use:link href={`/admin/user-profile/${user.user_id}`}>
              <div class="display-icon">
                <Icon component={Svg} viewBox="0 1 20 20">
                  <path
                    fill="outlined"
                    d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                  />
                </Icon>
              </div>
            </a>

            <a use:link href={`/admin/user-profile/${user.user_id}`}>
              <div class="label">
                #{user.user_id}
                {user.user_name}
              </div>
            </a>
          </div>
        </div>
      {/each}
    </div>
  {/if}

  <a href="/#/admin">
    <Button>Back to dashboard</Button>
  </a>

  {#if prevUsersUrl == null && nextUsersUrl != null}
    <div class="list-users-buttons">
      <Button on:click={showNextUsers}>more users</Button>
    </div>
  {:else if prevUsersUrl != null && nextUsersUrl == null}
    <div class="list-users-buttons">
      <Button on:click={showLastUsers}>last users</Button>
    </div>
  {:else if prevUsersUrl != null && nextUsersUrl != null}
    <div class="list-users-buttons">
      <Button on:click={showLastUsers}>last users</Button>
      <Button on:click={showNextUsers}>more users</Button>
    </div>
  {/if}
</Page>

<style lang="scss">
  .grid-container {
    max-width: 3fr;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    background-color: transparent;
    padding: 10px;
    margin: auto auto;
    grid-auto-rows: auto;
    grid-gap: 10px;
  }

  .grid-item {
    width: 350px;
    background-color: var(--mdc-theme-primary);
    padding: 10px;
  }

  .card{
    height: 120px;
    background-color: var(--mdc-theme-surface);
  }

  .display-icon {
    float: left;
    width: 100px;
    height: 100px;
  }

  .label {
    float: center;
    width: 200px;
    word-break: break-all;
    padding: 20px 0px 5px 50px;
    margin-left: 80px;
    font-family: monospace;
    font-size: 30px;
  }

  .add-user-icon {
    float: right;
    align-items: right;
  }

  .list-users-buttons {
    float: right;
  }
</style>
