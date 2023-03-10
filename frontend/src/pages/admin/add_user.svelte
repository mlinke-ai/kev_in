<script>
  import Card, { Content } from "@smui/card";
  import { Title } from "@smui/dialog";
  import SignUp from "../../lib/Authentication/SignUp.svelte";
  import Page from "../../lib/Common/Page.svelte";
</script>

<Page title="Add User">
  <Card
    style="margin: auto; display: flex; flex-direction: column; align-items: center; padding-bottom: 1rem;"
  >
    <Title>Create new User</Title>
    <SignUp autoLogin={false} />
  </Card>
</Page>
