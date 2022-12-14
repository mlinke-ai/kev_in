<script>
    import Textfield from '@smui/textfield'
    import HelperText from '@smui/textfield/helper-text'
    import IconButton, { Icon } from '@smui/icon-button'

    let visible = false
    let displayType = "password"
    let capsLockActive = false

    const toggleVisibility = () => {
        if (visible) {
            displayType = "password"
        } else {
            displayType = ""
        }
    }

    // @ts-ignore
    const checkCapsLock = (e) => {
        capsLockActive = e.getModifierState("CapsLock")
    }

    export let password = ""
    export let wrongPassword = false

</script>

<Textfield id="password-input" on:keyup={(e) => checkCapsLock(e)} invalid={wrongPassword} style="width: 20rem; display: flex; align-items: center;" type={displayType} bind:value={password} label="Password" variant="outlined">
    <IconButton tabindex={-1} type="button" slot="trailingIcon" toggle bind:pressed={visible} on:click={toggleVisibility}>
        <Icon class="material-icons">visibility</Icon>
        <Icon class="material-icons" on>visibility_off</Icon>
    </IconButton>
    <HelperText slot="helper">
        {#if capsLockActive}
            CAPS LOCK is active!
        {:else if wrongPassword}
            <a href="/forgot-password">Forgot Password?</a>
        {/if}
    </HelperText>
</Textfield>