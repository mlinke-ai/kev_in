<script>
    import Page from "../lib/components/common/Page.svelte";

    import Card, {
    Content,
    PrimaryAction,
    Media,
    MediaContent,
    Actions,
    ActionButtons,
    ActionIcons,
  } from '@smui/card';
  import Button, { Label } from '@smui/button';
  import GroupSvg from "../lib/components/AnimatedSVG/GroupSVG.svelte";
  import ExerciseSvg from "../lib/components/AnimatedSVG/ExerciseSVG.svelte";

</script>


<Page>
    
    <div class="grid-container-outside">
      <!--  Header -->
      <div class="header-outside">
        <h1 style="padding: 10px; font-family: monospace;">
          Welcome to your dashboard!

        </h1>
      </div>

      <!--  Menu -->
      <div class="menu-outside">

      </div>

      <!--  Main -->
      <div class="main-outside">
        <div class="grid-container-inside">
          <div class="left-inside">
            <a href="/#/users">
            <Card>
              <GroupSvg/>
            </Card>
            <div class="label">
              List all users
            </div>
          </a>
          </div>
            
          <div class="right-inside">
            <a href="/#/exercises">
            <Card>
              <ExerciseSvg/>
            </Card>
            <div class="label">List all exercises</div> 
          </a>
          </div>

        </div>   
      </div> 

      <!--  Right -->
      <div class="right-outside">
        <h4>Solved Exercieses:</h4>
        <p>function not implemented yet</p>
      </div>

      <!--  Footer -->
      <div class="footer-outside">

      </div>
    </div>
</Page>


<style lang=scss>
    .header-outside { 
      grid-area: header;
      width: auto; 
      height: fit-content;
    }

    .menu-outside { 
      grid-area: menu; 
    }
    .main-outside { 
      width: fit-content;
      align-content: center;
      grid-area: main; 
    }
    .right-outside { 
      max-width: 1200px;
      align-content: center;
      grid-area: right; 
      padding: 10px;
    }

    .footer-outside { grid-area: footer; }
    
    .grid-container-outside {
      display: grid;
      grid-template-areas:
        'header header header'
        'main main right';
      gap: 5px;
      background-color: transparent;
      padding: 10px;
    }
    
    .grid-container-outside > div {
      background-color: rgb(0,57,49);
      font-size: 30px;
    }

    .left-inside { 
      width: 300px;
      height: auto;
      align-content: center;
      grid-area: left; 
    }

    .right-inside { 
      width: 300px;
      height: auto;
      align-content: center;
      grid-area: right; 
    }

    .grid-container-inside {
      display: grid;
      grid-template-areas:
        'left right';
      gap: 10px;
      background-color: transparent;
      padding: 10px;
    }
    
    .grid-container-inside > div {
      background-color: rgb(0,57,49);
      font-size: 30px;
    }

    .label{
      align-content: center;
      padding: 5px;
    }



</style>