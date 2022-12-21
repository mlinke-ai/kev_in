<script>
    import Button from "@smui/button";
    
    export let label = ""
    export let route = ""
    export let variant = ""
</script>

<div class="navbar-button">
    <a href={route}>
        <Button variant={variant}>{label}</Button>
    </a>
</div>

<style>
    .navbar-button {
        margin-left: 1rem;
    }
</style>