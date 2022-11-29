<script>
    import Button, { Label } from '@smui/button'
    import Card from '@smui/card/'
    import Textfield from '@smui/textfield'
    import HelperText from '@smui/textfield/helper-text'
	import PasswordInput from './PasswordInput.svelte'
    import Tab, { Label as TLabel } from "@smui/tab"
    import TabBar from "@smui/tab-bar"
    import Select, { Option } from "@smui/select"

    let username = ""
    let password = ""
    let correctPassword = "test123"

    let userNotFound = false
    let wrongPassword = false

    let active = "Kev.In Account"
    let idProviders = ["TU Chemnitz", "WH Zwickau"]
    let value = "TU Chemnitz"
    


    const login = () => {
        //fetch password hash hash by submitting username
        //if answer is empty, user is not registered

        // hash user password
        if (username != "pymon") {
            userNotFound = true
            document.getElementById("username-input").focus();
        } else if (password == correctPassword) {
            userNotFound = false
            alert("Logged in!")
            wrongPassword = false
        } else {
            wrongPassword = true
            document.getElementById("password-input").focus();
        }
    }
</script>

<div class="login-card-container">
    <Card variant=outlined>
        <TabBar tabs={['Kev.In Account', "Shibboleth"]} let:tab bind:active>
            <Tab {tab}>
                <TLabel>{tab}</TLabel>
            </Tab>
        </TabBar>   
        
        {#if active == "Shibboleth"}
            <div class="idp-select-menu">
                <Select style="width: 90%" bind:value label="Select ID Provider">
                    {#each idProviders as fruit}
                      <Option value={fruit}>{fruit}</Option>
                    {/each}
                  </Select>
        </div>
        
        
        {:else}
        <form class="login-form" on:submit|preventDefault={login}>
            <div class="input-username">
                <Textfield invalid={userNotFound} id="username-input" style="width: 20rem" bind:value={username} label="Username" variant="outlined">
                    <HelperText slot="helper">{#if userNotFound}User not found. <a href="/register">Create Account?</a>{/if}</HelperText>
                </Textfield>
            </div>
            <div class="input-password">
                <PasswordInput bind:password={password} wrongPassword={wrongPassword}/>
            </div>
            
        </form>
        {/if}
        <Button class="login-button" type="submit" variant="unelevated">Login</Button>
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
            padding: .2rem;
    }
    .input-password {
            padding: .2rem;
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
