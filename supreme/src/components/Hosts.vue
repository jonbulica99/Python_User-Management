<template>
  <div class="hosts container card shadow-sm">
    <h1 class="page-header">Hosts</h1>
    <table class="table table-hover table-responsive-sm">
      <thead class="thead-light">
        <tr>
          <th>Hostname</th>
          <th>Address</th>
          <th>Port</th>
          <th>Login user</th>
          <th v-if="actions">Actions</th>
        </tr>
      </thead>
      <tbody v-bind:name="actions ? 'fade' : ''" is="transition-group">
        <template v-for="host in hosts">
          <tr v-bind:key="host.id" @click="editHost(host)">
            <td>
              <a v-bind:href="host_url + host.id">{{ host.name }}</a>
            </td>
            <td>{{ host.address }}</td>
            <td>{{ host.port }}</td>
            <td>
              <a v-bind:href="user_url + host.joins.user.username">{{ host.joins.user.username }}</a>
            </td>
            <td class="actions" v-if="actions">
              <a class="btn btn-primary" @click="editHost(host)">
                <edit-icon></edit-icon>
              </a>
              <a class="btn btn-danger" @click="confirmDelete(host)">
                <delete-icon></delete-icon>
              </a>
            </td>
          </tr>
        </template>
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
    });
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
        response = response.data;
        if (response.success) {
          this.hosts = response.data;
          EventBus.$emit("updateHosts", this.hosts);
        } else {
          this.$dialog.alert(
            "<b>Error fetching hosts</b>: " +
              response.message +
              "<br><i>Check the console log for more information.</i>"
          );
          console.log(response.exception);
        }
      });
    }
  }
};
</script>

<style scoped>
</style>
