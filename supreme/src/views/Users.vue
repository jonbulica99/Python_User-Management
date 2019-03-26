<template>
  <div class="home">
    <Users></Users>
    <NewUser></NewUser>
  </div>
</template>

<script>

import Users from '@/components/Users.vue'
import NewUser from '@/components/NewUser.vue'

export default {
  name: 'users',
  components: {
    Users,
    NewUser
  }
}
</script>
