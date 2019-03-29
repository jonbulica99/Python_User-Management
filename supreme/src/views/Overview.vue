<template>
  <div class="home">
    <Users></Users>
    <Groups></Groups>
    <Hosts></Hosts>
  </div>
</template>

<script>

import Users from '@/components/Users.vue'
import Groups from '@/components/Groups.vue'
import Hosts from '@/components/Hosts.vue'


export default {
  name: 'overview',
  components: {
    Users,
    Groups,
    Hosts
  }
}
</script>
