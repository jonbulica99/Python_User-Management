<template>
  <div class="hosts">
    <Hosts></Hosts>
  </div>
</template>

<script>
// @ is an alias to /src
import Hosts from '@/components/Hosts.vue'

export default {
  name: 'hosts',
  components: {
    Hosts
  }
}
</script>
