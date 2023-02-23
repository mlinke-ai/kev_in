<script>
  import Navbar from "../lib/Navbar/Navbar.svelte";
  import Footer from "../lib/Footer/Footer.svelte";
  import AcceptCookies from "../lib/AcceptCookies/AcceptCookies.svelte";
</script>

<AcceptCookies />
<Navbar />
<slot />
<Footer />
