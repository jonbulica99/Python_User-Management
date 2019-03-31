<template>
  <div class="groups container card shadow-sm">
    <h1 class="page-header">Groups</h1>
    <table class="table table-hover table-responsive-sm">
      <thead class="thead-light">
        <tr>
          <th>Name</th>
          <th>State</th>
          <th>Parent</th>
          <th v-if="actions">Actions</th>
        </tr>
      </thead>
      <tbody v-bind:name="actions ? 'fade' : ''" is="transition-group">
        <template v-for="group in groups">
          <tr v-bind:key="group.id">
            <td>{{ group.name }}</td>
            <td>{{ group.joins.state }}</td>
            <td>
              <a
                v-if="group.joins.parent"
                v-bind:href="group_url + group.joins.parent.id"
              >{{ group.joins.parent.name }}</a>
              <div v-else>
                <i>None</i>
              </div>
            </td>
            <td class="actions" v-if="actions">
              <a class="btn btn-primary" v-on:click="editGroup(group)">
                <edit-icon></edit-icon>
              </a>
              <a class="btn btn-danger" v-on:click="confirmDelete(group)">
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
  name: "groups",
  props: {
    actions: Boolean
  },
  data() {
    return {
      groups: [],
      user_url: Endpoints.USERS,
      group_url: Endpoints.GROUPS
    };
  },
  created: function() {
    this.fetchGroups();
  },
  mounted() {
    EventBus.$on("fetchGroups", () => {
      this.fetchGroups();
    });
  },
  methods: {
    editGroup(group) {
      EventBus.$emit("editGroup", group);
    },
    confirmDelete(group) {
      this.$dialog
        .confirm("Do you really want to delete <b>" + group.name + "</b>?")
        .then(function() {
          EventBus.$emit("deleteGroup", group);
        })
        .catch(function() {
          console.log("Group delete aborted.");
        });
    },
    fetchGroups() {
      axios.get(this.group_url + "0").then(response => {
        response = response.data;
        if (response.success) {
          this.groups = response.data;
          EventBus.$emit("updateGroups", this.groups);
        } else {
          this.$dialog.alert(
            "<b>Error fetching groups</b>: " +
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
