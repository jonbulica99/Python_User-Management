<template>
  <div class="new-user container">
    <h1 class="page-header">{{ action }} User</h1>
    <hr>
    <form v-on:submit.prevent="handleUser()" v-on:reset="resetForm()">
      <div class="form-row">
        <div class="col-md-4 mb-3">
          <label for="firstname">First Name</label>
          <input
            type="text"
            class="form-control"
            id="firstname"
            v-model="user.firstname"
            placeholder="Max"
            required
          >
        </div>
        <div class="col-md-4 mb-3">
          <label for="lastname">Last Name</label>
          <input
            type="text"
            class="form-control"
            id="lastname"
            v-model="user.lastname"
            placeholder="Mustermann"
            required
          >
        </div>
      </div>
      <div class="form-row">
        <div class="col-md-4 mb-3">
          <label for="username">Username</label>
          <input
            type="text"
            class="form-control"
            id="username"
            v-model="user.username"
            placeholder="maxmustermann"
            required
          >
        </div>
        <div class="col-md-4 mb-3">
          <label for="password">Password</label>
          <input
            type="password"
            class="form-control"
            id="password"
            v-model="user.password"
            placeholder="Password"
            required
          >
        </div>
      </div>
      <div class="form-row">
        <div class="col-md-3 mb-3">
          <label for="state">State</label>
          <multiselect
            id="state"
            v-model="stateValue"
            :options="user_states"
            :close-on-select="true"
            placeholder="State"
          ></multiselect>
        </div>
        <div class="col-md-3 mb-3">
          <label for="groups">Groups</label>
          <multiselect
            id="groups"
            v-model="groupsValue"
            :multiple="true"
            :options="groups"
            :searchable="true"
            :close-on-select="false"
            track-by="id"
            label="name"
            placeholder="Groups"
          ></multiselect>
        </div>
      </div>
      <div class="form-group">
        <label for="publicKey">Public SSH Key</label>
        <textarea
          class="form-control"
          id="publicKey"
          rows="2"
          v-model="user.publicKey"
          placeholder="ssh-rsa AAAAB..."
        ></textarea>
      </div>
      <button class="btn btn-primary" type="submit">Submit</button>
      <span>&nbsp;</span>
      <button class="btn btn-danger" type="reset">Reset</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import { EventBus } from "@/events.js";
import { Endpoints } from "@/variables.js";
import Multiselect from "vue-multiselect";

export default {
  name: "new_user",
  components: {
    Multiselect
  },
  data() {
    return {
      action: "New",
      user: {
        state: "present",
        groups: []
      },
      user_states: ["present", "absent", "inactive"],
      user_url: Endpoints.USERS,
      group_url: Endpoints.GROUPS,
      groups: []
    };
  },
  mounted() {
    EventBus.$on("editUser", data => {
      this.action = "Edit";
      this.user = data;
    });
    EventBus.$on("deleteUser", data => {
      this.action = "Delete";
      this.user = data;
      this.handleUser();
    });
    EventBus.$on("updateGroups", data => {
      this.groups = data;
    })
  },
  created: function() {
      axios.get(this.group_url + "0").then(response => {
        response = response.data;
        if(response.success){
          this.groups = response.data;
          EventBus.$emit("updateGroups", this.groups);
        } else {
          this.$dialog.alert("<b>Error fetching groups</b>: " + response.message + "<br><i>Check the console log for more information.</i>"); 
          console.log(response.exception);
        }
      });
  },
  methods: {
    handleUser() {
      this.user.state = this.stateValue;
      this.user.groups = this.groupsValue;

      if (!this.user.firstname || !this.user.lastname) {
        this.$dialog.alert("Please fill in first and last name.");
      } else if (!this.user.state) {
        this.$dialog.alert("Please select a valid user state.");
      } else {
        if (this.action === "New") {
          axios.post(this.user_url + "new", this.user).then(response => {
            response = response.data
            if (response.success) {
              this.$dialog.alert("User <b>" + response.data.username + "</b> created successfully.");
              EventBus.$emit("fetchUsers");
            } else {
              this.$dialog.alert("<b>Add operation failed</b>: " + response.message); 
              console.log(response.exception);
            }
          });
        } else if (this.action === "Edit") {
          axios.post(this.user_url + "edit", this.user).then(response => {
            response = response.data
            if (response.success) {
              this.$dialog.alert("User <b>" + this.user.username + "</b> edited successfully.");
              EventBus.$emit("fetchUsers");
            } else {
              this.$dialog.alert("<b>Edit operation failed</b>: " + response.message); 
              console.log(response.exception);
            }
          });
        } else if (this.action === "Delete") {
          axios.post(this.user_url + "delete", this.user).then(response => {
            response = response.data
            if (response.success) {
              this.$dialog.alert("User <b>" + this.user.username + "</b> deleted successfully.");
              EventBus.$emit("fetchUsers");
            } else {
              this.$dialog.alert("<b>Delete operation failed</b>: " + response.message); 
              console.log(response.exception);
            }
          });
        }
      }
    },
    resetForm() {
      this.user = {
        state: "present",
        groups: []
      };
      this.action = "New";
    }
  },
  computed: {
    groupsValue: {
      get() {
        if (this.action === "New") {
          return this.user.groups;
        } else {
          return this.user.joins.groups;
        }
      },
      set(newVal) {
        if (this.action === "New") {
          this.user.groups = newVal;
        } else {
          this.user.joins.groups = newVal;
        }
      }
    },
    stateValue: {
      get() {
        if (this.action === "New") {
          return this.user.state;
        } else {
          return this.user.joins.state;
        }
      },
      set(newVal) {
        if (this.action === "New") {
          this.user.state = newVal;
        } else {
          this.user.joins.state = newVal;
        }
      }
    }
  }
};
</script>

<style scoped>
</style>
