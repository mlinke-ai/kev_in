<script>
    import { Icon, Label } from "@smui/button"
    import Card, { Content } from "@smui/card/"
    import Ripple from "@smui/ripple"
</script>

<div class="lecture-card-container" use:Ripple={{ surface: true }}>
    <Card variant="outlined">
        <Content>
            <div class="lecture-card-content-container">
                <div class="lecture-card-icon">
                    <Icon class="material-icons" on size={100}>lock</Icon>
                </div>
                <div class="lecture-card-label">
                    1 - Welcome
                </div>
            </div>
        </Content>
    </Card>
</div>

<style>
    .lecture-card-container {
        padding: 0;
        margin: 0;
        max-width: 15rem;
    }

    .lecture-card-content-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-size: 1.5rem;
    }

    .lecture-card-label {
        font-family: "Roboto Mono";
    }
</style>