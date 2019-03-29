<template>
  <div class="hosts container">
    <h1 class="page-header">Hosts</h1>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Hostname</th>
          <th>Address</th>
          <th>Port</th>
          <th>Login user</th>
          <th v-if="actions">Actions</th>
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
          <td class="actions" v-if="actions">
            <a class="btn btn-primary" v-on:click="editHost(host)">
              <edit-icon></edit-icon>
            </a>
            <a class="btn btn-danger" v-on:click="confirmDelete(host)">
              <delete-icon></delete-icon>
            </a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";
import { EventBus } from "@/events.js";
import { Endpoints } from "@/variables.js";

export default {
  name: "hosts",
  props: {
    actions: Boolean
  },
  data() {
    return {
      hosts: [],
      user_url: Endpoints.USERS,
      host_url: Endpoints.HOSTS
    };
  },
  created: function() {
    this.fetchHosts();
  },
  mounted() {
    EventBus.$on("fetchHosts", () => {
      this.fetchHosts();
    })
  },
  methods: {
    editHost(host) {
      EventBus.$emit("editHost", host);
    },
    confirmDelete(host) {
      this.$dialog
        .confirm("Do you really want to delete " + host.name + "?")
        .then(function() {
          EventBus.$emit("deleteHost", host);
        })
        .catch(function() {
          console.log("Host delete aborted.");
        });
    },
    fetchHosts() {
      axios.get(this.host_url + "0").then(response => {
        this.hosts = response.data;
        EventBus.$emit("updateHosts", this.hosts);
      });
    }
  }
};
</script>

<style scoped>
</style>
