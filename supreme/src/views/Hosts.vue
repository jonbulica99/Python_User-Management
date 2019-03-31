<template>
  <div class="hosts-page">
    <Hosts actions></Hosts>
    <NewHost></NewHost>
  </div>
</template>

<script>
// @ is an alias to /src
import Hosts from '@/components/Hosts.vue'
import NewHost from '@/components/NewHost.vue'

export default {
  name: 'hosts',
  components: {
    Hosts,
    NewHost
  }
}
</script>
