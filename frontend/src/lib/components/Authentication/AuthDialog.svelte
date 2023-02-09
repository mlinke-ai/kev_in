<script>
    import Tab, { Label as TLabel } from "@smui/tab";
    import TabBar from "@smui/tab-bar";
    import SignUp from "./SignUp.svelte";
    import Login from "./Login.svelte";

    let active = "Login";
</script>

<TabBar tabs={["Login", "Sign Up"]} let:tab bind:active>
    <Tab style={"cursor: default"} {tab}>
        <TLabel>{tab}</TLabel>
    </Tab>
</TabBar>
{#if active == "Sign Up"}
    <SignUp />
{:else}
    <Login />
{/if}
