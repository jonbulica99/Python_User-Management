<template>
  <div class="groups container">
    <h1 class="page-header">Manage Groups</h1>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Name</th>
          <th>State</th>
          <th>Parent</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="group in groups">
          <td>{{ group.name }}</td>
          <td>{{ group.joins.state }}</td>
          <td>
            <a v-bind:href="group_url + group.parentID">{{ group.joins.parent }}</a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";
import { Endpoints } from "../variables.js";

export default {
  name: "groups",
  components: {
    Endpoints
  },
  data() {
    return {
      groups: [],
      user_url: Endpoints.USERS,
      group_url: Endpoints.GROUPS
    };
  },
  created: function() {
    axios.get(this.group_url + '0').then(response => {
      this.groups = response.data;
    });
    setInterval(() => {
      return false;
    }, 3600);
  }
};
</script>

<style scoped>
</style>
