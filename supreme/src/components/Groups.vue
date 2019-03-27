<template>
  <div class="groups container">
    <h1 class="page-header">Manage Groups</h1>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Name</th>
          <th>State</th>
          <th>Parent</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="group in groups">
          <td>{{ group.name }}</td>
          <td>{{ group.joins.state }}</td>
          <td>
            <a v-if="group.joins.parent" v-bind:href="group_url + group.joins.parent.id">{{ group.joins.parent.name }}</a>
          </td>
          <td class="actions">
            <a class="btn btn-primary" v-on:click="editGroup(group)">
              <edit-icon></edit-icon>
            </a>
            <a class="btn btn-danger" v-on:click="confirmDelete(group)">
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
  mounted() {
    EventBus.$on("fetchGroups", () => {
      setTimeout(() => this.fetchGroups(), 1000);
    })
  },
  created: function() {
    this.fetchGroups();
  },
  methods: {
    editGroup(group) {
      EventBus.$emit("editGroup", group);
    },
    confirmDelete(group) {
      this.$dialog
        .confirm("Do you really want to delete " + group.name + "?")
        .then(function() {
          EventBus.$emit("deleteGroup", group);
        })
        .catch(function() {
          console.log("Group delete aborted.");
        });
    },
    fetchGroups() {
      axios.get(this.group_url + "0").then(response => {
        this.groups = response.data;
      });
    }
  },
  created: function() {
    this.fetchGroups();
  }
};
</script>

<style scoped>
.actions a {
  color: white !important;
  margin-left: 5px;
}
</style>
