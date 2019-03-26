<template>
  <div class="users container">
    <h1 class="page-header">Manage Users</h1>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Vorname</th>
          <th>Nachname</th>
          <th>Username</th>
          <th>Password</th>
          <th>Public-Key</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users">
          <td>{{ user.firstname }}</td>
          <td>{{ user.lastname }}</td>
          <td>
            <a v-bind:href="user_url + user.username">{{ user.username }}</a>
          </td>
          <td>{{ user.password }}</td>
          <td>{{ user.publicKey }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";
import { Endpoints } from "../variables.js";

export default {
  name: "users",
  components: {
    Endpoints
  },
  data() {
    return {
      users: [],
      user_url: Endpoints.USERS
    };
  },
  created: function() {
    axios.get(this.user_url + 'all').then(response => {
      this.users = response.data;
    });
    setInterval(() => {
      axios.get(this.user_url + 'all').then(response => {
        this.users = response.data;
      });
    }, 3600000);
  }
};
</script>

<style scoped>
</style>
