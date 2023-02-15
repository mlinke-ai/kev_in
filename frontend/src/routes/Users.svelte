<script>
  import Page from "../lib/common/Page.svelte";
  import Button from "@smui/button/src/Button.svelte";

  import IconButton, { Icon } from "@smui/icon-button";
  import { Label, Svg } from "@smui/common";
  import { each } from "svelte/internal";
  import { accessLevel } from "../stores";
  import { accessLevels } from "../lib/constants";

  let currentUser = 1;
  let maxDisplayedUsers = 20;
  let usersLoaded = false;
  let users = [];

  const getUsers = async () => {
    await fetch(`/user?user_offset=${currentUser}`, {
      method: "GET",
    }).then((response) => {
      if (response.status == 200) {
        response.json().then((data) => {
          console.log(data);
          users = Object.values(data);
          console.log(users);
          currentUser += maxDisplayedUsers;
          usersLoaded = true;
        });
      } else if (response.status == 400) {
        alert(this.message);
      } else if (response.status == 403) {
        alert(this.message);
      } else if (response.status == 500) {
        alert("Oops an Error occured. Please try again.");
      } else {
        alert("Oops an Error occured. " + response.status);
      }
    });
  };

  getUsers();

  function showNextUsers() {
    usersLoaded = false;
    getUsers();
  }

  function showLastUsers() {
    currentUser -= maxDisplayedUsers;
    usersLoaded = false;
    getUsers();
  }
</script>

<Page requiredAccessLevel={accessLevels.admin}>

  <h1>Users</h1>

  <div class="add-user-icon">
    <a href="/#/adduser">
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

  <p>This is a placeholder site for listing all users.</p>

  {#if usersLoaded}
    <div class="grid-container">
      {#each users as user}
        <div class="grid-item">
          
            <div class="display-icon">
            
              <a href="/#/error">
                <!-- please add link to profile of user with {user.user_id} -->
                  <Icon component={Svg} viewBox="0 1 20 20">
                    <path
                      fill="outlined"
                      d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                    />
                  </Icon>
              </a>
          
          </div>

            <div class="label">
              <a href="/#/error">
                <!-- please add link to profile of user with {user.user_id} -->
                #{user.user_id}
                {user.user_name}
              </a>
            </div>
        
        </div>
      {/each}
    </div>
  {/if}

  <a href="/#/admin-dashboard">
    <Button>Back to dashboard</Button>
  </a>

  {#if users.length > maxDisplayedUsers && currentUser == 0}
    <div class="list-users-buttons">
      <Button on:click={showNextUsers}>more users</Button>
    </div>
  {:else if users.length > maxDisplayedUsers && users.length <= currentUser + maxDisplayedUsers - 1}
    <div class="list-users-buttons">
      <Button on:click={showLastUsers}>last users</Button>
    </div>
  {:else if users.length > maxDisplayedUsers && currentUser != 0}
    <div class="list-users-buttons">
      <Button on:click={showNextUsers}>more users</Button>
      <Button on:click={showLastUsers}>last users</Button>
    </div>
  {/if}
<!-- does not work properly yet, needs total number of users from backend-->
</Page>

<style lang="scss">
  .grid-container {
    max-width: 3fr;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    background-color: rgb(0, 57, 49);
    padding: 10px;
    margin: auto auto;
    grid-auto-rows: auto;
    grid-gap: 10px;
  }

  .grid-item {
    border: #001a16;
    width: 350px;
    background-color: #001a16;
    padding: 10px;
  }

  .display-icon{
    float: left;
    width: 100px;
    height: 100px;
  }

  .label{
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
