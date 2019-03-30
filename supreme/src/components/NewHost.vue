<template>
  <div class="new-host container">
    <h1 class="page-header">{{ action }} Host</h1>
    <hr>
    <form v-on:submit.prevent="handleHost()" v-on:reset="resetForm()">
      <div class="form-row">
        <div class="col-md-5 mb-3">
          <label for="Hostname">Hostname</label>
          <input
            type="text"
            class="form-control"
            id="Hostname"
            v-model="host.name"
            placeholder="server.example.com"
            required
          >
        </div>
      </div>
      <div class="form-row">
        <div class="col-md-4 mb-3">
          <label for="address">IP address</label>
          <input
            type="text"
            class="form-control"
            id="lastname"
            v-model="host.address"
            placeholder="::1"
            required
          >
        </div>
        <div class="col-md-1 mb-3">
          <label for="port">SSH port</label>
          <input
            type="text"
            class="form-control"
            id="port"
            v-model="host.port"
            placeholder="22"
            required
          >
        </div>
      </div>
      <div class="form-row">
        <div class="col-md-3 mb-3">
          <label for="user">User</label>
          <multiselect
            id="user"
            v-model="userValue"
            :options="users"
            :close-on-select="true"
            track-by="id"
            label="username"
            placeholder="User"
            required
          ></multiselect>
        </div>
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
  name: "new_host",
  components: {
    Multiselect
  },
  data() {
    return {
      action: "New",
      host: {
        user: "",
        port: 22
      },
      host_url: Endpoints.HOSTS,
      user_url: Endpoints.USERS,
      users: []
    };
  },
  mounted() {
    EventBus.$on("editHost", data => {
      this.action = "Edit";
      this.host = data;
    });
    EventBus.$on("deleteHost", data => {
      this.action = "Delete";
      this.host = data;
      this.handleHost();
    });
    EventBus.$on("updateUsers", data => {
      this.users = data;
    });
  },
  created: function() {
    axios.get(this.user_url + "all").then(response => {
      this.users = response.data;
    });
  },
  methods: {
    handleHost() {
      this.host.user = this.userValue;

      if (!this.host.name) {
        this.$dialog.confirm("Please fill in the hostname.");
      } else if (!this.host.user && this.action != "Delete") {
        this.$dialog.confirm("Please select a valid user to use for connecting to the host.");
      } else {
        if (this.action === "New") {
          axios.post(this.host_url + "0", this.host).then(response => {
            let status = response.data.success;
            if (status) {
              this.$dialog.confirm("Host " + response.data.host.name + " created successfully.");
              EventBus.$emit("fetchHosts");
            } else {
              this.$dialog.confirm(response.data.message);
            }
          });
        } else if (this.action === "Edit") {
          axios.post(this.host_url + "1", this.host).then(response => {
            let status = response.data.success;
            if (status) {
              this.$dialog.confirm("Host " + this.host.name + " edited successfully.");
              EventBus.$emit("fetchHosts");
            } else {
              this.$dialog.confirm(response.data.message);
            }
          });
        } else if (this.action === "Delete") {
          axios.post(this.host_url + "2", this.host).then(response => {
            let status = response.data.success;
            if (status) {
              this.$dialog.confirm("Host " + this.host.name + " deleted successfully.");
              EventBus.$emit("fetchHosts");
            } else {
              this.$dialog.confirm(response.data.message);
            }
          });
        }
      }
    },
    resetForm() {
      this.host = {
        user: "",
        port: 22
      };
      this.action = "New";
    }
  },
  computed: {
    userValue: {
      get() {
        if (this.action === "New") {
          return this.host.user;
        } else {
          return this.host.joins.user;
        }
      },
      set(newVal) {
        if (this.action === "New") {
          this.host.user = newVal;
        } else {
          this.host.joins.user = newVal;
        }
      }
    }
  }
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style scoped>
</style>
