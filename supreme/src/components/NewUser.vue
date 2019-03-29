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
  },
  created: function() {
    setTimeout(
      () =>
        axios.get(this.group_url + "0").then(response => {
          this.groups = response.data;
        }),
      1000
    );
  },
  methods: {
    handleUser() {
      this.user.state = this.stateValue;
      this.user.groups = this.groupsValue;

      if (!this.user.firstname || !this.user.lastname) {
        alert("Please fill in first and last name.");
      } else if (!this.user.state) {
        alert("Please select a valid user state.");
      } else {
        if (this.action === "New") {
          axios.post(this.user_url + "new", this.user).then(response => {
            let status = response.data.success;
            if (status) {
              alert("User " + response.data.user.username + " created successfully.");
            } else {
              alert(response.data.message);
            }
          });
        } else if (this.action === "Edit") {
          axios.post(this.user_url + "edit", this.user).then(response => {
            let status = response.data.success;
            if (status) {
              alert("User " + this.user.username + " edited successfully.");
            } else {
              alert(response.data.message);
            }
          });
        } else if (this.action === "Delete") {
          axios.post(this.user_url + "delete", this.user).then(response => {
            let status = response.data.success;
            if (status) {
              alert("User " + this.user.username + " deleted successfully.");
            } else {
              alert(response.data.message);
            }
          });
        }
      }
      EventBus.$emit("fetchUsers");
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

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style scoped>
</style>
