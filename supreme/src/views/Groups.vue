<template>
  <div class="groups">
    <Groups actions></Groups>
    <NewGroup></NewGroup>
  </div>
</template>

<script>

import Groups from '@/components/Groups.vue'
import NewGroup from '@/components/NewGroup.vue'

export default {
  name: 'groups',
  components: {
    Groups,
    NewGroup
  }
}
</script>
