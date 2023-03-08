<script lang="ts">
  import Menu from "@smui/menu";
  import { Anchor } from "@smui/menu-surface";
  import List, { Item, Separator, Text } from "@smui/list";
  import { logout } from "../Authentication/user";
  import { push as pushRoute } from "svelte-spa-router";
  import Button, { Icon, Label } from "@smui/button";
  import { accessLevel, startPage, userName } from "../../stores";
  import { accessLevels } from "../Common/types";
  import ThemeSelector from "../Theming/ThemeSelector.svelte";
  import Tooltip, { Wrapper } from "@smui/tooltip";

  let menu: Menu;
  let anchor: HTMLDivElement;
  let anchorClasses: { [k: string]: boolean } = {};
</script>

<div
  class={Object.keys(anchorClasses).join(" ")}
  use:Anchor={{
    addClass: (className) => {
      if (!anchorClasses[className]) {
        anchorClasses[className] = true;
      }
    },
    removeClass: (className) => {
      if (anchorClasses[className]) {
        delete anchorClasses[className];
        anchorClasses = anchorClasses;
      }
    },
  }}
  bind:this={anchor}
>
  <Button class="account-button" on:click={() => menu.setOpen(!menu.menuOpen)}>
    {#if $accessLevel >= accessLevels.admin}
      <Icon class="material-icons account-icon">admin_panel_settings</Icon>
    {:else}
      <Icon class="material-icons account-icon">account_circle</Icon>
    {/if}
    <Label>{$userName}</Label>
  </Button>
  <Menu
    bind:this={menu}
    anchor={false}
    bind:anchorElement={anchor}
    anchorCorner="BOTTOM_LEFT"
  >
    <List>
      <Wrapper>
      <Item
        disabled
        on:SMUI:action={() => {
          pushRoute("/profile");
        }}
      >
        <div class="menu-item">
          <Icon style="color: grey" class="material-icons">person</Icon>
          <Text>Profile</Text>
        </div>
      </Item>
      <Tooltip style="z-index: 999;">Coming Soon!</Tooltip>
    </Wrapper>
      <Item
        on:SMUI:action={() => {
          pushRoute($startPage);
        }}
      >
        <div class="menu-item">
          <Icon style="color: white;" class="material-icons">bar_chart</Icon>
          <Text>Dashboard</Text>
        </div>
      </Item>
      <Separator />
      <ThemeSelector />
      <Separator />
      <Item on:SMUI:action={logout}>
        <div class="menu-item">
          <Icon style="color: white;" class="material-icons">logout</Icon>
          <Text>Logout</Text>
        </div>
      </Item>
    </List>
  </Menu>
</div>

<style lang="scss">
  @use "../../variables";
  * :global(.account-icon) {
    transform: scale(1.5);
  }
  * :global(.account-button) {
    color: variables.$secondaryDark;
    display: flex;
    align-items: center;
    gap: 0.35rem;
  }
  .menu-item {
    display: flex;
    gap: 0.35rem;
  }
</style>
