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
    export let helperText = ""
    export let label = "Password"
    export let style = ""
    export let inputHandler = null
</script>

<Textfield id="password-input" on:keyup={(e) => checkCapsLock(e)} on:input={inputHandler} invalid={wrongPassword} style={"display: flex; align-items: center; ".concat(style)} type={displayType} bind:value={password} label={label} variant="outlined">
    <IconButton tabindex={-1} type="button" slot="trailingIcon" toggle bind:pressed={visible} on:click={toggleVisibility}>
        <Icon class="material-icons">visibility</Icon>
        <Icon class="material-icons" on>visibility_off</Icon>
    </IconButton>
    <HelperText slot="helper">
        {#if capsLockActive}
            CAPS LOCK is active!
        {:else if wrongPassword}
            <!-- <a href="/forgot-password">Forgot Password?</a> -->
            {helperText}
        {/if}
    </HelperText>
</Textfield>