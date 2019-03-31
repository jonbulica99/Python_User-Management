<template>
  <div class="users container card shadow-sm">
    <h1 class="page-header">Users</h1>
    <table class="table table-hover table-responsive-sm">
      <thead class="thead-light">
        <tr>
          <th>First name</th>
          <th>Last name</th>
          <th>Username</th>
          <th>Password</th>
          <th>Groups</th>
          <th>State</th>
          <th>Public Key</th>
          <th v-if="actions">Actions</th>
        </tr>
      </thead>
      <tbody v-bind:name="actions ? 'fade' : ''" is="transition-group">
        <template v-for="user in users">
          <tr v-bind:key="user.id">
            <td>{{ user.firstname }}</td>
            <td>{{ user.lastname }}</td>
            <td>
              <a v-bind:href="user_url + user.username">{{ user.username }}</a>
            </td>
            <td>{{ user.password }}</td>
            <td>
              <span v-for="group in user.joins.groups" v-bind:key="group.id">
                <a class="badge badge-secondary" v-bind:href="group_url + group.id">{{ group.name }}</a>
                <span>&nbsp;</span>
              </span>
            </td>
            <td>{{ user.joins.state }}</td>
            <td v-if="user.publicKey">{{ user.publicKey }}</td>
            <td v-else>
              <i>None</i>
            </td>
            <td class="actions" v-if="actions">
              <a class="btn btn-primary" v-on:click="editUser(user)">
                <edit-icon></edit-icon>
              </a>
              <a class="btn btn-danger" v-on:click="confirmDelete(user)">
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
  name: "users",
  props: {
    actions: Boolean
  },
  data() {
    return {
      users: [],
      user_url: Endpoints.USERS,
      group_url: Endpoints.GROUPS
    };
  },
  created: function() {
    this.fetchUsers();
  },
  mounted() {
    EventBus.$on("fetchUsers", () => {
      this.fetchUsers();
    });
  },
  methods: {
    editUser(user) {
      EventBus.$emit("editUser", user);
    },
    confirmDelete(user) {
      this.$dialog
        .confirm("Do you really want to delete <b>" + user.username + "</b>?")
        .then(function() {
          EventBus.$emit("deleteUser", user);
        })
        .catch(function() {
          console.log("User delete aborted.");
        });
    },
    fetchUsers() {
      axios.get(this.user_url + "all").then(response => {
        response = response.data;
        if (response.success) {
          this.users = response.data;
          EventBus.$emit("updateUsers", this.users);
        } else {
          this.$dialog.alert(
            "<b>Error fetching users</b>: " +
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
