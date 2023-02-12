<script lang="ts">
    import Menu from "@smui/menu";
    import { Anchor } from "@smui/menu-surface";
    import List, { Item, Separator, Text } from "@smui/list";
    import IconButton, { Icon } from "@smui/icon-button";

    import { logout } from "../../functions/user";
    import { push as pushRoute } from "svelte-spa-router";
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
    <IconButton
        style="color: white;"
        class="material-icons"
        on:click={() => menu.setOpen(true)}
    >
        account_circle
    </IconButton>
    <Menu
        bind:this={menu}
        anchor={false}
        bind:anchorElement={anchor}
        anchorCorner="BOTTOM_LEFT"
    >
        <List>
            <Item on:SMUI:action={() => {pushRoute("/profile")}}>
                <div class="menu-item">
                    <Icon style="color: white;" class="material-icons"
                        >person</Icon
                    >
                    <Text>Profile</Text>
                </div>
            </Item>
            <Item on:SMUI:action={() => {pushRoute("/dashboard")}}>
                <div class="menu-item">
                    <Icon style="color: white;" class="material-icons"
                        >bar_chart</Icon
                    >
                    <Text>Dashboard</Text>
                </div>
            </Item>
            <Separator />
            <Item on:SMUI:action={logout}>
                <div class="menu-item">
                    <Icon style="color: white;" class="material-icons"
                        >logout</Icon
                    >
                    <Text>Logout</Text>
                </div>
            </Item>
        </List>
    </Menu>
</div>

<style>
    .menu-item {
        display: flex;
        gap: .35rem;
    }
</style>
