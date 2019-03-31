<template>
  <div class="home">
    <Commands></Commands>
    <br>
    <div class="container">
      <Users></Users>
      <Groups></Groups>
      <Hosts></Hosts>
    </div>
  </div>
</template>

<script>

import Users from '@/components/Users.vue'
import Groups from '@/components/Groups.vue'
import Hosts from '@/components/Hosts.vue'
import Commands from '@/components/Commands.vue'


export default {
  name: 'overview',
  components: {
    Users,
    Groups,
    Hosts,
    Commands
  }
}
</script>
