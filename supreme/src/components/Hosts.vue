<template>
  <div class="hosts container">
    <h1 class="page-header">Hosts</h1>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Hostname</th>
          <th>Adresse</th>
          <th>Port</th>
          <th>Anmelde-Benutzer</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="host in hosts">
          <td>
            <a v-bind:href="host_url + host.id">{{ host.name }}</a>
          </td>
          <td>{{ host.address }}</td>
          <td>{{ host.port }}</td>
          <td>
            <a v-bind:href="user_url + host.joins.user.username">{{ host.joins.user.username }}</a>
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
  name: "hosts",
  components: {
    Endpoints
  },
  data() {
    return {
      hosts: [],
      host_url: Endpoints.HOSTS,
      user_url: Endpoints.USERS
    };
  },
  created: function() {
    axios.get(this.host_url + '0').then(response => {
      this.hosts = response.data;
    });
    setInterval(() => {
      axios.get(this.host_url + '0').then(response => {
        this.hosts = response.data;
      });
    }, 3600000);
  }
};
</script>

<style scoped>

</style>
