<script>
  import Page from "../lib/components/common/Page.svelte";
  import Button from "@smui/button/src/Button.svelte";
  import Card, {
    Content,
    PrimaryAction,
    Media,
    MediaContent,
    Actions,
    ActionButtons,
    ActionIcons,
  } from "@smui/card";

  import IconButton, { Icon } from "@smui/icon-button";
  import { Svg } from "@smui/common";
  import { each } from "svelte/internal";

  let currentUser = 1;
  let maxDisplayedUsers = 20;
  let usersLoaded = false;
  let users = [];

  // {
  //   user_id: 0,
  //   user_name: "nobody"

  // },
  // {
  //   user_id: 1,
  //   user_name: "nobody"
  // },
  // {
  //   user_id: 2,
  //   user_name: "nobody"

  // },
  // {
  //   user_id: 3,
  //   user_name: "nobody"

  // },
  // {
  //   user_id: 4,
  //   user_name: "nobody"

  // },
  //content only for testcases
  //turn later to
  //getUsers
  // ];

  //&user_limit=${maxDisplayedUsers+currentUser}

  const getUsers = async () => {
    await fetch(`/user?user_offset=${currentUser}`, {
      method: "GET",
    }).then((response) => {
      if (response.status == 200) {
        response.json().then((data) => {
          console.log(data);
          //users = [];
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

  function showLastUsers() {
    currentUser -= maxDisplayedUsers;
    usersLoaded = false;
    getUsers();
  }
</script>

<Page>
  <div class="add-user-icon">
    <div style="display: flex; align-items: center;">
      <a href="/#/error">
        <IconButton>
          <Icon component={Svg} viewBox="0 0 24 24">
            <path
              fill="outlined"
              d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 9h-4v4h-2v-4H9V9h4V5h2v4h4v2z"
            />
          </Icon>
        </IconButton>&nbsp; add user
      </a>
    </div>
  </div>

  <h1>Users</h1>

  <p>This is a placeholder site for listing all users.</p>

  {#if usersLoaded}
    <div class="grid-container">
      {#each users as user}
        <div class="grid-item">
          <Card>
            <div style="display: flex; align-items: center;">
              <a href="/#/error">
                <IconButton>
                  <Icon component={Svg} viewBox="0 0 24 24">
                    <path
                      fill="outlined"
                      d="M12 12.75c1.63 0 3.07.39 4.24.9 1.08.48 1.76 1.56 1.76 2.73V18H6v-1.61c0-1.18.68-2.26 1.76-2.73 1.17-.52 2.61-.91 4.24-.91zM4 13c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm1.13 1.1c-.37-.06-.74-.1-1.13-.1-.99 0-1.93.21-2.78.58C.48 14.9 0 15.62 0 16.43V18h4.5v-1.61c0-.83.23-1.61.63-2.29zM20 13c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm4 3.43c0-.81-.48-1.53-1.22-1.85-.85-.37-1.79-.58-2.78-.58-.39 0-.76.04-1.13.1.4.68.63 1.46.63 2.29V18H24v-1.57zM12 6c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3z"
                    />
                  </Icon>
                </IconButton>
              </a>
            </div>

            <a href="/#/error">
              #{user.user_id}
              {user.user_name}
            </a>
          </Card>
        </div>
      {/each}
    </div>
  {/if}

  <a href="/#/admin-dashboard">
    <Button>Back to dashboard</Button>
  </a>

  {#if users.length > maxDisplayedUsers && currentUser == 1}
    <div class="list-users-buttons">
      <Button on:click={getUsers}>more users</Button>
    </div>
  {:else if users.length > maxDisplayedUsers && users.length <= currentUser + maxDisplayedUsers - 1}
    <div class="list-users-buttons">
      <Button on:click={showLastUsers}>last users</Button>
    </div>
  {:else if users.length > maxDisplayedUsers && currentUser != 1}
    <div class="list-users-buttons">
      <Button on:click={getUsers}>more users</Button>
      <Button on:click={showLastUsers}>last users</Button>
    </div>
  {/if}
</Page>

<style>
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
    width: 350px;
    background-color: #001a16;
    padding: 10px;
    font-size: 30px;
    text-align: center;
  }

  .add-user-icon {
    float: right;
    align-items: right;
  }

  .list-users-buttons {
    float: right;
  }
</style>
