<template>
  <div class="home">
    <Users></Users>
    <Hosts></Hosts>
  </div>
</template>

<script>
// @ is an alias to /src
import Users from '@/components/Users.vue'
import Hosts from '@/components/Hosts.vue'

export default {
  name: 'home',
  components: {
    Users,
    Hosts
  }
}
</script>
