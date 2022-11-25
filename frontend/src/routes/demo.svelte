<script>
    import Card from "@smui/card"
    import Button from "@smui/button"
    import { Label } from "@smui/common"
    import { Icon } from "@smui/common"
    import Badge from "@smui-extra/badge"

    let likes = 0
    let dislikes = 0

    function like() {
        likes++
    }

    function dislike() {
        dislikes++
    }
</script>

<body>
    <div class="card-container">
        <Card class="welcome-card" variant="outlined" padded>
            <div class=welcome-card-content>
                <Label>Welcome to the <b>new</b> Framework!</Label>
                <div class="button-area">
                    <Button on:click={like}>
                        <Icon class="material-icons">thumb_up</Icon> Like
                        <Badge aria-label="new messages count">{likes}</Badge>
                    </Button>
                    <Button on:click={dislike}>
                        <Icon class="material-icons">thumb_down</Icon> Dislike
                        <Badge aria-label="new messages count">{dislikes}</Badge>
                    </Button>
                </div>
            </div>
        </Card>
    </div>
</body>


<style>
    .card-container {
        max-width: 30%;
        color: #005f50;
        font-size: 2rem;
        position: absolute;
        margin: 0;
        left: 50%;
        top: 50%;
        -ms-transform: translate(-50%, -50%);
        transform: translate(-50%, -50%);
    }
    .welcome-card-content {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .button-area {
        margin-top: 1.5rem;
    }
</style>