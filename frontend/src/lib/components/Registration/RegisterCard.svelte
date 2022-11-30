<script>
    import Button, { Label } from '@smui/button'
    import Card from '@smui/card/'
    import Textfield from '@smui/textfield'
    import HelperText from '@smui/textfield/helper-text'

    let username = ""
    let password = ""
    let repeatPassword = ""
    let email = ""
</script>

<div class="register-card-container">
    <Card variant=outlined>
        <form class="register-form" on:submit|preventDefault={() => {}}>
            <div class="input-username">
                <Textfield id="username-input" style="width: 20rem" bind:value={username} label="Username" variant="outlined"></Textfield>
            </div>
            <div class="input-password">
                <Textfield id="password-input" style="width: 20rem" bind:value={password} label="Password" variant="outlined"></Textfield>
                <Textfield id="password-input" style="width: 20rem" bind:value={repeatPassword} label="Repeat Password" variant="outlined"></Textfield>
            </div>
            
        </form>
    </Card>
</div>

<style lang="css">
    .register-card-container {
        width: 25rem;
        margin: 0;
        position: absolute;
        top: 50%;
        left: 50%;
        -ms-transform: translate(-50%, -50%);
        transform: translate(-50%, -50%);
    }
    .register-form {
        margin: auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 1rem;
    }
    .input-username {
        padding: 2rem;
    }
    .input-password {
        padding: 2rem;
    }
</style>
